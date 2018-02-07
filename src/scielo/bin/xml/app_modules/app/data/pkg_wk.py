# coding=utf-8

import os
import shutil

from ...generics import fs_utils
from ...generics import img_utils
from ...generics import xml_utils
from ..data import article


MARKUP_SUFFIXES = ['t', 'f', 'e', 'img', 'image']
MARKUP_SUFFIXES.extend(['-'+s for s in MARKUP_SUFFIXES])
MARKUP_SUFFIXES.extend(['-', '.', '0'])

XML_SUFFIXES = ['-', '.']

PREFIXES = {}
PREFIXES['frm'] = 'equation'
PREFIXES['form'] = 'equation'
PREFIXES['e'] = 'equation'
PREFIXES['eq'] = 'equation'
PREFIXES['equ'] = 'equation'
PREFIXES['img'] = 'graphic'
PREFIXES['image'] = 'graphic'
PREFIXES['t'] = 'tabwrap'
PREFIXES['tab'] = 'tabwrap'
PREFIXES['f'] = 'figgrp'
PREFIXES['fig'] = 'figgrp'
SORTED_PREFIXES = sorted(tuple(PREFIXES), reverse=True)


def classify_mkp_pkg_components_by_elem_name_and_id(name, main_name):
    done = False
    elem = None
    number = None
    posfix = name
    if name.startswith(main_name):
        posfix = name[len(main_name):]
    for k, v in SORTED_PREFIXES:
        if posfix.startswith(k):
            number = posfix[len(k):]
            if number.isdigit():
                number = int(number)
                elem = PREFIXES.get(k)
                done = True
        if done:
            break
    if done is False:
        numbers = ''
        notnumbers = ''
        for c in posfix:
            if c.isdigit():
                numbers += c
            elif c.upper() != c.lower():
                notnumbers += c
        elem = notnumbers
        number = int(numbers) if numbers != '' else None
    return elem, number, posfix


class Workarea(object):

    def __init__(self, output_path):
        self.output_path = output_path

        for p in [self.output_path, self.reports_path, self.scielo_package_path, self.pmc_package_path]:
            if not os.path.isdir(p):
                os.makedirs(p)

    @property
    def reports_path(self):
        return self.output_path + '/errors'

    @property
    def scielo_package_path(self):
        return self.output_path + '/scielo_package'

    @property
    def pmc_package_path(self):
        return self.output_path+'/pmc_package'

    @property
    def src_path(self):
        return self.output_path+'/src'


