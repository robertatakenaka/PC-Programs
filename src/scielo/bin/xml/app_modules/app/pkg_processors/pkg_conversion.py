# coding=utf-8

import os
import shutil

from ...__init__ import _

from ...generics import encoding
from ...generics.reports import html_reports
from ...generics.reports import validation_status
from ..validations import article_data_reports
from ..validations import validations as validations_module


EMAIL_SUBJECT_STATUS_ICON = {}
EMAIL_SUBJECT_STATUS_ICON['rejected'] = [u"\u274C", _(' REJECTED ')]
EMAIL_SUBJECT_STATUS_ICON['ignored'] = ['', _('IGNORED')]
EMAIL_SUBJECT_STATUS_ICON['accepted'] = [u"\u2713" + ' ' + u"\u270D", _(' ACCEPTED but corrections required ')]
EMAIL_SUBJECT_STATUS_ICON['approved'] = [u"\u2705", _(' APPROVED ')]
EMAIL_SUBJECT_STATUS_ICON['not processed'] = ['', _(' NOT PROCESSED ')]


categories_messages = {
    'converted': _('converted'),
    'rejected': _('rejected'),
    'not converted': _('not converted'),
    'skipped': _('skipped conversion'),
    'excluded ex-aop': _('excluded ex-aop'),
    'excluded incorrect order': _('excluded incorrect order'),
    'not excluded incorrect order': _('not excluded incorrect order'),
    'not excluded ex-aop': _('not excluded ex-aop'),
    'new aop': _('aop version'),
    'regular doc': _('doc has no aop'),
    'ex aop': _('aop is published in an issue'),
    'matched aop': _('doc has aop version'),
    'partially matched aop': _('doc has aop version partially matched (title/author are similar)'),
    'aop missing PID': _('doc has aop version which has no PID'),
    'unmatched aop': _('doc has an invalid aop version (title/author are not the same)'),
}


