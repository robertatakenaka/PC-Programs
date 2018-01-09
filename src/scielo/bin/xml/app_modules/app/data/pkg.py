# coding=utf-8

from ...generics import fs_utils
from ...generics import xml_utils
from . import article
from . import sps_document
from . import workarea


class ArticlePkgFiles(pkg_files.PkgFiles):

    def __init__(self, file):
        pkg_files.PkgFiles.__init__(self, file)
        self.xmlcontent = xml_utils.XMLContent(file.filename)

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

    def __init__(self, xml_list, wk):
        self.input_pkgfiles_items = [ArticlePkgFiles(fs_utils.File(item)) for item in xml_list]
        self.wk = wk
        dest_path = self.wk.scielo_package_path
        self.pkgfiles = [ArticlePkgFiles(fs_utils.File(dest_path + '/' + item.file.basename)) for item in self.input_pkgfiles_items]

    def normalize(self, dtd_location_type):
        self.outputs = {}
        for src, dest in zip(self.input_pkgfiles_items, self.pkgfiles):
            src.tiff2jpg()
            xmlcontent = sps_document.SPSXMLContent(src.file.content, src.file.path)
            xmlcontent.normalize()
            xmlcontent.doctype(dtd_location_type)
            dest.file.content = xmlcontent.content
            dest.file.write()
            src.copy_related_files(dest.file.path)
            self.outputs[dest.name] = workarea.OutputFiles(dest.file.name, self.wk.reports_path, None)


class Package(object):

    def __init__(self, pkgfiles_items, outputs, workarea_path):
        self.pkgfiles_items = pkgfiles_items
        self.package_folder = workarea.PackageFolder(pkgfiles_items[0].path, pkgfiles_items)
        self.outputs = outputs
        self.wk = workarea.Workarea(workarea_path)
        self._articles = None
        self._articles_xml_content = None
        self.issue_data = PackageIssueData()
        self.issue_data.setup(self.articles)

    @property
    def articles_xml_content(self):
        if self._articles_xml_content is None:
            self._articles_xml_content = {item.name: article.ArticleXMLContent(fs_utils.read_file(item.filename), item.previous_name, item.name) for item in self.pkgfiles_items}
        return self._articles_xml_content

    @property
    def articles(self):
        if self._articles is None:
            self._articles = {name: item.doc for name, item in self.articles_xml_content.items()}
        return self._articles

    @property
    def is_pmc_journal(self):
        return any([doc.journal_id_nlm_ta is not None for name, doc in self.articles.items()])


class PackageIssueData(object):

    def __init__(self):
        self.pkg_journal_title = None
        self.pkg_p_issn = None
        self.pkg_e_issn = None
        self.pkg_issue_label = None
        self.journal = None
        self.journal_data = None
        self._issue_label = None

    def setup(self, articles):
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
