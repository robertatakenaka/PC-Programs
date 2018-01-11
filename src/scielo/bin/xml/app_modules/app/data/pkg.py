# coding=utf-8

from ...generics import xml_utils
from . import article
from . import sps_document
from . import pkg_wk


class ArticlePkgFiles(pkg_wk.PkgFiles):

    def __init__(self, filename):
        pkg_wk.PkgFiles.__init__(self, filename)
        self.xmlcontent = xml_utils.XMLContent(filename)

    @property
    def article(self):
        return article.Article(self.xmlcontent.xml, self.file.basename)

    @article.setter
    def article(self, content):
        self.xmlcontent = xml_utils.XMLContent(content)

    def get_pdf_files(self):
        expected_pdf_files = self.article.expected_pdf_files.values()
        return [f for f in expected_pdf_files if f in self.related_files]

    def get_package_href_files(self):
        files = []
        for href_name in self.get_package_href_names():
            extensions = self.related_files_by_name.get(href_name, [])
            names = [href_name+ext for ext in extensions]
            files.extend(names)
        return files

    def get_package_href_names(self):
        href_names = []
        for href in self.article.href_files:
            if href.name_without_extension in self.related_files_by_name.keys():
                href_names.append(href.name_without_extension)
        return list(set(href_names))

    def select_pmc_files(self):
        files = []
        for item in self.get_package_href_names():
            if item in self.tiff_names:
                if item+'.tif' in self.tiff_items:
                    files.append(item+'.tif')
                elif item+'.tiff' in self.tiff_items:
                    files.append(item+'.tiff')
            else:
                files.extend([item + ext for ext in self.related_files_by_name.get(item, [])])
        files.extend(self.get_pdf_files())
        return files


class ReceivedPackage(object):

    def __init__(self, xml_list):
        self.xml_list = xml_list

    def normalize(self, dtd_location_type, dest_path):
        self.pkgfiles = {}
        for item in self.xml_list:
            input_pkg = ArticlePkgFiles(item)
            input_pkg.tiff2jpg()

            xmlcontent = sps_document.SPSXMLContent(
                input_pkg.file.content, input_pkg.file.path)
            xmlcontent.normalize()
            xmlcontent.doctype(dtd_location_type)

            dest_filename = dest_path + '/' + input_pkg.file.basename
            pkg = ArticlePkgFiles(dest_filename)
            pkg.file.content = xmlcontent.content
            pkg.file.write()
            input_pkg.copy_related_files(dest_path)
            self.pkgfiles[input_pkg.file.name] = pkg


class PkgInfo(object):

    def __init__(self, pkgfiles, wk):
        self.pkgfiles = pkgfiles
        self.wk = wk
        self.pkgfolder = pkg_wk.PkgFolder(self.pkgfiles)
        self.articles = {k: v.article for k, v in self.pkgfiles.items()}
        self.pkg_issue_data = PkgIssueData(self.articles)
        self.outputs = {k: workarea.OutputFiles(k, wk.reports_path, None) for k, v in self.pkgfiles.items()}


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
