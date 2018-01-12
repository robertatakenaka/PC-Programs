# coding=utf-8

import os
import shutil

from ...__init__ import _
from ...__init__ import BIN_PATH
from ...__init__ import FST_PATH

from ...generics.dbm import dbm_isis
from ...generics import encoding
from ...generics import fs_utils
from ...generics import doi_validations
from ...generics.reports import html_reports
from ...generics.reports import validation_status
from ..ws import institutions_manager
from ..ws import ws_journals
from ..validations import article_data_reports
from ..validations import pkg_articles_validations
from ..validations import article_validations as article_validations_module
from ..validations import validations as validations_module
from ..validations import reports_maker
from ..validations import merged_articles_validations
from ..services import institutions_normalizer
from ..data import package
from ..data import merged
from ..data import pkg_wk
from ..data import workarea
from ..db import registered
from ..db import manager

from ..db import xc_models
from . import pmc_pkgmaker
from . import sps_pkgmaker


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

    def article_validator(self, pkg, _registered, is_xml_generation):
        xml_journal_data_validator = article_validations_module.XMLJournalDataValidator(pkg.issue_data.journal_data)
        xml_issue_data_validator = article_validations_module.XMLIssueDataValidator(_registered)
        xml_content_validator = article_validations_module.XMLContentValidator(pkg.issue_data, _registered, is_xml_generation, self.app_institutions_manager, self.doi_validator, self.config)
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


class CheckedPackage(object):

    def __init__(self, validations_parameters, pkg_info):
        self.pkg_info = pkg_info
        # FIXME self.normalize_pkg_affiliations(pkg)
        self.parameters = validations_parameters
        self.registered = self.parameters.manager.get_registered(pkg_info.pkg_issue_data)
        self.files_location = workarea.AssetsDestinations(
                                pkg_info.wk.scielo_package_path,
                                pkg_info.issue_data.acron,
                                pkg_info.issue_data.issue_label,
                                self.parameters.config.serial_path,
                                self.parameters.config.local_web_app_path,
                                self.parameters.config.web_app_site)

    def make(self, GENERATE_PMC=False):
        self.normalize_pkg_affiliations()
        self.evaluate()
        self.generate_reports()
        self.generate_main_report(conversion=None)
        self.make_pmc_package(GENERATE_PMC)
        self.zip()

    def normalize_pkg_affiliations(self):
        for xml_name, a in self.pkg_info.articles.items():
            if a is not None:
                for aff_xml in a.affiliations:
                    if aff_xml is not None and aff_xml.id is not None:
                        normalized, variations = self.paramters.validators.aff_normalizer.normalize_institution_data(aff_xml.aff)
                        a.normalized_affiliations[aff_xml.id].normalized = normalized
                        a.normalized_affiliations[aff_xml.id].variations = variations

    def evaluate(self):
        self.validate_package()
        self.validate_merged_articles()

    def generate_reports(self):
        pkg_reports = pkg_articles_validations.PkgArticlesValidationsReports(self.pkg_validations, self.registered.articles_db_manager is not None)
        mergence_reports = merged_articles_validations.MergedArticlesReports(self.articles_mergence, self.registered)
        self.validations_reports = merged_articles_validations.IssueArticlesValidationsReports(pkg_reports, mergence_reports, self.is_xml_generation)

    def validate_package(self):
        article_validator = self.validator.article_validator(self.pkg_info, self.registered, self.parameters.is_xml_generation)
        encoding.display_message(_('Validate package ({n} files)').format(n=len(self.pkg_info.articles)))
        self.pkg_validations = {}
        for name in sorted(self.pkg_info.pkgfiles.keys()):
            pkgfiles = self.pkg_info.pkgfiles[name]
            encoding.display_message(_('Validate {name}').format(name=name))
            self.pkg_validations[name] = article_validator.validate(pkgfiles.article, self.pkg_info.outputs[name], pkgfiles)

    def validate_merged_articles(self):
        if len(self.registered.registered_articles) > 0:
            encoding.display_message(_('Previously registered: ({n} files)').format(n=len(self.registered.registered_articles)))
        self.articles_mergence = merged.ArticlesMergence(
            self.registered.registered_articles,
            self.pkg_info.articles,
            self.parameters.is_db_generation)

    def generate_main_report(self, conversion=None):
        reports = reports_maker.ReportsMaker(
                    self.pkg_info,
                    self.validations_reports,
                    self.files_location,
                    self.parameters.stage,
                    self.parameters.xpm_version,
                    conversion)
        if not self.parameters.is_xml_generation:
            reports.save_report(self.parameters.INTERATIVE)
        if conversion is not None:
            if self.registered.issue_files is not None:
                self.registered.issue_files.save_reports(self.files_location.report_path)
        if self.config.web_app_site is not None:
            for article_files in self.pkg_info.pkgfiles.values():
                # copia os xml para report path
                article_files.copy_xml(self.files_location.report_path)
        return reports

    def make_pmc_package(self, GENERATE_PMC):
        if not self.parameters.is_db_generation:
            pmc_package_maker = pmc_pkgmaker.PMCPackageMaker(
                self.pkg_info.wk,
                self.pkg_info.articles,
                self.pkg_info.outputs)
            if self.parameters.is_xml_generation:
                pmc_package_maker.make_report()
            if self.pkg_info.pkg_issue_data.is_pmc_journal:
                if GENERATE_PMC:
                    pmc_package_maker.make_package()
                else:
                    encoding.display_message(_('To generate PMC package, add -pmc as parameter'))

    def zip(self):
        if not self.parameters.is_xml_generation and not self.parameters.is_db_generation:
            self.pkg_info.pkgfolder.zip()
            for name, pkgfiles in self.pkg_info.pkgfiles.items():
                pkgfiles.zip(self.pkg_info.pkgfolder.path + '_zips')
