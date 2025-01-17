from flask import url_for, redirect
from flask_admin import expose, BaseView, AdminIndexView
from sqlalchemy import desc
from models import User, ImageFeed, DetectedObject
from files import db
'''
Блок маршутизации
'''


# Главная страница Админа
class MyMainView(AdminIndexView):
    @expose('/')
    def admin_main(self):
        context = {
            'text': 'Добро пожаловать',
            'message': 'Только для зарегистрированных пользователей!',
            'button_key': 'Вход',
        }
        return self.render('admin/index.html', context=context)


class MyInfo(BaseView):
    @expose('/')
    def info(self):
        return self.render('admin/info_user.html')


# Страница регистрации
class MySignInView(BaseView):
    @expose('/')
    def sing_in(self):
        return self.render('admin/sign_in.html', legend='Регистрация')


# Страница входа
class MyLoginView(BaseView):
    @expose('/')
    def login(self):
        return self.render('admin/login.html', legend='Войти')


# Страница аккаунта
class MyAccountView(BaseView):
    @expose('/')
    def account(self):
        users = User.query.all()
        return self.render('admin/account.html', users=users)


# Страница интелектуального распознавания
class MyDashboardView(BaseView):
    @expose('/')
    def dashboard(self):
        # Выводим все картинки на экран
        image_feeds = ImageFeed.query.all()
        image_detects = DetectedObject.query.all()
        context = {
            'text': 'Dashboard:',
            'message': 'Все изображения.',
            'button_key': 'Добавить изображение',
        }
        return self.render('admin/dashboard.html', image_feeds=image_feeds, image_detects=image_detects, context=context)


