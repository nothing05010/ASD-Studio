"""
ASD Studio -- Главное Flask-приложение.
Маршруты, авторизация, отзывы, админ-панель.
"""

import os
from datetime import datetime, timezone
from functools import wraps

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, abort
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from models import db, User, BotItem, Review

# =====================================================================
#  ИНИЦИАЛИЗАЦИЯ
# =====================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asd-studio-2026-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asd_studio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Войдите в аккаунт для доступа.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def admin_required(fn):
    """Декоратор: доступ только для администраторов."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_globals():
    """Глобальные переменные для шаблонов."""
    pending = 0
    if current_user.is_authenticated and current_user.is_admin:
        pending = Review.query.filter_by(is_approved=False).count()
    return {
        'current_year': datetime.now(timezone.utc).year,
        'pending_count': pending,
    }


# =====================================================================
#  ПУБЛИЧНЫЕ СТРАНИЦЫ
# =====================================================================

@app.route('/')
def index():
    """Главная: Hero + каталог ботов + одобренные отзывы."""
    bots = BotItem.query.order_by(BotItem.created_at.desc()).all()
    reviews = Review.query.filter_by(is_approved=True) \
                          .order_by(Review.created_at.desc()).all()
    return render_template('index.html', bots=bots, reviews=reviews)


@app.route('/bot/<int:bot_id>')
def bot_detail(bot_id):
    """Страница конкретного бота."""
    bot = db.session.get(BotItem, bot_id)
    if not bot:
        abort(404)
    return render_template('bot_detail.html', bot=bot)


# =====================================================================
#  АВТОРИЗАЦИЯ
# =====================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация нового пользователя."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        password2 = request.form.get('password2', '').strip()

        if not username or not password:
            flash('Заполните все поля.', 'error')
            return redirect(url_for('register'))
        if len(username) < 3:
            flash('Логин: минимум 3 символа.', 'error')
            return redirect(url_for('register'))
        if len(password) < 6:
            flash('Пароль: минимум 6 символов.', 'error')
            return redirect(url_for('register'))
        if password != password2:
            flash('Пароли не совпадают.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Такой логин уже занят.', 'error')
            return redirect(url_for('register'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Аккаунт создан! Войдите.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Вход в аккаунт."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Привет, {user.username}!', 'success')
            return redirect(request.args.get('next') or url_for('index'))

        flash('Неверный логин или пароль.', 'error')
        return redirect(url_for('login'))

    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    """Выход из аккаунта."""
    logout_user()
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('index'))


# =====================================================================
#  ОТЗЫВЫ
# =====================================================================

@app.route('/review', methods=['GET', 'POST'])
def submit_review():
    """Форма отправки отзыва (сохраняется со статусом 'ожидает')."""
    if request.method == 'POST':
        author = request.form.get('author_name', '').strip()
        text = request.form.get('text', '').strip()
        rating = request.form.get('rating', 5, type=int)

        if not author or not text:
            flash('Заполните все поля.', 'error')
            return redirect(url_for('submit_review'))
        if not (1 <= rating <= 5):
            flash('Рейтинг от 1 до 5.', 'error')
            return redirect(url_for('submit_review'))
        if len(text) < 10:
            flash('Минимум 10 символов в отзыве.', 'error')
            return redirect(url_for('submit_review'))

        review = Review(
            author_name=author,
            text=text,
            rating=rating,
            is_approved=False,
            user_id=current_user.id if current_user.is_authenticated else None,
        )
        db.session.add(review)
        db.session.commit()

        flash('Отзыв отправлен на модерацию!', 'success')
        return redirect(url_for('index'))

    return render_template('review_form.html')


# =====================================================================
#  АДМИН-ПАНЕЛЬ
# =====================================================================

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Дашборд: статистика + управление отзывами."""
    stats = {
        'bots': BotItem.query.count(),
        'reviews': Review.query.count(),
        'pending': Review.query.filter_by(is_approved=False).count(),
        'users': User.query.count(),
    }
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('admin/dashboard.html', stats=stats, reviews=reviews)


@app.route('/admin/review/<int:rid>/approve', methods=['POST'])
@login_required
@admin_required
def approve_review(rid):
    """Одобрить отзыв (сделать публичным)."""
    review = db.session.get(Review, rid)
    if not review:
        abort(404)
    review.is_approved = True
    db.session.commit()
    flash(f'Отзыв от "{review.author_name}" опубликован.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/review/<int:rid>/delete', methods=['POST'])
@login_required
@admin_required
def delete_review(rid):
    """Удалить отзыв безвозвратно."""
    review = db.session.get(Review, rid)
    if not review:
        abort(404)
    name = review.author_name
    db.session.delete(review)
    db.session.commit()
    flash(f'Отзыв от "{name}" удален.', 'warning')
    return redirect(url_for('admin_dashboard'))


# =====================================================================
#  ОШИБКИ
# =====================================================================

@app.errorhandler(403)
def err_403(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def err_404(e):
    return render_template('errors/404.html'), 404


# =====================================================================
#  ЗАПУСК
# =====================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
