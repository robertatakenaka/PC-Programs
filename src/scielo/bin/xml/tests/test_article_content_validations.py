import unittest

from app_modules.__init__ import _
from app_modules.app.validations import article_content_validations
from app_modules.generics.reports import validation_status


class Object(object):

    def __init__(self):
        pass


class ArticleHistoryValidationTest(unittest.TestCase):

    def setUp(self):
        _article = Object()
        _article.received_dateiso = None
        _article.accepted_dateiso = None
        _article.article_type = None

        self.article_history_validation = article_content_validations.ArticleHistoryValidation(
            _article)

    def update(self, received, accepted, article_type):
        self.article_history_validation.article.received_dateiso = received
        self.article_history_validation.article.accepted_dateiso = accepted
        self.article_history_validation.article.article_type = article_type

    @property
    def error_level(self):
        if self.article_history_validation.article.article_type == 'editorial':
            return validation_status.STATUS_INFO
        return validation_status.STATUS_FATAL_ERROR

    def test_article_history_none(self):
        self.update(None, None, 'case-report')
        expected = [(
                        'history',
                        self.error_level,
                        _('Not found: {label}. ').format(label='history'))]

        self.assertListEqual(
            self.article_history_validation.validate(),
            expected)

    def test_text_history_none(self):
        self.update(None, None, 'editorial')
        expected = [(
                        'history',
                        self.error_level,
                        _('Not found: {label}. ').format(label='history'))]

        self.assertListEqual(
            self.article_history_validation.validate(),
            expected)

    def test_article_history_received_only(self):
        self.update('', None, 'case-report')
        label = 'history: accepted'
        expected = [(
                        label,
                        self.error_level,
                        _('{label} is required. ').format(label=label))]

        self.assertListEqual(
            self.article_history_validation.validate(),
            expected)

    def test_text_history_received_only(self):
        self.update('', None, 'editorial')
        label = 'history: accepted'
        expected = [(
                        label,
                        self.error_level,
                        _('{label} is required. ').format(label=label))]

        self.assertListEqual(
            self.article_history_validation.validate(),
            expected)

    def test_article_history_accepted_only(self):
        self.update(None, '', 'case-report')
        self.article_history_validation.article.received_dateiso = None
        self.article_history_validation.article.accepted_dateiso = ''
        self.article_history_validation.article.article_type = 'case-report'
        label = 'history: received'
        expected = [(
                        label,
                        self.error_level,
                        _('{label} is required. ').format(label=label))]

        self.assertListEqual(
            self.article_history_validation.validate(),
            expected)

    def test_text_history_accepted_only(self):
        self.update(None, '', 'editorial')
        label = 'history: received'
        expected = [(
                        label,
                        self.error_level,
                        _('{label} is required. ').format(label=label))]

        self.assertListEqual(
            self.article_history_validation.validate(),
            expected)

    def test_article_history(self):
        self.update('', '', 'case-report')
        dateiso = ''
        result = []

        for label in ['received', 'accepted']:
            parts = []
            parts.append((0, 'year (' + label + ')'))
            parts.append((0, 'month (' + label + ')'))
            parts.append((0, 'day (' + label + ')'))

            for part, part_label in parts:
                msg = '{}: {}. '.format(label, dateiso)
                msg += _('{value} is an invalid value for {label}. ').format(
                            value=part, label=part_label)
                result.append(msg)

        expected = [(
                        'history',
                        self.error_level,
                        '\n'.join(result))]

        self.assertListEqual(
            self.article_history_validation.validate(),
            expected)

    def test_text_history(self):
        self.update('', '', 'editorial')
        label = 'history'
        expected = [(
                        label,
                        self.error_level,
                        _('{label} is required. ').format(label=label))]

        self.assertListEqual(
            self.article_history_validation.validate(),
            expected)


if __name__ == '__main__':
    unittest.main()
