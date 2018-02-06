# coding=utf-8

from ..data import sps_document
from ..data import pkg_wk


class Reception(object):

    def __init__(self, manager):
        self.manager = manager

    def normalize(self, xml_list, dtd_location_type, dest_path):
        pkgfiles = {}
        for item in self.xml_list:
            input_pkg = pkg_wk.ArticlePkgFiles(item)
            input_pkg.tiff2jpg()

            xmlcontent = sps_document.SPSXMLContent(
                input_pkg.file.content, input_pkg.file.path)
            xmlcontent.normalize()
            xmlcontent.doctype(dtd_location_type)

            dest_filename = dest_path + '/' + input_pkg.file.basename
            pkg = pkg_wk.ArticlePkgFiles(dest_filename)
            pkg.file.content = xmlcontent.content
            pkg.file.write()
            input_pkg.copy_related_files(dest_path)
            pkgfiles[input_pkg.file.name] = pkg
        return pkgfiles

    def receive(self, pkgfiles, wk, outputs):
        received = ReceivedPackage(pkgfiles, wk, outputs)
        received.registered = self.manager.get_registered(
            received.pkg_issue_data)
        return received


class ReceivedPackage(object):

    def __init__(self, pkgfiles, wk, outputs):
        self.pkgfiles = pkgfiles
        self.wk = wk
        # FIXME path
        self.pkgfolder = pkg_wk.ArticlePkgFolder(path, self.pkgfiles)
        self.articles = {k: v.article for k, v in self.pkgfiles.items()}
        self.pkg_issue_data = PkgIssueData(self.articles)
        self.outputs = outputs
        if outputs is None:
            self.outputs = {k: workarea.OutputFiles(k, wk.reports_path, None) for k, v in self.pkgfiles.items()}
        self.registered = None


class PkgIssueData(object):

    def __init__(self, articles):
        self.pkg_journal_title = None
        self.pkg_p_issn = None
        self.pkg_e_issn = None
        self.pkg_issue_label = None
        self.journal = None
        self.journal_data = None
        self._issue_label = None
        self.is_pmc_journal = any([doc.journal_id_nlm_ta is not None for name, doc in self.articles.items()])

        data = [(a.journal_title, a.print_issn, a.e_issn, a.issue_label) for a in articles.values() if a.tree is not None]
        if len(data) > 0:
            self.pkg_journal_title, self.pkg_p_issn, self.pkg_e_issn, self.pkg_issue_label = self.select(data)

    def select(self, data):
        _data = []
        for item in list(set(data)):
            _data.append([field if field is not None else '' for field in item])
        _data = sorted(_data, reverse=True)
        return [item if item != '' else None for item in _data[0]]

    @property
    def acron(self):
        a = 'unknown_acron'
        if self.journal is not None:
            if self.journal.acron is not None:
                a = self.journal.acron
        return a

    @property
    def acron_issue_label(self):
        return self.acron + ' ' + self.issue_label

    @property
    def issue_label(self):
        r = self._issue_label if self._issue_label else self.pkg_issue_label
        if r is None:
            r = 'unknown_issue_label'
        return r
