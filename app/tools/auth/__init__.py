from secrets import token_urlsafe

from flask import current_app
from itsdangerous import URLSafeSerializer
from werkzeug.security import generate_password_hash, check_password_hash


def encrypt_cookie(content):
    s = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="cookie")
    encrypted_content = s.dumps(content)
    return encrypted_content


def decrypt_cookie(encrypted_content):
    s = URLSafeSerializer(current_app.config["SECRET_KEY"], salt="cookie")
    try:
        content = s.loads(encrypted_content)
    except:
        content = "-1"
    return content


def generate_token():
    return token_urlsafe(30)


def generate_hash(token):
    return generate_password_hash(token)


def _check_token(hash, token):
    return check_password_hash(hash, token)
