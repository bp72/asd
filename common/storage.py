#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'bp'
__version__ = (0, 0, 1)


import os
import hashlib
from content import File


################################################################################
class BaseStorage(object):
    """
    Базвый класс Хранилища.
    Ничего не умеет
    """

    maxfile = 0

    class FileExists(Exception):
        def __init__(self, filename):
            self.message = u'Файл уже присутвует в хранилище: {}'.format(filename)


    class FileNotFound(Exception):
        def __init__(self, filename):
            self.message = u'Файл не найден в хранилище: {}'.format(filename)


    class FileDuplicate(Exception):
        def __init__(self, filename):
            self.message = u'Опаньки! Как так случилось, что файлов больше 1го: {}'.format(filename)


    class FileLimitExceeded(Exception):
        def __init__(self, filename):
            self.message = u'Опаньки! Как так случилось, что файлов больше 1го: {}'.format(filename)


    def store_file(self, content):
        raise NotImplementedError


    def add_filepath(self, user, filepath):
        self.add_file(user, os.path.basename(filepath), open(filepath, 'rb').read())


    def add_files(self, user, filepath_set):
        for filepath in filepath_set:
            self.add_filepath(user, filepath)


    def remove_from_index(self, user, alias):
        """
        Удаление файла из индекса
        :param user:
        :param alias:
        :return:
        """
        raise NotImplementedError


    def __delete_file(self, md5):
        """
        Удаление файла из хранилища.
        Удаление происходит только в том, случае, если
        в индексе нет ни одной ссылки на файл
        :param md5:
        :return:
        """
        if self.refcount(md5) == 0:
            os.unlink('{}/{}'.format(self.root, md5))


    def del_file(self, user, alias):
        """
        Удаление файла из хранилища.
        Процедура для пользователя.
        :param user: str
        :param alias: str
        :return: None
        """
        file = self.findfile(user, alias)
        if file is None:
            raise self.FileNotFound(alias)
        if not isinstance(file, File):
            raise self.FileDuplicate(alias)
        self.remove_from_index(user, alias)
        self.delete_file(file.md5sum)


    def delete_files(self, user, alias_set):
        for alias in alias_set:
            self.__del_file(user, alias)


    def add_file(self, user, filename, file_content):
        """
        Добавление файла в хранилище
        :param user: str, владелец
        :param filename: str, пользовательское имя файла
        :param file_content: str, содержимое файла
        :return: None
        """
        md5 = hashlib.md5(file_content).hexdigest()
        if self.file_exists(user, md5, filename):
            raise self.FileExists(filename)
        if len(list(self.list(user))) >= self.maxfile:
            raise self.FileLimitExceeded(filename)
        self.store_file(file_content, md5)
        self.store_index(user, filename, md5)


    def list(self, user=None):
        raise NotImplementedError


    def findfile(self, user=None, alias=None):
        """
        Поиск индексу.
        Если файл не найден, возвращает None
        Если найден один файл, возвращает File object
        Если найдено два и более файлов, возвращает спискок
        """
        result = filter(lambda item: item.filename == alias, self.list(user))
        if len(result) == 1:
            return result[0]
        return result


    def refcount(self, md5):
        """
        Посчет количества ссылок на физический файл.
        Возвращает int
        """
        refs = filter(lambda item: item.md5sum == md5, self.list())
        if not refs:
            return 0
        return len(refs)


    def file_exists(self, user, md5, alias):
        return True if filter(lambda item: item.md5sum == md5 and item.filename == alias, self.list(user)) else False

# end of class BaseStorage(object)
################################################################################


################################################################################
class IndexFileStorage(BaseStorage):
    """
    Хранилище с файлом-индексом

    >>> ifs = IndexFileStorage()
    >>> ifs.reset_index()
    >>> ifs.add_file('bp', 'filename.txt', '1')
    >>> ifs.add_file('bp', 'filename.txt', '1') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    FileExists
    >>> ifs.file_exists('bp', 'c4ca4238a0b923820dcc509a6f75849b', 'filename.txt')
    True
    >>> ifs.file_exists('bp', 'c4ca4238a0b923820dcc509a6f75849b', 'filename1.txt')
    False
    >>> ifs.list().next().filename
    'filename.txt'
    >>> ifs.add_file('bp', 'filename2.txt', '1')
    >>> ifs.add_file('bp', 'filename2.txt', '1')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    FileExists
    >>> ifs.file_exists('bp', 'c4ca4238a0b923820dcc509a6f75849b', 'filename2.txt')
    True
    >>> ifs.add_file('mark', 'mark_cv.txt', '22')
    >>> ifs.del_file('bp', 'filename2.txt')
    >>> ifs.del_file('bp', 'filename.txt')
    >>> ifs.add_file('bp', 'filename.txt', '1')
    >>> ifs.add_file('bp', 'filename2.txt', '1')
    >>> for i in xrange(100):
    ...     ifs.add_file('bp', 'filename{}.txt'.format(i + 3), '{}'.format(i/10)) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    FileLimitExceeded
    >>> for i in xrange(100):
    ...     ifs.add_file('masha', 'filename{}.txt'.format(i + 3), '{}'.format(i/10)) # doctest: +ELLIPSIS
    """
    root = '/home/bp/work/cloud/storage'
    index_filename = '.index'
    index_file = '{}/{}'.format(root, index_filename)
    maxfile = 100


    def reset_index(self):
        """
        Сброс индекса
        :return: None
        """
        with open(self.index_file, 'w') as index:
            index.close()


    def store_file(self, content, md5):
        """
        Сохранение файла в хранилище
        :param content: str, тело файла
        :param md5: str
        :return: None
        """
        filepath = '{}/{}'.format(self.root, md5)
        if os.path.exists(filepath):
            return None
        with open(filepath, 'wb') as userfile:
            userfile.write(content)
            userfile.close()


    def delete_file(self, md5):
        """
        Удаление файла из хранилища.
        Удаление происходит только в том, случае, если
        в индексе нет ни одной ссылки на файл
        :param md5:
        :return:
        """
        if self.refcount(md5) == 0:
            os.unlink('{}/{}'.format(self.root, md5))


    def remove_from_index(self, user, alias):
        """
        Удаление файла из индекса
        :param user: str
        :param alias: str
        :return: None
        """
        file = self.findfile(user, alias)
        if not file:
            raise self.FileNotFound(alias)
        if not isinstance(file, File):
            raise self.FileDuplicate(alias)
        original = open(self.index_file, 'r').readlines()
        with open(self.index_file, 'w') as new:
            for line in original:
                if line.strip().endswith('{}|{}'.format(user, alias)):
                    continue
                new.write(line)
            new.close()


    def store_index(self, user, filename, md5):
        """
        Обновить индекс
        :param user: str, владелец
        :param filename: str, пользовательское имя файла
        :param md5: str, содержимое файла
        :return: None
        """
        with open(self.index_file, 'a') as index:
            index.write('{}|{}|{}\n'.format(md5, user, filename))
            index.close()


    def list(self, user=None):
        """
        Список пользовательских файлов в хранилище
        :param user: str
        :return: generator
        """
        if not os.path.exists(self.index_file):
            self.reset_index()
        with open(self.index_file, 'r') as index:
            for line in index:
                (md5, owner, filename) = line.strip().split('|')
                if user is not None and user != owner:
                    continue
                yield File(filename, md5, self.root)


# end of class IndexFileStorage(BaseStorage)
################################################################################


if __name__ == '__main__':
    import doctest
    doctest.testmod()