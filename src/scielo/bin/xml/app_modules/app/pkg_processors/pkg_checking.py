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
from ..db import manager


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


class Validators(object):

    def __init__(self, config):
        self.config = config
        self.app_institutions_manager = institutions_manager.InstitutionsManager(self.config.app_ws_requester)
        self.aff_normalizer = institutions_normalizer.InstitutionsNormalizer(self.app_institutions_manager)
        self.doi_validator = doi_validations.DOIValidator(self.config.app_ws_requester)

    def article_validator(self, rcvd_pkg, is_xml_generation):
        xml_journal_data_validator = article_validations_module.XMLJournalDataValidator(rcvd_pkg.issue_data.journal_data)
        xml_issue_data_validator = article_validations_module.XMLIssueDataValidator(rcvd_pkg.registered)
        xml_content_validator = article_validations_module.XMLContentValidator(rcvd_pkg.issue_data, rcvd_pkg.registered, is_xml_generation, self.app_institutions_manager, self.doi_validator, self.config)
        return article_validations_module.ArticleValidator(xml_journal_data_validator, xml_issue_data_validator, xml_content_validator, self.config.xml_structure_validator_preference)


class ValidationsParameters(object):

    def __init__(self, config, INTERATIVE, stage='xpm'):
        self.manager = manager.Manager(config)
        self.validator = Validators(config)

        self.INTERATIVE = INTERATIVE
        self.stage = stage
        self.is_xml_generation = stage == 'xml'
        self.is_db_generation = stage == 'xc'
        self.xpm_version = xpm_version() if stage == 'xpm' else None


class PackageChecker(object):

    def __init__(self, validations_parameters, rcvd_pkg):
        self.rcvd_pkg = rcvd_pkg
        self.parameters = validations_parameters

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
                        normalized, variations = self.paramters.validators.aff_normalizer.normalize_institution_data(aff_xml.aff)
                        a.normalized_affiliations[aff_xml.id].normalized = normalized
                        a.normalized_affiliations[aff_xml.id].variations = variations

    def validate_package(self):
        article_validator = self.validator.article_validator(self.rcvd_pkg, self.parameters.is_xml_generation)
        encoding.display_message(_('Validate package ({n} files)').format(n=len(self.rcvd_pkg.articles)))
        self.pkg_validations = {}
        for name in sorted(self.rcvd_pkg.pkgfiles.keys()):
            pkgfiles = self.rcvd_pkg.pkgfiles[name]
            encoding.display_message(_('Validate {name}').format(name=name))
            self.pkg_validations[name] = article_validator.validate(pkgfiles.article, self.rcvd_pkg.outputs[name], pkgfiles)

    def validate_merged_articles(self):
        if len(self.rcvd_pkg.registered.registered_articles) > 0:
            encoding.display_message(_('Previously registered: ({n} files)').format(n=len(self.rcvd_pkg.registered.registered_articles)))
        self.articles_mergence = merged.ArticlesMergence(
            self.rcvd_pkg.registered.registered_articles,
            self.rcvd_pkg.articles,
            self.parameters.is_db_generation)

    def generate_reports(self):
        pkg_reports = pkg_articles_validations.PkgArticlesValidationsReports(self.pkg_validations, self.rcvd_pkg.registered.articles_db_manager is not None)
        mergence_reports = merged_articles_validations.MergedArticlesReports(self.articles_mergence, self.rcvd_pkg.registered)
        self.validations_reports = merged_articles_validations.IssueArticlesValidationsReports(pkg_reports, mergence_reports, self.parameters.is_xml_generation)

    def generate_main_report(self, files_location, pkg_converter=None):
        self.files_location = files_location
        self.main_report = reports_maker.ReportsMaker(
                    self.rcvd_pkg,
                    self.validations_reports,
                    files_location,
                    self.parameters.stage,
                    self.parameters.xpm_version,
                    pkg_converter)
        if not self.parameters.is_xml_generation:
            self.main_report.save_report(self.parameters.INTERATIVE)
