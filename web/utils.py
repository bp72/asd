#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'bp'
__version__ = (0, 0, 1)


from functools import wraps
from flask import request, Response
from settings import BASICAUTH


def check_auth(username, password):
    """
    Валидация пароля
    :param username: str
    :param password: str
    :return: bool
    """
    try:
        return BASICAUTH[username].password == password
    except KeyError:
        return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Введи логин и пароль.\n'
    '--- ---', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated