# coding=utf-8

from unittest import TestCase
from app_modules.generics.dbm.dbm_isis import IDFile

import sys
python_version = sys.version_info.major


class TestIDFile(TestCase):

    def setUp(self):
        self.idfile = IDFile()
        print(python_version)

    def test_tag_content_returns_tagged_content(self):
        if python_version < 3:
            return self.assertEqual(
                self.idfile.tag_content("300", u"blá"),
                u"!v300!blá\n"
            )

        self.assertEqual(
            self.idfile.tag_content("300", "blá"),
            "!v300!blá\n"
        )

    def test_tag_content_does_not_return(self):
        if python_version < 3:
            return self.assertEqual(
                self.idfile.tag_content("1300", u"blá"),
                ""
            )

        self.assertEqual(
            self.idfile.tag_content("1300", "blá"),
            ""
        )

