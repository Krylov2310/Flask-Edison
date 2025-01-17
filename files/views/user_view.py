import os
from flask import url_for
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from wtforms import validators

from files import bcrypt

'''
Модуль пользователей
'''

file_path = os.path.abspath(os.path.dirname(__name__))  # Абсолютный путь к файлам


# Функция, которая будет генерировать имя файла из модели и загруженного файлового объекта.
def name_gen_image(model, file_data):
    hash_name = f'{model}/{model.username}'
    return hash_name


# Поля для таблици
class UserView(ModelView):
    column_display_pk = True  # Управление отображением колонок
    column_labels = {
        'id': 'ID',
        'username': 'Логин',
        'last_name': 'Имя',
        'first_name': 'Фамилия',
        'last_seen': 'Последний вход',
        'image_user': 'Аватар',
        'dashboards': 'Dashboard',
        'email': 'Email',
        'password': 'Пароль',
        'role': 'Роль',
        'file': 'Выберите изображение'
    }  # Переименовываем поля

    # Настраиваем какие поля показывать
    column_list = ['id', 'role', 'username', 'last_name',  'first_name', 'email', 'password', 'last_seen', 'image_user']
    # Колонка сортировки по умолчанию
    column_default_sort = ('username', True)
    # Список колонок сортировки
    column_sortable_list = ('id', 'role', 'last_name', 'first_name', 'email', 'username')
    # Поиск
    column_searchable_list = ['username', 'last_name',  'first_name', 'email']

    # 4 Метода can разрешения для полей
    can_create = True  # Разрешение на создание
    can_edit = True  # Разрешение на редактирование
    can_delete = True  # Разрешение на удаление
    can_export = True  # Разрешение на экспортирование
    export_max_rows = 500  # Количество максимальных строк
    export_types = ['csv']  # Формат экспорта

    # Форм аргумент валидаторы для ввода данных (правила для полей)
    form_args = {
        'username': dict(label='Логин', validators=[validators.DataRequired()]),
        'last_name': dict(label='Имя', validators=[validators.DataRequired()]),
        'first_name': dict(label='Фамилия', validators=[validators.DataRequired()]),
        'email': dict(label='Почта', validators=[validators.Email()]),
        'password': dict(label='Пароль', validators=[validators.DataRequired()]),
    }

    # Список аргументов для полей роли
    AVAILABLE_USER_TYPES = [
        (u'User', u'User'),
        (u'Admin', u'Admin'),
    ]

    # Оппределяем аргумент для поля
    form_choices = {
        'role': AVAILABLE_USER_TYPES,
    }

    # Словарь, где ключ — это имя столбца, а значение — описание столбца представления списка или поля формы
    # добавления/редактирования.
    column_descriptions = dict(
        role='Роль пользователя',
        username='Логин',
        last_name='Имя',
        first_name='Фамилия',
        email='Адрес электронной почты'
    )

    # исключенные колонки
    column_exclude_list = ['password']
    # Колонка поиска
    column_searchable_list = ['last_name', 'first_name', 'email', 'username']
    # Фильтр поиска
    column_filters = ['last_name', 'first_name', 'email', 'username']
    # Редактирование прямо в списке
    column_editable_list = ['role', 'last_name', 'first_name', 'email', 'username']

    # Модальные окна из Bootstrap открывается в отдельном окне
    # create_modal = True  # При создании
    # edit_modal = True  # При редактировании

    # Исключить колонку из создания, редактирования
    form_excluded_columns = ['id']

    # Установка фото на аватар
    def _list_thumbnail(view, context, model, name):  # model = User
        if not model.image_user:
            return ''

        url = url_for('static', filename=os.path.join('storage/user_img/', model.image_user))
        if model.image_user.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:  # Сверка формата файла
            return Markup(f'<img src={url} width="100">')


    # передаю функцию _list_thumbnail в поле image_user
    column_formatters = {
        'image_user': _list_thumbnail  # Передаем работу функции прямо в поле
    }

    form_extra_fields = {
        # ImageUploadField Выполняет проверку изображений, создание эскизов, обновление и удаление изображений.
        "image_user": form.ImageUploadField('',
                                            # Абсолютный путь к каталогу, в котором будут храниться файлы
                                            base_path=
                                            os.path.join(file_path, 'files/static/storage/user_img'),
                                            # Относительный путь из каталога. Будет добавляться к имени загружаемого файла.
                                            url_relative_path='storage/user_img/',
                                            namegen=name_gen_image,
                                            # Список разрешенных расширений. Если не указано, то будут разрешены форматы gif, jpg, jpeg, png и tiff.
                                            allowed_extensions=['jpg'],
                                            max_size=(1200, 780, True),  # Обрезка фото
                                            thumbnail_size=(100, 100, True),  # Размер миниатюры
                                            )}

    # Создание объекта
    def create_form(self, obj=None):
        return super(UserView, self).create_form(obj)

    # Редактировать объект
    def edit_form(self, obj=None):
        return super(UserView, self).edit_form(obj)

    # Шифрование паролей
    def on_model_change(self, view, model, is_created):
        model.password = bcrypt.generate_password_hash(model.password)
