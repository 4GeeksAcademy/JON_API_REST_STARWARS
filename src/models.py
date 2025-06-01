# src/models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ----------------------------------------------------------------
# MODELOS PRINCIPALES: User, Person (people), Planet y tablas de favoritos
# ----------------------------------------------------------------

class User(db.Model):
    __tablename__ = 'users'
    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(50), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name  = db.Column(db.String(50), nullable=True)
    joined_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación Uno-a-muchos con Post (si en el futuro quieres posts de blog)
    posts = db.relationship('Post', backref='author', cascade='all, delete-orphan')

    # Relación Muchos-a-muchos con Planet (favoritos de planetas)
    favorite_planets = db.relationship(
        'Planet',
        secondary='favorite_planets',
        back_populates='fans'
    )

    # Relación Muchos-a-muchos con Person (favoritos de personajes)
    favorite_characters = db.relationship(
        'Person',
        secondary='favorite_characters',
        back_populates='fans'
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Person(db.Model):
    """
    Equivalente a 'people' en SWAPI.  
    Cada registro representa un personaje de StarWars.
    """
    __tablename__ = 'people'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), unique=True, nullable=False)
    birth_year = db.Column(db.String(20), nullable=True)
    gender     = db.Column(db.String(20), nullable=True)
    eye_color  = db.Column(db.String(50), nullable=True)

    # Relación Muchos-a-muchos con User (favoritos de personajes)
    fans = db.relationship(
        'User',
        secondary='favorite_characters',
        back_populates='favorite_characters'
    )

    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}')>"


class Planet(db.Model):
    """
    Tabla de planetas de StarWars.
    """
    __tablename__ = 'planets'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), unique=True, nullable=False)
    climate    = db.Column(db.String(100), nullable=True)
    terrain    = db.Column(db.String(100), nullable=True)
    population = db.Column(db.Integer, nullable=True)

    # Relación Muchos-a-muchos con User (favoritos de planetas)
    fans = db.relationship(
        'User',
        secondary='favorite_planets',
        back_populates='favorite_planets'
    )

    def __repr__(self):
        return f"<Planet(id={self.id}, name='{self.name}')>"


class Post(db.Model):
    """
    (Opcional) - Si en algún momento quieres extender tu API para que 
    los usuarios puedan escribir posts en el blog.
    """
    __tablename__ = 'posts'
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title[:20]}...', user_id={self.user_id})>"


# Tablas de asociación (many-to-many) para favoritos:
favorite_planets = db.Table(
    'favorite_planets',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id',   db.Integer, db.ForeignKey('users.id'),   nullable=False),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.id'), nullable=False),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

favorite_characters = db.Table(
    'favorite_characters',
    db.Column('id',           db.Integer, primary_key=True),
    db.Column('user_id',      db.Integer, db.ForeignKey('users.id'),   nullable=False),
    db.Column('person_id',    db.Integer, db.ForeignKey('people.id'),  nullable=False),
    db.Column('created_at',   db.DateTime, default=datetime.utcnow)
)
