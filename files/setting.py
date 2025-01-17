import os

# Основные настройки и пути
SQLALCHEMY_DATABASE_URI = 'sqlite:///fl_base.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(20)
FLASK_ADMIN_SWATCH = 'cosmo'  # Тема приложения
BABEL_DEFAULT_LOCALE = 'ru'  # Языки приложения
