# coding=utf-8

from ...__init__ import _
from ...generics import utils
from ...generics.reports import html_reports
from ...generics.reports import validation_status


class ArticlesComparison(object):

    def __init__(self, article1, article2, ign_name=False, ign_order=False):
        self.article1 = article1
        self.article2 = article2
        self.ign_name = ign_name
        self.ign_order = ign_order
        self.exact_comparison_result = None
        self.relaxed_comparison_result = None
        self.compare_articles()

    def compare_articles(self):
        self.exact_comparison_result = []
        self.relaxed_comparison_result = []
        if self.article1 is not None and self.article2 is not None:
            relaxed_labels = [_('titles'), _('authors')]
            relaxed_data = []
            relaxed_data.append((normalize_text(self.article1.textual_titles), normalize_text(self.article2.textual_titles)))
            relaxed_data.append((display_authors(self.article1.article_contrib_items, '; '), display_authors(self.article2.article_contrib_items, '; ')))

            if not any([self.article1.textual_titles, self.article2.textual_titles, self.article1.textual_contrib_surnames, self.article2.textual_contrib_surnames]):
                if self.article1.body_words is not None and self.article2.body_words is not None:
                    relaxed_labels.append(_('body'))
                    relaxed_data.append((self.article1.body_words[0:200], self.article2.body_words[0:200]))

            exact_labels = [_('doi')]
            exact_data = []
            if self.ign_order is False:
                exact_labels.append(_('order'))
                exact_data.append((self.article1.order, self.article2.order))
            if self.ign_name is False:
                exact_labels.append(_('name'))
                exact_data.append((self.article1.prefix, self.article2.prefix))
            exact_data.append((self.article1.doi, self.article2.doi))
            exact_data.extend(relaxed_data)
            exact_labels.extend(relaxed_labels)
            self.exact_comparison_result = [(label, items) for label, items in zip(exact_labels, exact_data) if not items[0] == items[1]]
            self.relaxed_comparison_result = [(label, items) for label, items in zip(relaxed_labels, relaxed_data) if not utils.is_similar(items[0], items[1])]

    @property
    def status(self):
        _status = validation_status.STATUS_BLOCKING_ERROR
        if len(self.exact_comparison_result) == 0:
            _status = validation_status.STATUS_INFO
        elif len(self.exact_comparison_result) == 1 and len(self.relaxed_comparison_result) in [0, 1]:
            _status = validation_status.STATUS_WARNING
        return _status

    @property
    def are_similar(self):
        return self.status in [validation_status.STATUS_INFO, validation_status.STATUS_WARNING]

    def display_articles_differences(self):
        comparison_result = self.exact_comparison_result
        msg = []
        if len(comparison_result) > 0:
            msg.append(html_reports.p_message(self.status))
            for label, differences in comparison_result:
                diff = [differences[0], differences[1]]
                diff = '&#160;=>&#160;'.join([d for d in diff if d is not None])
                msg.append(html_reports.tag('p', diff))
        return ''.join(msg)


