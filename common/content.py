#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'bp'
__version__ = (0, 0, 1)

from fields import MD5Field, FilenameField

################################################################################
class File(object):
    """
    Объект файла

    >>> with open('./filename.txt', 'w') as f:
    ...     f.write('1')
    ...     f.close()
    >>> a = File('filename.txt', 'c4ca4238a0b923820dcc509a6f75849b')
    >>> a.filename
    'filename.txt'
    >>> a.md5sum
    'c4ca4238a0b923820dcc509a6f75849b'
    >>> a.filepath()
    './filename.txt'
    >>> import os
    >>> os.unlink('./filename.txt')
    """

    md5sum = MD5Field()
    filename = FilenameField()

    def __init__(self, filename, md5, root=None):
        self.root = root or '.'
        self.filename = filename
        self.md5sum = md5


    def filepath(self):
        return '{}/{}'.format(self.root, self.filename)


# end of class FileField(BaseField)
################################################################################