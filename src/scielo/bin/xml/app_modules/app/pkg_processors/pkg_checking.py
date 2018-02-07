# coding=utf-8

import os

from ...__init__ import _
from ...__init__ import BIN_PATH

from ...generics import encoding
from ...generics import fs_utils
from ...generics import doi_validations

from ..ws import institutions_manager

from ..validations import pkg_articles_validations
from ..validations import article_validations as article_validations_module
from ..validations import reports_maker
from ..validations import merged_articles_validations

from ..services import institutions_normalizer
from ..data import merged


def xpm_version():
    version_files = [
        BIN_PATH + '/xpm_version.txt',
        BIN_PATH + '/cfg/xpm_version.txt',
    ]
    version = '|'
    for f in version_files:
        encoding.debugging('xpm_version', f)
        if os.path.isfile(f):
            version = fs_utils.read_file_lines(f)[0]
            break
    if '|' not in version:
        version += '|'
    encoding.debugging('version', version)
    major_version, minor_version = version.split('|')
    return major_version, minor_version


class PkgChecking(object):

    def __init__(self, pkg_checker, rcvd_pkg):
        self.pkg_checker = pkg_checker
        self.rcvd_pkg = rcvd_pkg

    def check(self):
        self.normalize_pkg_affiliations()
        self.validate_package()
        self.validate_merged_articles()

    def report(self, files_location, pkg_converter=None):
        self.generate_reports()
        self.generate_main_report(files_location, pkg_converter)

    def normalize_pkg_affiliations(self):
        for xml_name, a in self.rcvd_pkg.articles.items():
            if a is not None:
                for aff_xml in a.affiliations:
                    if aff_xml is not None and aff_xml.id is not None:
                        normalized, variations = self.pkg_checker.aff_normalizer.normalize_institution_data(aff_xml.aff)
                        a.normalized_affiliations[aff_xml.id].normalized = normalized
                        a.normalized_affiliations[aff_xml.id].variations = variations

    def validate_package(self):
        article_validator = self.pkg_checker.article_validator(self.rcvd_pkg)
        encoding.display_message(_('Validate package ({n} files)').format(n=len(self.rcvd_pkg.articles)))
        self.pkg_validations = {}
        for name in sorted(self.rcvd_pkg.pkgfiles.keys()):
            pkgfiles = self.rcvd_pkg.pkgfiles[name]
            encoding.display_message(_('Validate {name}').format(name=name))
            self.pkg_validations[name] = article_validator.validate(pkgfiles.article, self.rcvd_pkg.outputs[name], pkgfiles)

    def validate_merged_articles(self):
        if len(self.rcvd_pkg.registered.registered_articles) > 0:
            encoding.display_message(_('Previously registered: ({n} files)').format(n=len(self.rcvd_pkg.registered.registered_articles)))
        self.mergence = merged.ArticlesMergence(
            self.rcvd_pkg.registered.registered_articles,
            self.rcvd_pkg.articles,
            self.pkg_checker.is_db_generation)

    def generate_reports(self):
        pkg_reports = pkg_articles_validations.PkgArticlesValidationsReports(
            self.pkg_validations,
            self.rcvd_pkg.registered.articles_db_manager is not None)

        self.checking_reports = CheckingReports(
            self.rcvd_pkg,
            self.mergence,
            pkg_reports,
            self.pkg_checker.is_xml_generation)

    def generate_main_report(self, files_location, pkg_converter=None):
        self.files_location = files_location
        self.main_report = reports_maker.ReportsMaker(
                    self.checking_reports,
                    files_location,
                    self.pkg_checker.stage,
                    self.pkg_checker.xpm_version,
                    pkg_converter)
        if not self.pkg_checker.is_xml_generation:
            self.main_report.save_report(self.pkg_checker.INTERATIVE)


