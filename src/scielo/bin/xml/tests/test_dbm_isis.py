# coding=utf-8

from unittest import TestCase, skip
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
                ""
            )
        return self.assertEqual(
            self.idfile.format_subfield("", "blá"),
            ""
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
                self.idfile.format_subfield("x", "Ü ^ b"),
                "^xÜ [PRESERVECIRC] b"
            )
        return self.assertEqual(
            self.idfile.format_subfield("x", "Ü ^ b"),
            "^xÜ [PRESERVECIRC] b"
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

    def test_format_subfields_returns_one_value_and_two_subfields(self):
        if python_version < 3:
            subf_and_values = [
                ("a", u"blá"),
                ("_", u"clá"),
                ("3", u"dlá"),
            ]
            expected = u"clá^3dlá^ablá"
        else:
            subf_and_values = [
                ("a", "blá"),
                ("_", "clá"),
                ("3", "dlá"),
            ]
            expected = "clá^3dlá^ablá"

        result = self.idfile.format_subfields(dict(subf_and_values))
        self.assertEqual(result, expected)

    def test_format_subfields_returns_two_subfields(self):
        if python_version < 3:
            subf_and_values = [
                ("a", u"blá"),
                ("3", u"dlá"),
            ]
            expected = u"^3dlá^ablá"
        else:
            subf_and_values = [
                ("a", "blá"),
                ("3", "dlá"),
            ]
            expected = "^3dlá^ablá"

        result = self.idfile.format_subfields(dict(subf_and_values))
        self.assertEqual(result, expected)

    def test_format_subfields_ignore_invalid_subfield_and_value(self):
        if python_version < 3:
            subf_and_values = [
                ("a", u"blá"),
                ("b", u"clá"),
                ("", u"clá"),
                ("_", u""),
                ("3", u"dlá"),
            ]
            expected = u"^3dlá^ablá^bclá"
        else:
            subf_and_values = [
                ("a", "blá"),
                ("b", "clá"),
                ("", "clá"),
                ("_", ""),
                ("3", "dlá"),
            ]
            expected = "^3dlá^ablá^bclá"

        result = self.idfile.format_subfields(dict(subf_and_values))
        self.assertEqual(result, expected)

    def test__format_id_returns_ID_6digits(self):
        self.assertEqual("!ID 000312\n", self.idfile._format_id(312))

    def test__format_id_returns_none(self):
        self.assertIsNone(self.idfile._format_id(""))

    def test__format_id_returns_none_for_input_greater_than_6digits(self):
        self.assertIsNone(self.idfile._format_id("123456789"))

    def test__format_id_returns_ID999999(self):
        self.assertEqual("!ID 999999\n", self.idfile._format_id("999999"))

    def test__format_id_returns_ID000001(self):
        self.assertEqual("!ID 000001\n", self.idfile._format_id("1"))

    def test__format_record_returns_(self):
        if python_version < 3:
            inputs = [
                ("103", 
                    [
                        {"_": "valor\nG", "a": u"ãçá"},
                        {"_": "valor A", "a": u"ãçá"},
                        {"_": "valor B", "a": u"ãçá"},
                        {"_": "valor C", "a": u"ãçá"}
                    ]
                ),
                ("102", 
                    [
                        {"1": u"ãçá", "x": "subcampo\nA"},
                        {"1": u"ãçá", "y": "subcampo A"},
                        {"1": u"ãçá", "z": "subcampo A"},
                    ]
                ),
                ("1", "valor\n1"),
                ("2", {"a": u"ãçá", "b": "subcampo b", "1": "subcampo 1"}),
                ("3", {"_": "valor", "a": u"ãçá", "1": "subcampo 1"}),
                ("4",
                    [
                        {"_": "campo 4, ocorrencia 1"},
                        {"_": "campo 4, ocorrencia 2"},
                        {"_": "campo 4, ocorrencia 3"},
                    ]
                )
            ]

            values = [
                u"!v001!valor 1",
                u"!v002!^1subcampo 1^aãçá^bsubcampo b",
                u"!v003!valor^1subcampo 1^aãçá",
                u"!v004!campo 4, ocorrencia 1",
                u"!v004!campo 4, ocorrencia 2",
                u"!v004!campo 4, ocorrencia 3",
                u"!v102!^1ãçá^xsubcampo A",
                u"!v102!^1ãçá^ysubcampo A",
                u"!v102!^1ãçá^zsubcampo A",
                u"!v103!valor G^asubcampo a",
                u"!v103!valor A^asubcampo a",
                u"!v103!valor B^asubcampo a",
                u"!v103!valor C^asubcampo a"
            ]    
        inputs = [
            ("103", 
                [
                    {"_": "valor G", "a": "subcampo a"},
                    {"_": "valor\nA", "a": "subcampo a"},
                    {"_": "valor B", "a": "subcampo a"},
                    {"_": "valor C", "a": "subcampo a"}
                ]
            ),
            ("102", 
                [
                    {"1": "subcampo\na", "x": "subcampo A"},
                    {"1": "subcampo a", "y": "subcampo A"},
                    {"1": "subcampo a", "z": "subcampo A"},
                ]
            ),
            ("1", "valor\n1"),
            ("2", {"a": "subcampo a", "b": "subcampo b", "1": "subcampo 1"}),
            ("3", {"_": "valor", "a": "subcampo a", "1": "subcampo 1"}),
            ("4",
                [
                    {"_": "campo 4, ocorrencia 1"},
                    {"_": "campo 4, ocorrencia 2"},
                    {"_": "campo 4, ocorrencia 3"},
                ]
            )
        ]

        values = [
            "!v001!valor 1",
            "!v002!^1subcampo 1^asubcampo a^bsubcampo b",
            "!v003!valor^1subcampo 1^asubcampo a",
            "!v004!campo 4, ocorrencia 1",
            "!v004!campo 4, ocorrencia 2",
            "!v004!campo 4, ocorrencia 3",
            "!v102!^1subcampo a^xsubcampo A",
            "!v102!^1subcampo a^ysubcampo A",
            "!v102!^1subcampo a^zsubcampo A",
            "!v103!valor G^asubcampo a",
            "!v103!valor A^asubcampo a",
            "!v103!valor B^asubcampo a",
            "!v103!valor C^asubcampo a"
        ]

        self.assertEqual(
            "\n".join(values)+"\n",
            self.idfile._format_record(dict(inputs))
        )

