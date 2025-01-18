import os
from flask import redirect, url_for
from files import create_app, db
from files.mechanics import process_image
from models import ImageFeed, DetectedObject

'''
Блок управления
'''
app = create_app()
file_path = os.path.abspath(os.path.dirname(__name__))
STORAGE = os.path.join(file_path, 'files/static/media_file/')


@app.route('/')  # Основной маршрут
def main():
    return redirect(url_for('admin.admin_main'))


# Передача на распознакание картинки
@app.route('/dashboard/<int:id>', methods=['POST', 'GET'])
def process_image_feed(id):
    image_feed = ImageFeed.query.get_or_404(id)
    process_image(image_feed.id)
    return redirect('/dashboard')


# Удаление картинки
@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_image_feed(id):
    print('delete_id =', id)
    try:
        img = ImageFeed.query.get_or_404(id)
        if db.session.query(DetectedObject).filter(DetectedObject.image_feed == img.id).delete():
            os.remove(f'{STORAGE}{img.processed_image}')
        os.remove(f'{STORAGE}{img.image}')
        db.session.delete(img)
        db.session.commit()
        return redirect('/dashboard')
    except:
        return redirect('/dashboard')


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=False)
