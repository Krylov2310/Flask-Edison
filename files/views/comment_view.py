from flask_admin.contrib.sqla import ModelView


class CommentView(ModelView):  # Управление отображением колонок
    column_labels = {
        'name': 'Имя комментария'
    }

    # 4 Метода can разрешения для полей
    can_delete = True
    can_create = True
    can_edit = True
