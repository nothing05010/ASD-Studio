"""
ASD Studio — Модели базы данных.
Таблицы: User, BotItem, Review.
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Пользователь сайта (логин, пароль, роль)."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    reviews = db.relationship('Review', backref='user', lazy='dynamic')

    def set_password(self, password: str) -> None:
        """Хешировать и сохранить пароль."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Проверить пароль по хешу."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class BotItem(db.Model):
    """Telegram-бот в каталоге студии."""
    __tablename__ = 'bot_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    category = db.Column(db.String(80), nullable=False, default='General')
    icon = db.Column(db.String(10), nullable=False, default='bot')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def price_formatted(self) -> str:
        """Форматирование цены с разделителем тысяч."""
        return f'{self.price:,.0f}'.replace(',', ' ')

    def __repr__(self):
        return f'<BotItem {self.name}>'


class Review(db.Model):
    """Отзыв клиента (с системой модерации)."""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)  # 1-5
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<Review by {self.author_name} ({self.rating}/5)>'
