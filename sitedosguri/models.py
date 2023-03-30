from sitedosguri import database, login_manager
from datetime import datetime
from flask_login import UserMixin



@login_manager.user_loader
def load_user(id_usuario):
    return User.query.get(int(id_usuario))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    image_file = database.Column(database.String(20), nullable=False, default='default.jpg')
    password = database.Column(database.String(60), nullable=False)
    cursos = database.Column(database.String, nullable=False, default='Não Informado.')
    posts = database.relationship('Post', backref='author', lazy=True)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    content = database.Column(database.Text, nullable=False)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