class PkgConverter(object):

    def __init__(self, registered, pkg, validations_reports, create_windows_base, web_app_path, web_app_site):
        self.create_windows_base = create_windows_base
        self.registered = registered
        self.db = self.registered.articles_db_manager
        self.local_web_app_path = web_app_path
        self.web_app_site = web_app_site
        self.pkg = pkg
        self.validations_reports = validations_reports
        self.articles_mergence = validations_reports.merged_articles_reports.articles_mergence
        self.error_messages = []
        self.conversion_status = {}

    def convert(self):
        self.articles_conversion_validations = validations_module.ValidationsResultItems()
        scilista_items = [self.pkg.issue_data.acron_issue_label]
        if self.validations_reports.blocking_errors == 0 and (self.accepted_articles == len(self.pkg.articles) or len(self.articles_mergence.excluded_orders) > 0):
            self.error_messages = self.db.exclude_articles(self.articles_mergence.excluded_orders)

            _scilista_items = self.db.convert_articles(self.pkg.issue_data.acron_issue_label, self.articles_mergence.accepted_articles, self.registered.issue_models.record, self.create_windows_base)
            scilista_items.extend(_scilista_items)
            self.conversion_status.update(self.db.db_conversion_status)

            for name, message in self.db.articles_conversion_messages.items():
                self.articles_conversion_validations[name] = validations_module.ValidationsResult()
                self.articles_conversion_validations[name].message = message

            if len(_scilista_items) > 0:
                # IMPROVEME
                self.registered.issue_files.copy_files_to_local_web_app(self.pkg.package_folder.path, self.local_web_app_path)
                self.registered.issue_files.save_source_files(self.pkg.package_folder.path)
                self.replace_ex_aop_pdf_files()

        return scilista_items

    @property
    def aop_status(self):
        if self.db is not None:
            return self.db.db_aop_status
        return {}

    def replace_ex_aop_pdf_files(self):
        # IMPROVEME
        encoding.debugging('replace_ex_aop_pdf_files()', self.db.aop_pdf_replacements)
        for xml_name, aop_location_data in self.db.aop_pdf_replacements.items():
            folder, aop_name = aop_location_data

            aop_pdf_path = self.local_web_app_path + '/bases/pdf/' + folder
            if not os.path.isdir(aop_pdf_path):
                os.makedirs(aop_pdf_path)
            issue_pdf_path = self.local_web_app_path + '/bases/pdf/' + self.pkg.issue_data.acron_issue_label.replace(' ', '/')

            issue_pdf_files = [f for f in os.listdir(issue_pdf_path) if f.startswith(xml_name) or f[2:].startswith('_'+xml_name)]

            for pdf in issue_pdf_files:
                aop_pdf = pdf.replace(xml_name, aop_name)
                encoding.debugging('replace_ex_aop_pdf_files()', (issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf))
                shutil.copyfile(issue_pdf_path + '/' + pdf, aop_pdf_path + '/' + aop_pdf)

    @property
    def conversion_report(self):
        #resulting_orders
        labels = [_('registered') + '/' + _('before conversion'), _('package'), _('executed actions'), _('article')]
        widths = {_('article'): '20', _('registered') + '/' + _('before conversion'): '20', _('package'): '20', _('executed actions'): '20'}

        for status, status_items in self.aop_status.items():
            for status_data in status_items:
                if status != 'aop':
                    name = status_data
                    self.articles_mergence.history_items[name].append(status)
        for status, names in self.conversion_status.items():
            for name in names:
                self.articles_mergence.history_items[name].append(status)

        items = []
        db_articles = self.registered_articles or {}
        for xml_name in sorted(self.articles_mergence.history_items.keys()):
            pkg = self.articles_mergence.articles.get(xml_name)
            registered = self.articles_mergence.registered_articles.get(xml_name)
            merged = db_articles.get(xml_name)

            diff = ''
            if registered is not None and pkg is not None:
                comparison = article_data_reports.ArticlesComparison(registered, pkg)
                diff = comparison.display_articles_differences()
                if diff != '':
                    diff += '<hr/>'

            values = []
            values.append(article_data_reports.display_article_data_to_compare(registered) if registered is not None else '')
            values.append(article_data_reports.display_article_data_to_compare(pkg) if pkg is not None else '')
            values.append(article_data_reports.article_history(self.articles_mergence.history_items[xml_name]))
            values.append(diff + article_data_reports.display_article_data_to_compare(merged) if merged is not None else '')

            items.append(html_reports.label_values(labels, values))
        return html_reports.tag('h3', _('Conversion steps')) + html_reports.sheet(labels, items, html_cell_content=[_('article'), _('registered') + '/' + _('before conversion'), _('package'), _('executed actions')], widths=widths)

    @property
    def registered_articles(self):
        if self.db is not None:
            return self.db.registered_articles

    @property
    def acron_issue_label(self):
        return self.pkg.issue_data.acron_issue_label

    @property
    def accepted_articles(self):
        return len(self.articles_mergence.accepted_articles)

    @property
    def total_converted(self):
        return len(self.conversion_status.get('converted', []))

    @property
    def total_not_converted(self):
        return len(self.conversion_status.get('not converted', []))

    @property
    def xc_status(self):
        if self.validations_reports.blocking_errors > 0:
            result = 'rejected'
        elif self.accepted_articles == 0 and len(self.articles_mergence.excluded_orders) == 0:
            result = 'ignored'
        elif self.articles_conversion_validations.blocking_errors > 0:
            result = 'rejected'
        elif self.articles_conversion_validations.fatal_errors > 0:
            result = 'accepted'
        else:
            result = 'approved'
        return result

    @property
    def conversion_status_report(self):
        title = _('Conversion results')
        status = self.conversion_status
        style = 'conversion'
        text = ''
        if status is not None:
            for category in sorted(status.keys()):
                _style = style
                if status.get(category) is None:
                    ltype = 'ul'
                    list_items = ['None']
                    _style = None
                elif len(status[category]) == 0:
                    ltype = 'ul'
                    list_items = ['None']
                    _style = None
                else:
                    ltype = 'ol'
                    list_items = status[category]
                text += html_reports.format_list(categories_messages.get(category, category), ltype, list_items, _style)
        if len(text) > 0:
            text = html_reports.tag('h3', title) + text
        return text

    @property
    def aop_status_report(self):
        if len(self.aop_status) == 0:
            return _('this journal has no aop. ')
        r = ''
        for status in sorted(self.aop_status.keys()):
            if status != 'aop':
                r += self.aop_report(status, self.aop_status[status])
        r += self.aop_report('aop', self.aop_status.get('aop'))
        return r

    def aop_report(self, status, status_items):
        if status_items is None:
            return ''
        r = ''
        if len(status_items) > 0:
            labels = []
            widths = {}
            if status == 'aop':
                labels = [_('issue')]
                widths = {_('issue'): '5'}
            labels.extend([_('filename'), 'order', _('article')])
            widths.update({_('filename'): '5', 'order': '2', _('article'): '88'})

            report_items = []
            for item in status_items:
                issueid = None
                article = None
                if status == 'aop':
                    issueid, name, article = item
                else:
                    name = item
                    article = self.articles_mergence.merged_articles.get(name)
                if article is not None:
                    if not article.is_ex_aop:
                        values = []
                        if issueid is not None:
                            values.append(issueid)
                        values.append(name)
                        values.append(article.order)
                        values.append(article.title)
                        report_items.append(html_reports.label_values(labels, values))
            r = html_reports.tag('h3', _(status)) + html_reports.sheet(labels, report_items, table_style='reports-sheet', html_cell_content=[_('article')], widths=widths)
        return r

    @property
    def conclusion_message(self):
        text = ''.join(self.error_messages)
        app_site = self.web_app_site if self.web_app_site is not None else _('scielo web site')
        status = ''
        result = _('updated/published on {app_site}').format(app_site=app_site)
        reason = ''
        update = True
        if self.xc_status == 'rejected':
            update = False
            status = validation_status.STATUS_BLOCKING_ERROR
            if self.accepted_articles > 0:
                if self.total_not_converted > 0:
                    reason = _('because it is not complete ({value} were not converted). ').format(value=str(self.total_not_converted) + '/' + str(self.accepted_articles))
                else:
                    reason = _('because there are blocking errors in the package. ')
            else:
                reason = _('because there are blocking errors in the package. ')
        elif self.xc_status == 'ignored':
            update = False
            reason = _('because no document has changed. ')
        elif self.xc_status == 'accepted':
            status = validation_status.STATUS_WARNING
            reason = _(' even though there are some fatal errors. Note: These errors must be fixed in order to have good quality of bibliometric indicators and services. ')
        elif self.xc_status == 'approved':
            status = validation_status.STATUS_OK
            reason = ''
        else:
            status = validation_status.STATUS_FATAL_ERROR
            reason = _('because there are blocking errors in the package. ')
        action = _('will not be')
        if update:
            action = _('will be')
        text = u'{status}: {issueid} {action} {result} {reason}'.format(status=status, issueid=self.acron_issue_label, result=result, reason=reason, action=action)
        text = html_reports.p_message(_('converted') + ': ' + str(self.total_converted) + '/' + str(self.accepted_articles), False) + html_reports.p_message(text, False)
        return text
