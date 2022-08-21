import base64
import calendar
import datetime
import hashlib

import jwt
from flask import current_app


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


# Хешируем пароль
def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_password(password_hash, other_password):
    """
    :param password_hash: пароль из БД
    :param other_password: пароль, который прислал пользователь
    """
    return password_hash == generate_password_hash(other_password)


# Генерируем токен
def generate_token(email, password, password_hash, refresh=False):
    if not email:
        return "Не хватает данных"

    if not refresh:
        if not compare_password(password_hash=password_hash, other_password=password):
            return "Что-то пошло не так"

    data = {
        "email": email,
        "password": password
    }
    # Временный токен
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGORITHM"])

    # Обновляем токен для длительного доступа
    min_day = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_DAY"])
    data["exp"] = calendar.timegm(min_day.timetuple())
    refresh_token = jwt.encode(data, key=current_app.config["SECRET_KEY"], algorithm=current_app.config["ALGORITHM"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# Обновляем токен
def update_token(refresh_token):
    data = jwt.decode(refresh_token, key=current_app.config["SECRET_KEY"], algorithms=current_app.config["ALGORITHM"])

    email = data.get("email")
    password = data.get("password")

    return generate_token(email=email, password=password, password_hash=None, refresh=True)


def data_by_token(refresh_token):
    data = jwt.decode(refresh_token, key=current_app.config["SECRET_KEY"], algorithms=current_app.config["ALGORITHM"])

    return data
