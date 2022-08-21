from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100),
})


movie: Model = api.model('Фильмы', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100),
    'description': fields.String(required=True, max_length=100),
    'trailer': fields.String(required=True, max_length=100),
    'year': fields.String(required=True, max_length=100),
    'rating': fields.Float(required=True, max_length=100),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director)
})

user: Model = api.model('Пользователи', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100),
    'password': fields.String(required=True, max_length=100),
    'name': fields.String(required=True, max_length=100),
    'surname': fields.String(required=True, max_length=100),
    'favorite_genre': fields.Nested(genre)
})
