# coding=utf-8

from ...__init__ import _
from ...generics.reports import html_reports
from ...generics.reports import validation_status
from . import article_data_reports


class MergedReports(object):

    def __init__(self, merged):
        self.mgd = merged

    @property
    def consistency_report(self):
        reports = []
        reports += self.report_missing_required_issue_data
        reports += self.report_issue_data_conflicting_values
        reports += self.report_issue_data_duplicated_values

        text = html_reports.tag('h2', _('Checking issue data consistency'))
        text += html_reports.tag('div', ''.join(reports), 'issue-messages')
        return text

    @property
    def journal_issue_header_report(self):
        if not hasattr(self, '_journal_issue_header_report'):
            common_data = ''
            for label, values in self.mgd.common_data.items():
                if len(values.keys()) == 1:
                    common_data += html_reports.tag('p', html_reports.display_label_value(label, list(values.keys())[0]))
                else:
                    common_data += html_reports.format_list(label + ':', 'ol', values.keys())
            self._journal_issue_header_report = html_reports.tag('h2', _('Data in the XML Files')) + html_reports.tag('div', common_data, 'issue-data')
        return self._journal_issue_header_report

    @property
    def report_missing_required_issue_data(self):
        if not hasattr(self, '_report_missing_required_issue_data'):
            r = ''
            for label, items in self.mgd.missing_required_data.items():
                r += html_reports.tag('div', html_reports.p_message(_('{status}: missing {label} in: ').format(status=validation_status.STATUS_BLOCKING_ERROR, label=label)))
                r += html_reports.tag('div', html_reports.format_list('', 'ol', items, 'issue-problem'))
            self._report_missing_required_issue_data = r
        return self._report_missing_required_issue_data

    @property
    def report_issue_data_conflicting_values(self):
        if not hasattr(self, '_report_issue_data_conflicting_values'):
            parts = []
            for label, values in self.mgd.conflicting_values.items():
                _status = validation_status.STATUS_BLOCKING_ERROR
                if self.mgd.is_rolling_pass or self.mgd.is_aop_issue:
                    _status = validation_status.STATUS_WARNING
                elif label == 'license':
                    _status = validation_status.STATUS_WARNING
                _m = _('{status}: same value for {label} is required for all the documents in the package. ').format(status=_status, label=label)
                parts.append(html_reports.p_message(_m))
                parts.append(html_reports.tag('div', html_reports.format_html_data(values), 'issue-problem'))
            self._report_issue_data_conflicting_values = ''.join(parts)
        return self._report_issue_data_conflicting_values

    @property
    def report_issue_data_duplicated_values(self):
        if not hasattr(self, '_report_issue_data_duplicated_values'):
            parts = []
            for label, values in self.mgd.duplicated_values.items():
                status = self.mgd.ERROR_LEVEL_FOR_UNIQUE_VALUES[label]
                _m = _('Unique value for {label} is required for all the documents in the package').format(label=label)
                parts.append(html_reports.p_message(status + ': ' + _m))
                for value, xml_files in values.items():
                    parts.append(html_reports.format_list(_('found {label}="{value}" in:').format(label=label, value=value), 'ul', xml_files, 'issue-problem'))
            self._report_issue_data_duplicated_values = ''.join(parts)
        return self._report_issue_data_duplicated_values

    @property
    def report_issue_page_values(self):
        # FIXME separar validacao e relatório
        if not hasattr(self, '_report_issue_page_values'):
            results = []
            previous = None

            error_level = validation_status.STATUS_BLOCKING_ERROR
            fpage_and_article_id_other_status = [all([a.fpage, a.lpage, a.article_id_other]) for xml_name, a in self.mgd.articles]
            if all(fpage_and_article_id_other_status):
                error_level = validation_status.STATUS_ERROR

            for xml_name, article in self.mgd.articles:
                msg = []
                status = ''
                if article.pages == '':
                    msg.append(_('no pagination was found. '))
                    if not article.is_ahead:
                        status = validation_status.STATUS_ERROR
                if all([article.fpage_number, article.lpage_number]):
                    if previous is not None:
                        if previous.lpage_number > article.fpage_number:
                            status = error_level if not article.is_epub_only else validation_status.STATUS_WARNING
                            msg.append(_('Invalid value for fpage and lpage. Check lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous.prefix, xml_name=xml_name, lpage=previous.lpage, fpage=article.fpage))
                        elif previous.lpage_number + 1 < article.fpage_number:
                            status = validation_status.STATUS_WARNING
                            msg.append(_('There is a gap between lpage={lpage} ({previous_article}) and fpage={fpage} ({xml_name}). ').format(previous_article=previous.prefix, xml_name=xml_name, lpage=previous.lpage, fpage=article.fpage))
                        if previous.fpage_number == article.fpage_number:
                            if all([previous.fpage_seq, article.fpage_seq]) is False:
                                msg.append(_('Same value for fpage={fpage} ({previous_article} and {xml_name}) requires @seq for both fpage. ').format(previous_article=previous.prefix, xml_name=xml_name, lpage=previous.fpage, fpage=article.fpage))
                            elif previous.fpage_seq > article.fpage_seq:
                                msg.append(_('fpage/@seq must be a and b: {a} ({previous_article}) and {b} ({xml_name}). ').format(previous_article=previous.prefix, xml_name=xml_name, a=previous.fpage_seq, b=article.fpage_seq))
                    if article.fpage_number > article.lpage_number:
                        status = error_level
                        msg.append(_('Invalid page range: {fpage} (fpage) > {lpage} (lpage). '.format(fpage=article.fpage_number, lpage=article.lpage_number)))
                    previous = article

                #dates = '|'.join([item if item is not None else 'none' for item in [article.epub_ppub_dateiso, article.collection_dateiso, article.epub_dateiso]])
                msg = '\n'.join(msg)
                results.append({'label': xml_name, 'status': status, 'pages': article.pages, 'message': msg, _('why it is not a valid message?'): ''})
            self._report_issue_page_values = html_reports.tag('h2', _('Pages Report')) + html_reports.tag('div', html_reports.sheet(['label', 'status', 'pages', 'message', _('why it is not a valid message?')], results, table_style='validation_sheet', widths={'label': '10', 'status': '10', 'pages': '5', 'message': '75'}))
        return self._report_issue_page_values


class MergenceReports(object):

    def __init__(self, mergence):
        self.mergence = mergence

    def report_articles_merging_conflicts(self):
        if not hasattr(self, '_report_articles_merging_conflicts'):
            merging_errors = []
            if len(self.mergence.results_titaut_conflicts) + len(self.mergence.results_name_order_conflicts) > 0:

                keys = list(self.mergence.results_titaut_conflicts.keys()) + list(self.mergence.results_name_order_conflicts.keys())
                keys = sorted(list(set(keys)))

                merging_errors = [html_reports.p_message(validation_status.STATUS_BLOCKING_ERROR + ': ' + _('Unable to update because the registered article data and the package article data do not match. '))]

                articles = self.mergence.articles
                registered_articles = self.mergence.registered_articles
                for name in keys:
                    labels = [name, _('title/author conflicts'), _('name/order conflicts')]
                    values = [article_data_reports.display_article_data_to_compare(articles.get(name))]

                    articles_in_conflict = []
                    for reg_name, art in self.mergence.results_titaut_conflicts.get(name, {}).items():
                        articles_in_conflict.append(article_data_reports.display_article_data_to_compare(art))
                    values.append(''.join(articles_in_conflict))

                    articles_in_conflict = []
                    for pkg_name, art in self.mergence.results_name_order_conflicts.get(name, {}).items():
                        articles_in_conflict.append(article_data_reports.display_article_data_to_compare(art))
                    values.append(''.join(articles_in_conflict))

                    merging_errors.append(html_reports.sheet(labels, [html_reports.label_values(labels, values)], table_style='dbstatus', html_cell_content=labels))
            self._report_articles_merging_conflicts = ''.join(merging_errors)
        return self._report_articles_merging_conflicts

    def report_articles_order_conflicts(self):
        if not hasattr(self, '_report_articles_order_conflicts'):
            r = []
            if len(self.mergence.pkg_order_conflicts) > 0:
                html_reports.tag('h2', _('Order conflicts'))
                for order, names in self.mergence.pkg_order_conflicts.items():
                    r.append(html_reports.tag('h3', order))
                    r.append(html_reports.format_html_data(names))
            self._report_articles_order_conflicts = ''.join(r)
        return self._report_articles_order_conflicts

    @property
    def report_articles_changed_names(self):
        if not hasattr(self, '_report_articles_changed_names'):
            r = []
            if len(self.mergence.results_name_changes) > 0:
                r.append(html_reports.tag('h3', _('Names changes')))
                for old, new in self.mergence.results_name_changes.items():
                    r.append(html_reports.tag('p', '{old} => {new}'.format(old=old, new=new), 'info'))
            self._report_articles_changed_names = ''.join(r)
        return self._report_articles_changed_names

    @property
    def report_articles_changed_orders(self):
        if not hasattr(self, '_report_articles_changed_orders'):
            r = []
            if len(self.mergence.results_order_changes) > 0:
                r.append(html_reports.tag('h3', _('Orders changes')))
                for name, changes in self.mergence.results_order_changes.items():
                    r.append(html_reports.tag('p', '{name}: {old} => {new}'.format(name=name, old=changes[0], new=changes[1]), 'info'))
            if len(self.mergence.results_excluded_orders) > 0:
                r.append(html_reports.tag('h3', _('Orders exclusions')))
                for name, order in self.mergence.results_excluded_items.items():
                    r.append(html_reports.tag('p', '{order} ({name})'.format(name=name, order=order), 'info'))
            self._report_articles_changed_orders = ''.join(r)
        return self._report_articles_changed_orders

    @property
    def report_articles_data_changes(self):
        if not hasattr(self, '_report_articles_data_changes'):
            r = ''
            r += self.report_articles_changed_orders
            r += self.report_articles_changed_names
            if len(r) > 0:
                r = html_reports.tag('h2', _('Changes Report')) + r
            self._report_articles_data_changes = r
        return self._report_articles_data_changes

    @property
    def report_articles_data_conflicts(self):
        if not hasattr(self, '_report_articles_data_conflicts'):
            self._report_articles_data_conflicts = ''
            r = ''.join([self.report_articles_order_conflicts() + self.report_articles_merging_conflicts()])
            if len(r) > 0:
                self._report_articles_data_conflicts = html_reports.tag('h2', _('Data Conflicts Report')) + r
        return self._report_articles_data_conflicts