class PkgChecker(object):

    def __init__(self, config, stage='xpm'):
        self.config = config
        self.stage = stage
        self.app_institutions_manager = institutions_manager.InstitutionsManager(self.config.app_ws_requester)
        self.aff_normalizer = institutions_normalizer.InstitutionsNormalizer(self.app_institutions_manager)
        self.doi_validator = doi_validations.DOIValidator(self.config.app_ws_requester)
        self.is_xml_generation = stage == 'xml'
        self.is_db_generation = stage == 'xc'
        self.xpm_version = xpm_version() if stage == 'xpm' else None
        self.INTERATIVE = config.interative_mode and stage in ['xc', 'xpm']

    def get_article_validator(self, rcvd_pkg):
        xml_journal_data_validator = article_validations_module.XMLJournalDataValidator(rcvd_pkg.issue_data.journal_data)
        xml_issue_data_validator = article_validations_module.XMLIssueDataValidator(rcvd_pkg.registered)
        xml_content_validator = article_validations_module.XMLContentValidator(rcvd_pkg.issue_data, rcvd_pkg.registered, self.is_xml_generation, self.app_institutions_manager, self.doi_validator, self.config)
        return article_validations_module.ArticleValidator(xml_journal_data_validator, xml_issue_data_validator, xml_content_validator, self.config.xml_structure_validator_preference)


class CheckingReports(object):

    def __init__(self, rcvd_pkg, mergence, pkg_validations_reports, is_xml_generation=False):
        self.rcvd_pkg = rcvd_pkg
        mgd = merged.Merged(mergence.merged_articles, self.rcvd_pkg.registered.articles_db_manager is not None)
        self.mgd_reports = merged_articles_validations.MergedReports(mgd)
        self.mergence_reports = merged_articles_validations.MergenceReports(mergence)
        self.pkg_validations_reports = pkg_validations_reports
        self.is_xml_generation = is_xml_generation
        self.blocking_errors = sum([self.merged_validations.blocking_errors,
            self.pkg_validations_reports.pkg_issue_validations.blocking_errors])
        self.pkg_folder_reports = pkg_articles_validations.PkgFolderReports(rcvd_pkg.pkgfolder)
        self.pkg_articles_data_reports = pkg_articles_validations.PkgArticlesDataReports(rcvd_pkg.articles)

    @property
    def merged_content(self):
        if not hasattr(self, '_content'):
            r = []
            if self.rcvd_pkg.registered.issue_error_msg is not None:
                r.append(self.rcvd_pkg.registered.issue_error_msg)
            r.append(self.mgd_reports.consistency_report)
            r.append(self.mgd_reports.report_issue_page_values)
            r.append(self.mergence_reports.report_articles_data_conflicts)
            r.append(self.mergence_reports.report_articles_data_changes)
            self._content = ''.join(r)
        return self._content

    @property
    def merged_validations(self):
        if not hasattr(self, '_validations'):
            self._validations = validations_module.ValidationsResult()
            self._validations.message = self.content
        return self._validations

    @property
    def journal_and_issue_report(self):
        report = []
        report.append(self.mgd_reports.journal_issue_header_report)
        errors_only = not self.is_xml_generation
        report.append(self.pkg_validations_reports.pkg_journal_validations.report(errors_only))
        report.append(self.pkg_validations_reports.pkg_issue_validations.report(errors_only))
        report.append(self.merged_content)
        return ''.join(report)

    @property
    def pkg_files_report(self):
        return self.pkg_folder_reports.orphan_files_report + self.pkg_articles_data_report.invalid_xml_report

    @property
    def group_validations_report(self):
        r = self.pkg_files_report
        if not self.is_xml_generation:
            r += self.journal_and_issue_report
        if self.rcvd_pkg.registered.issue_error_msg is not None:
            r += self.rcvd_pkg.registered.issue_error_msg
        return r

    @property
    def individual_validations_report(self):
        return self.pkg_validations_reports.detailed_report

    @property
    def aff_report(self):
        return self.pkg_articles_data_report.articles_affiliations_report

    @property
    def dates_report(self):
        return self.pkg_articles_data_report.articles_dates_report

    @property
    def references(self):
        return self.pkg_articles_data_report.references_overview_report + self.pkg_articles_data_report.sources_overview_report
