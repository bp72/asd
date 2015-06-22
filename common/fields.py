#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'bp'
__version__ = (0, 0, 1)

import os
import hashlib

################################################################################
class BaseField(object):
    """
    >>> class MyClass(object):
    ...     fld = BaseField()
    >>> a = MyClass()
    >>> a.fld = 'asd'
    >>> a.fld
    'asd'
    """
    def __init__(self, name=None):
        self.name = self.mangle(name)


    def mangle(self, name):
        if name is None:
            return
        if name.startswith('__'):
            raise AttributeError(u'Возможен конфликт')
        if name.startswith('_'):
            return '_' + name
        return '__' + name


    def fetchname(self, instance):
        for attr in filter(lambda a: not a.startswith('_'), instance.__class__.__dict__):
            obj = instance.__class__.__dict__[attr]
            if obj == self:
                self.name = self.mangle(attr)


    def __set__(self, instance, value):
        if self.name is None:
            self.fetchname(instance)
        instance.__dict__[self.name] = value


    def __get__(self, instance, owner):
        if self.name is None:
            self.fetchname(instance)
        return instance.__dict__[self.name]

# end of class BaseField(object)
################################################################################


################################################################################
class MD5Field(BaseField):
    """
    Дескриптор расчета MD5
    >>> with open('./filename.txt', 'w') as f:
    ...     f.write('1')
    ...     f.close()
    >>> class MyClass(object):
    ...     md5sum = MD5Field()
    ...     filename = 'filename.txt'
    ...     def __init__(self, name=None):
    ...         self.name = name
    >>> c = MyClass('filename.txt')
    >>> c.md5sum
    'c4ca4238a0b923820dcc509a6f75849b'

    """

    class FileDoesNotExist(Exception):
        def __init__(self, filename, *args, **kwargs):
            self.message = u'Загружается несуществующий файл/попытка чтения MD5 для несуществующего файла: {}'.format(filename)

    def __init__(self, name=None, root=None):
        super(MD5Field, self).__init__(name=name)
        self.root = root or '.'


    def __get__(self, instance, owner):
        if self.name is None:
            self.fetchname(instance)
        try:
            return instance.__dict__[self.name]
        except KeyError:
            filepath = '{}/{}'.format(self.root, instance.filename)
            if not os.path.exists(filepath):
                return None
            instance.__dict__[self.name] = hashlib.md5(open(filepath, 'rb').read()).hexdigest()
            return instance.__dict__[self.name]

# end of class MD5Field(BaseField)
################################################################################


################################################################################
class FilenameField(BaseField):
    """
    Обект имени файла

    >>> class MyClass(object):
    ...     fld = FilenameField()
    >>> a = MyClass()
    >>> a.fld = 'asd'
    >>> a.fld
    'asd'
    """

# end of class FilenameField(BaseField)
################################################################################





