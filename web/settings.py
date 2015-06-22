#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'bp'
__version__ = (0, 0, 1)


class User(object):
    def __init__(self, username, password, alias):
        self.username = username
        self.password = password
        self.alias = alias


BASICAUTH = {
    'bp': User('bp', '123qwe', u'Павлик'),
    'masha': User('masha', 'stillsingleat33', u'Мари'),
}

