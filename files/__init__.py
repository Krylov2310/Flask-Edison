from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


db = SQLAlchemy()  # Объект базы данных
babel = Babel()  # Перевод приложения с разных языков
migrate = Migrate()  # Миграции
bcrypt = Bcrypt()  # Безопасность

'''
Блок главных настроек
'''


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('setting.py')
    db.init_app(app)
    babel.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from files.routes import MyMainView, MySignInView, MyLoginView, MyAccountView, MyInfo, MyDashboardView  #, MyImageFeedView, MyDetectObjectView  # Создаёт модели
    from models import User, Storage, ImageFeed
    from files.views.user_view import UserView
    from files.views.image_feed_view import ImageFeedView
    from files.views.storage_view import StorageView
    admin = Admin(app, 'Приложение на Flask для распознавания объектов', index_view=MyMainView(), url='/')

    admin.add_view(MyInfo(name='О проекте', url='info'))
    admin.add_view(MyDashboardView(name='Dashboard', url='dashboard'))
    admin.add_view(StorageView(Storage, db.session, name='Архив файлов'))
    admin.add_view(ImageFeedView(ImageFeed, db.session, category='Админка', name='Добавить изображение'))
    admin.add_view(MyLoginView(name='Логин', category='Админка', url='login'))
    admin.add_view(MySignInView(name='Регистрация', category='Админка', url='register'))
    admin.add_view(MyAccountView(name='Аккаунты', category='Админка', url='account'))
    admin.add_view(UserView(User, db.session, name='Пользователи', category='Админка', endpoint='admin/user'))

    # admin.add_view(MyExitView(name='Выход', url='exit'))

    return app
