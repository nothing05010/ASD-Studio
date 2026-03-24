"""
ASD Studio -- Наполнение БД тестовыми данными.
Создает: admin, demo-пользователь, 5 ботов, 4 отзыва.
"""

from app import app
from models import db, User, BotItem, Review


def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # ---- Пользователи ----
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin123')

        demo = User(username='demo', is_admin=False)
        demo.set_password('demo123')

        db.session.add_all([admin, demo])

        # ---- Каталог ботов ----
        bots = [
            BotItem(
                name='ShopMaster Pro',
                description=(
                    'Полноценный интернет-магазин внутри Telegram. Каталог товаров '
                    'с категориями и поиском, корзина покупок, интеграция с платежными '
                    'системами ЮKassa и Stripe. CRM-панель для владельца с аналитикой '
                    'продаж, автоматические уведомления о статусе заказа, промокоды '
                    'и система лояльности для постоянных клиентов.'
                ),
                price=45000,
                category='E-Commerce',
                icon='cart',
            ),
            BotItem(
                name='SupportDesk AI',
                description=(
                    'Интеллектуальная служба поддержки с AI-движком на базе GPT-4. '
                    'Автоматическая маршрутизация обращений, база знаний с нейросетевым '
                    'поиском, система тикетов с приоритетами и SLA. Передача сложных '
                    'вопросов живому оператору, мультиязычность, дашборд аналитики '
                    'с метриками CSAT, NPS и средним временем ответа.'
                ),
                price=38000,
                category='Business',
                icon='headset',
            ),
            BotItem(
                name='ContentFlow',
                description=(
                    'Автоматизация контент-маркетинга для Telegram-каналов. '
                    'Визуальный планировщик публикаций, авто-постинг из RSS и соцсетей, '
                    'генерация текстов и изображений с помощью AI. Watermark на фото, '
                    'A/B тестирование заголовков, глубокая аналитика вовлечённости '
                    'и роста подписчиков в реальном времени.'
                ),
                price=28000,
                category='Marketing',
                icon='megaphone',
            ),
            BotItem(
                name='BookingPro',
                description=(
                    'Система онлайн-записи и бронирования для сферы услуг. '
                    'Интерактивный календарь с выбором даты и времени, напоминания '
                    'клиентам за 24 часа и за 1 час до визита. Управление '
                    'расписанием нескольких мастеров, интеграция с Google Calendar, '
                    'приём предоплаты и накопительные скидки для постоянных клиентов.'
                ),
                price=32000,
                category='Services',
                icon='calendar',
            ),
            BotItem(
                name='EduPlatform',
                description=(
                    'Образовательная LMS-платформа в Telegram. Система курсов '
                    'с модулями и уроками, интерактивные квизы с мгновенной проверкой, '
                    'отслеживание прогресса учеников. Геймификация: XP, уровни, ачивки. '
                    'Поддержка видео-уроков, домашних заданий, выдача сертификатов '
                    'и обратная связь от преподавателя.'
                ),
                price=52000,
                category='Education',
                icon='graduation',
            ),
        ]
        db.session.add_all(bots)

        # ---- Отзывы ----
        reviews = [
            Review(
                author_name='Alexey K.',
                text=(
                    'Ordered a bot for our online store -- the result exceeded all '
                    'expectations! The bot runs stable, customers love it. '
                    'Highly recommend ASD Studio!'
                ),
                rating=5,
                is_approved=True,
            ),
            Review(
                author_name='Marina S.',
                text=(
                    'We got a support bot for our company. Response speed tripled '
                    'and the operator workload dropped significantly. Great job!'
                ),
                rating=5,
                is_approved=True,
            ),
            Review(
                author_name='Elena V.',
                text=(
                    'The booking bot for our beauty salon is amazing! Clients book '
                    'appointments themselves, freeing up so much of our time.'
                ),
                rating=4,
                is_approved=True,
            ),
            Review(
                author_name='Dmitry L.',
                text='Good bot, but would love more design customization options.',
                rating=3,
                is_approved=False,
            ),
        ]
        db.session.add_all(reviews)

        db.session.commit()

        print('[OK] Database seeded!')
        print(f'  Users:   {User.query.count()}')
        print(f'  Bots:    {BotItem.query.count()}')
        print(f'  Reviews: {Review.query.count()}')


if __name__ == '__main__':
    seed()
