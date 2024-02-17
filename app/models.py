from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

user_pokemon = db.Table(
    'user_pokemon',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('name', db.String, db.ForeignKey('pokemon.name'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    caught_pokemon = db.relationship('Pokemon',
                             secondary=user_pokemon,
                             backref="caught_by",
                             lazy="dynamic")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Pokemon(db.Model):
    name = db.Column(db.String, primary_key=True)
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    sprite_img = db.Column(db.String, nullable=False)

    def __init__(self, name, hp, attack, defense, sprite_img):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sprite_img = sprite_img

    def save(self):
        db.session.add(self)
        db.session.commit()