class PkgFiles(object):

    def __init__(self, filename):
        self._prefixes = None
        self.file = fs_utils.File(filename)

        if not os.path.isdir(self.file.path):
            os.makedirs(self.file.path)
        self.folder = os.path.basename(self.file.path)
        if self.file.filename.endswith('.sgm.xml'):
            self.file.name, ign = os.path.splitext(self.file.name)

        self.previous_name = self.file.name
        self.listdir = []
        self._load()

    def location(self, name):
        if os.path.isfile(self.file.path + '/' + name):
            return self.file.path + '/' + name

    def add_extension(self, new_href):
        if '.' not in new_href:
            extensions = self.related_files_by_name.get(new_href)
            if extensions is not None:
                if len(extensions) > 1:
                    extensions = [e for e in extensions if '.tif' in e or '.eps' in e] + extensions
                if len(extensions) > 0:
                    new_href += extensions[0]
        return new_href

    @property
    def prefixes(self):
        if self._prefixes is None:
            r = []
            SUFFIXES = XML_SUFFIXES
            if self.file.filename.endswith('.sgm.xml'):
                SUFFIXES = MARKUP_SUFFIXES
                if self.file.basename.startswith('a') and self.file.basename[3:4] == 'v':
                    r.extend([self.file.basename[:3] + suffix for suffix in SUFFIXES])
            r.extend([self.file.name + suffix for suffix in SUFFIXES])
            self._prefixes = list(set(r))
        return self._prefixes

    def select_files(self):
        r = []
        files = [item for item in self.listdir if not item.endswith('incorrect.xml') and not item.endswith('.sgm.xml')]
        for item in files:
            selected = [item for prefix in self.prefixes if item.startswith(prefix)]
            r.extend(selected)
        return list(set(r))

    def is_listdir_changed(self):
        listdir = os.listdir(self.file.path)
        if set(listdir) != set(self.listdir):
            self.listdir = listdir
            return True
        return False

    def _update(self):
        if self.is_listdir_changed():
            self._load()

    def _load(self):
        self._files = self.select_files()
        self._related_files = [f for f in self.files if f != self.file.basename and not f.endswith('.ctrl.txt')]
        self._related_files_by_name = {}
        self._related_files_by_extension = {}
        for f in self._related_files:
            name, extension = os.path.splitext(f)
            if name not in self._related_files_by_name.keys():
                self._related_files_by_name[name] = []
            if extension not in self._related_files_by_extension.keys():
                self._related_files_by_extension[extension] = []
            if extension not in self._related_files_by_name[name]:
                self._related_files_by_name[name].append(extension)
            if name not in self._related_files_by_extension[extension]:
                self._related_files_by_extension[extension].append(name)

        self._mkp_components_classified_by_elem_name_and_id = {}
        if self.file.filename.endswith('.sgm.xml'):
            for name, extensions in self._related_files_by_name:
                elem, number, alt = classify_mkp_pkg_components_by_elem_name_and_id(name, self.file.name)
                if elem is not None:
                    self._mkp_components_classified_by_elem_name_and_id[(elem, number)] = (name, extensions)

    @property
    def files(self):
        self._update()
        return self._files

    @property
    def related_files(self):
        self._update()
        return self._related_files

    @property
    def related_files_by_name(self):
        self._update()
        return self._related_files_by_name

    @property
    def mkp_components_classified_by_elem_name_and_id(self):
        self._update()
        return self._mkp_components_classified_by_elem_name_and_id

    @property
    def related_files_by_extension(self):
        self._update()
        return self._related_files_by_extension

    def files_by_ext(self, extensions):
        r = []
        for ext in extensions:
            r.extend([name+ext for name in self.related_files_by_extension.get(ext, [])])
        return r

    @property
    def png_items(self):
        return self.files_by_ext(['.png'])

    @property
    def jpg_items(self):
        return self.files_by_ext(['.jpg', '.jpeg'])

    @property
    def tiff_items(self):
        return self.files_by_ext(['.tif', '.tiff'])

    @property
    def png_names(self):
        return self.related_files_by_extension.get('.png', [])

    @property
    def jpg_names(self):
        return self.related_files_by_extension.get('.jpg', []) + self.related_files_by_extension.get('.jpeg', [])

    @property
    def tiff_names(self):
        return self.related_files_by_extension.get('.tiff', []) + self.related_files_by_extension.get('.tif', [])

    def clean(self):
        for f in self.related_files:
            fs_utils.delete_file_or_folder(self.file.path + '/' + f)
        self._update()

    def tiff2jpg(self):
        for item in self.tiff_names:
            if item not in self.jpg_names and item not in self.png_names:
                source_fname = item + '.tif'
                if source_fname not in self.related_files:
                    source_fname = item + '.tiff'
                img_utils.hdimg_to_jpg(self.file.path + '/' + source_fname, self.file.path + '/' + item + '.jpg')
        self._update()

    def delete_files(self, files):
        for f in files:
            fs_utils.delete_file_or_folder(self.file.path + '/' + f)
        self._update()

    def svg2tiff(self):
        sgv_items = self.files_by_ext(['.svg'])
        if len(self.tiff_items) == 0 and len(sgv_items) > 0:
            img_utils.svg2png(self.file.path)
            self._update()
            img_utils.png2tiff(self.file.path)
            self._update()

    def evaluate_tiff_images(self):
        errors = []
        for f in self.tiff_items:
            errors.append(img_utils.validate_tiff_image_file(self.file.path+'/'+f))
        return [e for e in errors if e is not None]

    def zip(self, dest_path=None):
        if dest_path is None:
            dest_path = os.path.dirname(self.file.path)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        filename = dest_path + '/' + self.file.name + '.zip'
        fs_utils.zip(filename, [self.file.path + '/' + f for f in self.files])
        return filename

    def copy_related_files(self, dest_path):
        if dest_path is not None:
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            for f in self.related_files:
                shutil.copyfile(self.file.path + '/' + f, dest_path + '/' + f)

    def copy_xml(self, dest_path):
        if dest_path is not None:
            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            shutil.copyfile(self.file.filename, dest_path + '/' + self.file.basename)


class ArticlePkgFiles(PkgFiles):

    def __init__(self, filename):
        PkgFiles.__init__(self, filename)
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


class ArticlePkgFolder(object):

    def __init__(self, xml_path, pkgfiles_items):
        self.name = os.path.basename(xml_path)
        self.xml_path = xml_path
        self.pkgfiles_items = pkgfiles_items
        if pkgfiles_items is None:
            self.pkgfiles_items = {}
            for filename in os.listdir(xml_path):
                f = fs_utils.File(filename)
                self.pkgfiles_items[f.name] = ArticlePkgFiles(filename)
        self.INFORM_ORPHANS = len(self.pkgfiles_items) > 1

    @property
    def package_filenames(self):
        items = []
        for pkg in self.pkgfiles_items.values():
            items.extend(pkg.files)
        return items

    @property
    def orphans(self):
        items = []
        if self.INFORM_ORPHANS is True:
            items = [f for f in os.listdir(self.xml_path) if f not in self.package_filenames]
        return items

    def zip(self, dest_path=None):
        if dest_path is None:
            dest_path = os.path.dirname(self.xml_path)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        _name = os.path.basename(self.xml_path)
        filename = dest_path + '/' + _name + '.zip'
        fs_utils.zip(filename, [self.xml_path + '/' + f for f in self.package_filenames])
        return filename


