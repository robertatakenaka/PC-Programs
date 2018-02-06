# coding=utf-8

from ...__init__ import TABLES_PATH

from ...generics.fs_utils import read_file


PERMISSION_ELEMENTS = [
    'license',
    'copyright-holder',
    'copyright-year',
    'copyright-statement',
    ]

LICENSES = read_file(TABLES_PATH + '/licenses.csv')
if LICENSES is None:
    LICENSES = []
else:
    LICENSES = LICENSES.split()
