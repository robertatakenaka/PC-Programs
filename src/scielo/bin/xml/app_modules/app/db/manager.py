# coding=utf-8

from ..ws import ws_journals
from ..db import xc_models
from ..data import registered as registered_module


class Manager(object):

    def __init__(self, config):
        self.config = config
        self._db_manager = None
        self.ws_journals = ws_journals.Journals(self.config.app_ws_requester)
        self.ws_journals.update_journals_file()
        self.journals_list = xc_models.JournalsList(self.ws_journals.downloaded_journals_filename)
        self.registered_issues_manager = xc_models.RegisteredIssuesManager(self.db_manager, self.journals_list)

    def get_registered(self, pkgissuedata):
        registered = registered_module.Registered()
        if self.db_manager is None:
            journals_list = self.journals_list
            pkgissuedata.journal = self.journals_list.get_journal(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
            pkgissuedata.journal_data = self.journals_list.get_journal_data(pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn, pkgissuedata.pkg_journal_title)
        else:
            registered.acron_issue_label, registered.issue_models, registered.issue_error_msg, pkgissuedata.journal, pkgissuedata.journal_data = self.db_manager.get_registered_data(pkgissuedata.pkg_journal_title, pkgissuedata.pkg_issue_label, pkgissuedata.pkg_p_issn, pkgissuedata.pkg_e_issn)
            ign, pkgissuedata._issue_label = registered.acron_issue_label.split(' ')
            if registered.issue_error_msg is None:
                registered.issue_files = self.db_manager.get_issue_files(registered.issue_models)
                registered.articles_db_manager = xc_models.ArticlesManager(self.db_manager.db_isis, registered.issue_files)
        return registered