class OutputFiles(object):

    def __init__(self, xml_name, report_path, wrk_path):
        self.xml_name = xml_name
        self.report_path = report_path
        self.wrk_path = wrk_path

        #self.related_files = []
        #self.xml_filename = xml_filename
        #self.new_xml_filename = self.xml_filename
        #self.xml_path = os.path.dirname(xml_filename)
        #self.xml_name = basename.replace('.xml', '')
        #self.new_name = self.xml_name

    @property
    def report_path(self):
        return self._report_path

    @report_path.setter
    def report_path(self, _report_path):
        if not os.path.isdir(_report_path):
            os.makedirs(_report_path)
        self._report_path = _report_path

    @property
    def ctrl_filename(self):
        if self.wrk_path is not None:
            if not os.path.isdir(self.wrk_path):
                os.path.makedirs(self.wrk_path)
            return self.wrk_path + '/' + self.xml_name + '.ctrl.txt'

    @property
    def style_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.rep.html'

    @property
    def dtd_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.dtd.txt'

    @property
    def pmc_dtd_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.pmc.dtd.txt'

    @property
    def pmc_style_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.pmc.rep.html'

    @property
    def err_filename(self):
        return self.report_path + '/' + self.xml_name + '.err.txt'

    @property
    def err_filename_html(self):
        return self.report_path + '/' + self.xml_name + '.err.html'

    @property
    def mkp2xml_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.mkp2xml.txt'

    @property
    def mkp2xml_report_filename_html(self):
        return self.report_path + '/' + self.xml_name + '.mkp2xml.html'

    @property
    def data_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.contents.html'

    @property
    def images_report_filename(self):
        return self.report_path + '/' + self.xml_name + '.images.html'

    @property
    def xml_structure_validations_filename(self):
        return self.report_path + '/xmlstr-' + self.xml_name

    @property
    def xml_content_validations_filename(self):
        return self.report_path + '/xmlcon-' + self.xml_name

    @property
    def journal_validations_filename(self):
        return self.report_path + '/journal-' + self.xml_name

    @property
    def issue_validations_filename(self):
        return self.report_path + '/issue-' + self.xml_name

    def clean(self):
        for f in [self.err_filename, self.dtd_report_filename, self.style_report_filename, self.pmc_dtd_report_filename, self.pmc_style_report_filename, self.ctrl_filename]:
            fs_utils.delete_file_or_folder(f)


class AssetsDestinations(object):

    def __init__(self, pkg_path, acron, issue_label, serial_path=None, web_app_path=None, web_url=None):
        self.web_app_path = web_app_path
        self.pkg_path = pkg_path
        self.issue_path = acron + '/' + issue_label
        self.serial_path = serial_path
        self.web_url = web_url

    @property
    def result_path(self):
        if self.serial_path is not None:
            return self.serial_path + '/' + self.issue_path
        else:
            return os.path.dirname(self.pkg_path)

    @property
    def img_path(self):
        if self.web_app_path is not None:
            return self.web_app_path + '/htdocs/img/revistas/' + self.issue_path
        else:
            return self.pkg_path

    @property
    def pdf_path(self):
        if self.web_app_path is not None:
            return self.web_app_path + '/bases/pdf/' + self.issue_path
        else:
            return self.pkg_path

    @property
    def xml_path(self):
        if self.web_app_path is not None:
            return self.web_app_path + '/bases/xml/' + self.issue_path
        elif self.serial_path is not None:
            return self.serial_path + '/' + self.issue_path + '/base_xml/base_source'
        else:
            return self.pkg_path

    @property
    def report_path(self):
        if self.web_app_path is not None:
            return self.web_app_path + '/htdocs/reports/' + self.issue_path
        else:
            return self.result_path + '/errors'

    @property
    def report_link(self):
        if self.web_url is not None:
            return self.web_url + '/reports/' + self.issue_path
        else:
            return self.result_path + '/errors'

    @property
    def base_report_path(self):
        if self.serial_path is not None:
            return self.serial_path + '/' + self.issue_path + '/base_xml/base_reports'

    @property
    def img_link(self):
        if self.web_url is not None:
            return self.web_url + '/img/revistas/' + self.issue_path
        else:
            return 'file://' + self.img_path

    @property
    def pdf_link(self):
        if self.web_url is not None:
            return self.web_url + '/pdf/' + self.issue_path + '/'
        else:
            return 'file://' + self.pdf_path + '/'

    @property
    def xml_link(self):
        if self.web_url is not None:
            return self.web_url + '/xml/' + self.issue_path + '/'
        else:
            return 'file://' + self.xml_path + '/'
