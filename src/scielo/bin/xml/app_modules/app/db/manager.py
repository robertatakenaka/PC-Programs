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
from ..db import xc_models
from . import pmc_pkgmaker
from . import sps_pkgmaker


class Manager(object):

    def __init__(self, config):
        self.config = config
        self._db_manager = None
        self.ws_journals = ws_journals.Journals(self.config.app_ws_requester)
        self.ws_journals.update_journals_file()
        self.journals_list = xc_models.JournalsList(self.ws_journals.downloaded_journals_filename)
        self.registered_issues_manager = xc_models.RegisteredIssuesManager(self.db_manager, self.journals_list)

    def get_registered(self, pkgissuedata):
        registered = Registered()
        if self.db_manager is None:
            journals_list = self.journals_list
            pkgissuedata.journal = self.journals_list.get_journal(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
            pkgissuedata.journal_data = self.journals_list.get_journal_data(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
        else:
            registered.acron_issue_label, registered.issue_models, registered.issue_error_msg, pkgissuedata.journal, pkgissuedata.journal_data = self.db_manager.get_registered_data(pkgissuedata.pkg_journal_title, pkgissuedata.pkg_issue_label, pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn)
            ign, pkgissuedata._issue_label = registered.acron_issue_label.split(' ')
            if registered.issue_error_msg is None:
                registered.issue_files = self.db_manager.get_issue_files(registered.issue_models)
                registered.articles_db_manager = ArticlesManager(self.db_manager.db_isis, registered.issue_files)
        return registered


class Registered(object):

    def __init__(self):
        self.issue_error_msg = None
        self.issue_models = None
        self.issue_files = None
        self.articles_db_manager = None

    @property
    def registered_articles(self):
        if self.articles_db_manager is not None:
            return self.articles_db_manager.registered_articles
        return {}
