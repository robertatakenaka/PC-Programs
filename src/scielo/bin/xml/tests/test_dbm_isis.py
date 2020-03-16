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

    def test_format_subfield_returns_subfield_and_value(self):
        if python_version < 3:
            return self.assertEqual(
                self.idfile.format_subfield("a", u"blá"),
                u"^ablá"
            )
        return self.assertEqual(
            self.idfile.format_subfield("a", "blá"),
            "^ablá"
        )

    def test_format_subfield_returns_only_value(self):
        if python_version < 3:
            return self.assertEqual(
                self.idfile.format_subfield("", u"blá"),
                u"blá"
            )
        return self.assertEqual(
            self.idfile.format_subfield("", "blá"),
            "blá"
        )

    def test_format_subfield_returns_empty_str(self):
        if python_version < 3:
            return self.assertEqual(
                self.idfile.format_subfield("", None),
                ""
            )
        return self.assertEqual(
            self.idfile.format_subfield("", None),
            ""
        )

    def test_format_subfield_preserve_circ(self):
        if python_version < 3:
            return self.assertEqual(
                self.idfile.format_subfield("", "Ü ^ b"),
                "Ü [PRESERVECIRC] b"
            )
        return self.assertEqual(
            self.idfile.format_subfield("", "Ü ^ b"),
            "Ü [PRESERVECIRC] b"
        )

    def test_format_subfield_creates_subfield_and_preserve_circ(self):
        if python_version < 3:
            return self.assertEqual(
                self.idfile.format_subfield("1", "a ^ b"),
                "^1a [PRESERVECIRC] b"
            )
        return self.assertEqual(
            self.idfile.format_subfield("1", "a ^ b"),
            "^1a [PRESERVECIRC] b"
        )

    def test_format_subfield_creates_subfield_and_supress_extra_spaces(self):
        if python_version < 3:
            return self.assertEqual(
                self.idfile.format_subfield("1", "         a ^ b"),
                "^1a [PRESERVECIRC] b"
            )
        return self.assertEqual(
            self.idfile.format_subfield("1", "        a ^ b"),
            "^1a [PRESERVECIRC] b"
        )

    def test_format_subfield_creates_subfield_and_supress_breaks(self):
        if python_version < 3:
            return self.assertEqual(
                self.idfile.format_subfield("1", """
                         a ^ b"""),
                "^1a [PRESERVECIRC] b"
            )
        return self.assertEqual(
            self.idfile.format_subfield("1", """
                         a ^ b"""),
            "^1a [PRESERVECIRC] b"
        )
