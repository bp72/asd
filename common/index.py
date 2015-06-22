#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'bp'
__version__ = (0, 0, 1)


################################################################################
class BaseIndex(object):
    class FileExists(Exception):
        def __init__(self, filename):
            self.message = u'Файл уже присутвует в индексе: {}'.format(filename)


    class FileNotFound(Exception):
        def __init__(self, filename):
            self.message = u'Файл не найден в индексе: {}'.format(filename)


    class FileDuplicate(Exception):
        def __init__(self, filename):
            self.message = u'Опаньки! Как так случилось, что файлов больше 1го: {}'.format(filename)


    def reset_index(self):
        """
        Сброс индекса
        """
        raise NotImplementedError


    def remove_from_index(self, user, alias):
        """
        Удаление файла из индекса
        :param user:
        :param alias:
        :return:
        """
        raise NotImplementedError


    def add_to_index(self, user, alias, content):
        """
        Добавление файла в индекс
        :param content:
        :return:
        """
        raise NotImplementedError


# end of class BaseIndex(object)
################################################################################
