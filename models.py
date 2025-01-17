from files import db

'''
Блок моделей
'''


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100), nullable=True, default='User')  # Роли
    username = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    image_user = db.Column(db.String(255), nullable=True, default='default.jpg')

    def __repr__(self):
        return self.username


class ImageFeed(db.Model):
    __tablename__ = 'image_feed'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    image = db.Column(db.String(128))
    processed_image = db.Column(db.String(128))
    type = db.Column(db.String(4))
    create_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<ImageFeed %r>' % self.image


class DetectedObject(db.Model):
    __tablename__ = 'detected_object'

    id = db.Column(db.Integer, primary_key=True)
    # image_feed = db.Column(db.Integer, db.ForeignKey('image_feed.processed_image', ondelete='CASCADE'))
    image_feed = db.Column(db.Integer, db.ForeignKey('image_feed.id'))
    object_type = db.Column(db.String(100))
    confidence = db.Column(db.Float())
    location = db.Column(db.String(255))

    def __repr__(self):
        return '<DetectedObject %r>' % f"{self.object_type} ({self.confidence * 100}%) on {self.image_feed}"


class Storage(db.Model):
    __tablename__ = 'storage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    path = db.Column(db.String(128))
    type = db.Column(db.String(4))
    create_date = db.Column(db.DateTime)
