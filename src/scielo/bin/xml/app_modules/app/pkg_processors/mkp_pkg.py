# coding=utf-8

import os
import shutil

from ...generics import fs_utils
from ...generics import encoding
from ...generics import java_xml_utils
from ...generics import xml_utils

from ...__init__ import _
from ...generics.reports import text_report
from ...generics.reports import html_reports
from ...generics.reports import validation_status
from ..data import pkg_files
from ..data import sps_document
from ..data import xhtml_document
from . import symbols
from . import xml_versions


class SGMLHTMLDocment(object):

    def __init__(self, html_filename):
        self.htmlfile = fs_utils.File(html_filename, encoding.SYS_DEFAULT_ENCODING)
        self.find_html_img_path()
        self.find_img_src_items()
        self.find_fontsymbols()

    def location(self, name):
        if os.path.isfile(self.html_img_path + '/' + name):
            return self.html_img_path + '/' + name

    def find_html_img_path(self):
        path = None
        for item in os.listdir(self.htmlfile.path):
            if os.path.isdir(self.htmlfile.path + '/' + item) and item.startswith(self.htmlfile.name):
                path = self.htmlfile.path + '/' + item
                break
        if path is None:
            path = self._alternative_html_img_path(self.htmlfile.path, self.htmlfile.name)
        if path is None:
            path = self.htmlfile.path
        self.html_img_path = path

    def _alternative_html_img_path(self):
        #name_image001
        new_html_folder = self.htmlfile.path + '/' + self.htmlfile.name + '_arquivosalt'
        if not os.path.isdir(new_html_folder):
            os.makedirs(new_html_folder)
        for item in os.listdir(self.htmlfile.path):
            if os.path.isfile(self.htmlfile.path + '/' + item) and item.startswith(self.htmlfile.name + '_image'):
                new_name = item[len(self.htmlfile.name)+1:]
                shutil.copyfile(self.htmlfile.path + '/' + item, new_html_folder + '/' + new_name)
        return new_html_folder

    @property
    def img_files(self):
        return os.listdir(self.html_img_path)

    @property
    def img_href_items(self):
        return [item for item in self.img_src_items if item != 'None']

    def find_img_src_items(self):
        """
        [graphic href=&quot;?a20_115&quot;]</span><img border=0 width=508 height=314
        src="a20_115.temp_arquivos/image001.jpg"><span style='color:#33CCCC'>[/graphic]
        """
        html_content = self.htmlfile.content
        if 'href=&quot;?' in html_content:
            html_content = html_content.replace('href=&quot;?', 'href="?')
        """
        if '“' in html_content:
            html_content = html_content.replace('“', '"')
        if '”' in html_content:
            html_content = html_content.replace('”', '"')
        """
        _items = html_content.replace('href="?', 'href="?--~BREAK~FIXHREF--FIXHREF').split('--~BREAK~FIXHREF--')
        items = [item for item in _items if item.startswith('FIXHREF')]
        img_src = []
        for item in items:
            if 'src="' in item:
                src = item[item.find('src="') + len('src="'):]
                src = src[0:src.find('"')]
                if '/' in src:
                    src = src[src.find('/') + 1:]
                if len(src) > 0:
                    img_src.append(src)
            else:
                img_src.append(None)
        self.img_src_items = img_src

    def find_fontsymbols(self):
        r = []
        html_content = self.htmlfile.content
        if '[fontsymbol]' in html_content.lower():
            for style in ['italic', 'sup', 'sub', 'bold']:
                html_content = html_content.replace('<' + style + '>', '[' + style + ']')
                html_content = html_content.replace('</' + style + '>', '[/' + style + ']')

            html_content = html_content.replace('[fontsymbol]'.upper(), '[fontsymbol]')
            html_content = html_content.replace('[/fontsymbol]'.upper(), '[/fontsymbol]')
            html_content = html_content.replace('[fontsymbol]', '~BREAK~[fontsymbol]')
            html_content = html_content.replace('[/fontsymbol]', '[/fontsymbol]~BREAK~')

            html_fontsymbol_items = [item for item in html_content.split('~BREAK~') if item.startswith('[fontsymbol]')]
            for item in html_fontsymbol_items:
                item = item.replace('[fontsymbol]', '').replace('[/fontsymbol]', '')
                item = item.replace('<', '~BREAK~<').replace('>', '>~BREAK~')
                item = item.replace('[', '~BREAK~[').replace(']', ']~BREAK~')
                parts = [part for part in item.split('~BREAK~') if not part.endswith('>') and not part.startswith('<')]

                new = ''
                for part in parts:
                    if part.startswith('['):
                        new += part
                    else:

                        for c in part:
                            _c = c.strip()
                            if _c.isdigit() or _c == '':
                                n = c
                            else:
                                try:
                                    n = symbols.get_symbol(c)
                                except:
                                    n = '?'
                            new += n
                for style in ['italic', 'sup', 'sub', 'bold']:
                    new = new.replace('[' + style + ']', '<' + style + '>')
                    new = new.replace('[/' + style + ']', '</' + style + '>')
                r.append(new)
        self.fontsymbols = r


class SGMLXMLFixed(object):

    def __init__(self, content, src_pkgfiles, sgmlhtmldoc):
        self.src_pkgfiles = src_pkgfiles
        self.sgmlhtmldoc = sgmlhtmldoc
        self.content = self.fix_begin_end(xml_utils.remove_doctype(content))

    def fix_begin_end(self, content):
        s = content
        if '<?xml' in s:
            s = s[s.find('>')+1:]
        if '<!DOCTYPE' in s:
            s = s[s.find('>')+1:]
        if '<doc' in s:
            remove = s[:s.find('<doc')]
            if len(remove) > 0:
                content = content.replace(remove, '')
        if not content.endswith('</doc>') and '</doc>' in content:
            content = content[:content.rfind('</doc>')+len('</doc>')]
        return content

    def fix(self):
        self.fix_quotes()
        self.fix_styles_names()

        self.xmlcontent = xml_utils.XMLContent(self.content)
        self.replace_fontsymbols()
        self.replace_xhtml_items()

        self.insert_mml_namespace_reference()

        self.find_undefined_href_items()
        self.define_graphic_href_files()
        self.replace_undefined_href_items()

        self.remove_exceding_styles_tags()
        self.content = self.fix_begin_end(self.content)
        if self.xmlcontent.xml is None:
            self.xmlcontent.fix()
            self.content = self.xmlcontent.content

    def fix_styles_names(self):
        for style in ['italic', 'bold', 'sup', 'sub']:
            s = '<' + style + '>'
            e = '</' + style + '>'
            self.content = self.content.replace(s.upper(), s.lower()).replace(e.upper(), e.lower())

    def remove_exceding_styles_tags(self):
        self.fix_styles_names()
        content = ''
        while content != self.content:
            content = self.content
            for style in ['italic', 'bold', 'sup', 'sub']:
                self._remove_exceding_style_tag(style)

    def _remove_exceding_style_tag(self, style):
        s = '<' + style + '>'
        e = '</' + style + '>'
        self.content = self.content.replace(e + s, '')
        self.content = self.content.replace(e + ' ' + s, ' ')

    def fix_quotes(self):
        self.content = self.content.replace('href=&quot;?', 'href="?')
        self.content = self.content.replace('"">', '">')
        self.content = self.content.replace('href=""?', 'href="?')
        if u'“' in self.content or u'”' in self.content:
            items = []
            for item in self.content.replace('<', '~BREAK~<').split('~BREAK~'):
                if u'“' in item or u'”' in item and item.startswith('<'):
                    elem = item[:item.find('>')]
                    new = elem.replace(u'“', '"').replace(u'”', '"')
                    item = item.replace(elem, new)
                items.append(item)
            self.content = ''.join(items)

    def insert_mml_namespace_reference(self):
        if '>' in self.content:
            self.content = self.content[:self.content.rfind('>') + 1]
        if 'mml:' in self.content and 'xmlns:mml="https://www.w3.org/1998/Math/MathML"' not in self.content:
            if '</' in self.content:
                main_tag = self.content[self.content.rfind('</') + 2:]
                main_tag = main_tag[:main_tag.find('>')]
                if '<' + main_tag + ' ':
                    self.content = self.content.replace('<' + main_tag + ' ', '<' + main_tag + ' xmlns:mml="https://www.w3.org/1998/Math/MathML" ')

    def replace_fontsymbols(self):
        if self.xmlcontent.xml is not None:
            index = 0
            parent_nodes = self.xmlcontent.xml.findall('.//*[fontsymbol]') or []
            for parent_node in parent_nodes:
                nodes = parent_node.findall('fontsymbol') or []
                for node in nodes:
                    new = self.sgmlhtmldoc.fontsymbols[index]
                    index += 1
                    node.text = new
        self.update_content()

    def replace_xhtml_items(self):
        if self.xmlcontent.xml is not None:
            nodes = self.xmlcontent.xml.findall('.//*[xhtml]') or []
            for parent_node in nodes:
                node = parent_node.find('xhtml')
                href = node.get('href')
                xhtml_filename = self.src_pkgfiles.location(href)
                if xhtml_filename is not None:
                    xhtmldoc = xhtml_document.XHTMLDocument(xhtml_filename)
                    if xhtmldoc.body_content is not None:
                        parent_node.remove(node)
                        parent_node.append(xhtmldoc.body_content)
            self.update_content()

    def find_undefined_href_items(self):
        self.undefined_href_items = []
        if self.xmlcontent.xml is not None:
            nodes = self.xmlcontent.xml.findall('.//*[graphic]') or []
            for node in nodes:
                parent = node
                graphic = node.find('graphic')
                if graphic.get('href', '').startswith('?'):
                    href_info = {}
                    href_info['name'] = parent.tag
                    href_info['id'] = parent.get('id')
                    href_info['graphic'] = graphic
                    self.undefined_href_items.append(href_info)

    def define_graphic_href_files(self):
        if len(self.undefined_href_items) != len(self.sgmlhtmldoc.img_src_items):
            error = '{} (graphics) x {} (src)'.format(len(self.undefined_href_items), len(self.sgmlhtmldoc.img_src_items))
        else:
            print(self.undefined_href_items)
            for sgml_graphic, html_href in zip(self.undefined_href_items, self.sgmlhtmldoc.img_src_items):
                if html_href is not None:
                    elem_name = sgml_graphic.get('name')
                    elem_id = sgml_graphic.get('id')
                    graphic = sgml_graphic.get('graphic')
                    number = get_numbers(elem_id)
                    pkg_elem_from_doc = self.sgmlhtmldoc.location(html_href)
                    pkg_elem_origin = 'doc'
                    new_href_value = html_href

                    src_href = self.src_pkgfiles.mkp_components_classified_by_elem_name_and_id.get((elem_name, number))
                    if src_href is not None:
                        pkg_elem_from_src = self.src_pkgfiles.location(src_href)
                        pkg_elem_origin = 'src'
                        new_href_value = src_href
                    else:
                        # copy html image to src folder
                        new_href_value = self.src_pkgfiles.file.name + '-' + html_href
                        shutil.copyfile(pkg_elem_from_doc, self.src_pkgfiles.path + '/' + new_href_value)

                    if new_href_value is not None:
                        graphic.set('href', new_href_value)
                        sgml_graphic['pkg_elem_html_href'] = html_href
                        sgml_graphic['pkg_elem_href'] = new_href_value
                        sgml_graphic['pkg_elem_origin'] = pkg_elem_origin
                        sgml_graphic['pkg_elem_from_src'] = pkg_elem_from_src
                        sgml_graphic['pkg_elem_from_doc'] = pkg_elem_from_doc
            print(self.undefined_href_items)

    def replace_undefined_href_items(self):
        for href_info in self.undefined_href_items:
            href_info['graphic'].set('href', href_info['pkg_elem_href'])
        self.update_content()

    def update_content(self):
        replace = self.content[self.content.find('<doc'):]
        self.content = self.content.replace(replace, xml_utils.tostring(self.xmlcontent.xml.getroot()))


class SGMLXMLDocument(object):

    def __init__(self, sgmlfile, src_pkgfiles):
        self.sgmlfile = sgmlfile
        self.src_pkgfiles = src_pkgfiles
        shutil.copyfile(self.sgmlfile.filename, self.sgmlfile.filename+'.bkp')

    @property
    def html_filename(self):
        return self.sgmlfile.path + '/' + self.sgmlfile.name + '.temp.htm'

    def fix(self):
        sgmlhtmldoc = SGMLHTMLDocment(self.html_filename)
        fixer = SGMLXMLFixed(self.sgmlfile.content, self.src_pkgfiles, sgmlhtmldoc)
        fixer.fix()
        self.href_files_info = fixer.undefined_href_items
        self.sgmlfile.content = fixer.content
        self.sgmlfile.write()
        self.sps_version = fixer.xmlcontent.xml.getroot().get('sps')


class PackageName(object):

    def __init__(self, doc):
        self.doc = doc
        self.xml_name = doc.xml_name

    def generate(self, acron):
        parts = [self.issn, acron, self.doc.volume, self.issueno, self.suppl, self.last, self.doc.compl]
        return '-'.join([part for part in parts if part is not None and not part == ''])

    @property
    def issueno(self):
        _issueno = self.doc.number
        if _issueno:
            if _issueno == 'ahead':
                _issueno = '0'
            if _issueno.isdigit():
                if int(_issueno) == 0:
                    _issueno = None
                else:
                    n = len(_issueno)
                    if len(_issueno) < 2:
                        n = 2
                    _issueno = _issueno.zfill(n)
        return _issueno

    @property
    def suppl(self):
        s = self.doc.volume_suppl if self.doc.volume_suppl else self.doc.number_suppl
        if s is not None:
            s = 's' + s if s != '0' else 'suppl'
        return s

    @property
    def issn(self):
        _issns = [_issn for _issn in [self.doc.e_issn, self.doc.print_issn] if _issn is not None]
        if len(_issns) > 0:
            if self.xml_name[0:9] in _issns:
                _issn = self.xml_name[0:9]
            else:
                _issn = _issns[0]
        return _issn

    @property
    def last(self):
        if self.doc.fpage is not None and self.doc.fpage != '0':
            _last = self.doc.fpage
            if self.doc.fpage_seq is not None:
                _last += self.doc.fpage_seq
        elif self.doc.elocation_id is not None:
            _last = self.doc.elocation_id
        elif self.doc.number == 'ahead' and self.doc.doi is not None and '/' in self.doc.doi:
            _last = self.doc.doi[self.doc.doi.find('/')+1:].replace('.', '-')
        else:
            _last = self.doc.publisher_article_id
        return _last


class PackageRenamed(object):

    def __init__(self, src_pkgfiles, mkp_href_info_items):
        self.src_pkgfiles = src_pkgfiles
        self.dest_pkgfiles = None
        self.mkp_href_info_items = mkp_href_info_items

    def rename(self, acron, dest_path):
        self.new_name = PackageName(self.src_pkgfiles.article).generate(acron)

        xml_filename = dest_path + '/' + self.new_name + '.xml'
        self.dest_pkgfiles = pkg_files.ArticlePkgFiles(xml_filename)
        self.dest_pkgfiles.clean()

        self._rename_xml_href_values()
        self._rename_href_files()
        self._rename_other_files()

    def _rename_xml_href_values(self):
        content = self.src_pkgfiles.file.content
        self.renamed_href_items = []
        for href in self.src_pkgfiles.article.href_files:
            new = self._xml_href_value(href)
            self.renamed_href_items.append((href.src, new))
            if href.src != new:
                content = content.replace('href="' + href.src + '"', 'href="' + new + '"')
        self.dest_pkgfiles.file.content = content
        self.dest_pkgfiles.file.write()

    def _xml_href_value(self, href):
        href_type = href.href_attach_type
        href_id = href.id
        if href_id is None:
            href_id = href.src.replace(self.src_pkgfiles.name, '')
            href_id = href_id.replace('image', '').replace('img', '')
            if href_id[0:1] in '-_':
                href_id = href_id[1:]
        else:
            if '.' in href.src:
                href_id += href.ext
        if href_id.startswith(href_type):
            href_type = ''
        new_href = self.new_name + '-' + href_type + href_id
        new_href = self.src_pkgfiles.add_extension(new_href)
        return new_href

    def _rename_href_files(self):
        self.href_files_copy = []
        self.href_names = []
        self.missing_href_files = []
        for f, new in self.renamed_href_items:
            name, _ = os.path.splitext(f)
            new_name, _ = os.path.splitext(new)
            for ext in self.src_pkgfiles.related_files_by_name.get(name, []):
                shutil.copyfile(self.src_pkgfiles.path + '/' + name + ext, self.dest_pkgfiles.path + '/' + new_name + ext)
                self.href_files_copy.append((name + ext, new_name + ext))
                self.href_names.append(name)
            if self.dest_pkgfiles.related_files_by_name.get(new_name) is None:
                self.missing_href_files.append(new)

    def _rename_other_files(self):
        self.related_files_copy = []
        for name, ext_items in self.src_pkgfiles.related_files_by_name.items():
            if name not in self.href_names:
                for ext in ext_items:
                    new_name = name.replace(self.src_pkgfiles.name, self.new_name)
                    if self.new_name in new_name:
                        shutil.copyfile(self.src_pkgfiles.path + '/' + name + ext, self.dest_pkgfiles.path + '/' + new_name + ext)
                        self.related_files_copy.append((name + ext, new_name + ext))

    def report(self):
        log = []
        log.append(_('Report of files') + '\n' + '-'*len(_('Report of files')) + '\n')
        log.append(_('Source path') + ':   ' + self.src_pkgfiles.path)
        log.append(_('Package path') + ':  ' + self.dest_pkgfiles.path)
        log.append(_('Source XML name') + ': ' + self.src_pkgfiles.name)
        log.append(_('Package XML name') + ': ' + self.new_name)
        log.append(text_report.display_labeled_list(_('Total of related files'), text_report.display_pairs_list(self.related_files_copy)))
        log.append(text_report.display_labeled_list(_('Total of files in package'), text_report.display_pairs_list(self.href_files_copy)))
        log.append(text_report.display_labeled_list(_('Total of @href in XML'), text_report.display_pairs_list(self.renamed_href_items)))
        log.append(text_report.display_labeled_list(_('Total of files not found in package'), self.missing_href_files))
        return '\n'.join(log)


class MarkupPackage(object):

    def __init__(self, sgmlxml_filename, acron):
        self.acron = acron
        self.sgmlfile = fs_utils.File(sgmlxml_filename)
        self.wk_area = workarea.Workarea(os.path.dirname(self.sgmlfile.parent_path))
        self.sgmxml_outputs = workarea.OutputFiles(sgmlfile.name, self.wk_area.reports_path, sgmlfile.path)
        srcxmlfile = fs_utils.File(self.wk_area.src_path + '/' + self.sgmlfile.name + '.xml')
        self.src_pkgfiles = pkg_files.ArticlePkgFiles(srcxmlfile)
        self.src_pkgfiles.tiff2jpg()

    def _generate_xml(self, xmlfile):
        sgmlxmldoc = SGMLXMLDocument(self.sgmlfile, self.src_pkgfiles)
        sgmlxmldoc.fix()
        self.mkp_href_info_items = sgmlxmldoc.href_files_info
        xsl = xml_versions.xsl_getter(sgmlxmldoc.sps_version)
        java_xml_utils.xml_transform(self.sgmlfile.filename, xsl, xmlfile.filename)

    def _generate_pack_xml(self):
        pkg_renamer = PackageRenamed(self.src_pkgfiles, self.mkp_href_info_items)
        pkg_renamer.rename(self.acron, self.wk_area.scielo_pkg_path)
        self.xml_pkgfiles = pkg_renamer.dest_pkgfiles
        self.xml_pkgfiles.previous_name = self.src_pkgfiles.name
        self.renamed_href_items = pkg_renamer.renamed_href_items
        self.pkg_generation_report = pkg_renamer.report()

    def _normalize_xml(self, xmlfile):
        spsxmlcontent = sps_document.SPSXMLContent(xmlfile.content, xmlfile.path)
        spsxmlcontent.normalize()
        xmlfile.content = spsxmlcontent.content
        xmlfile.write()

    def report(self):
        msg = self.invalid_xml_message
        if msg == '':
            msg = self.pkg_generation_report
            img_reports = ImageFilesOriginReport(self.mkp_href_info_items, self.renamed_href_items, self.xml_pkgfiles.file.path)
            html_reports.save(self.sgmxml_outputs.images_report_filename, '', img_reports.report())
        fs_utils.write_file(self.sgmxml_outputs.mkp2xml_report_filename, msg)

    @property
    def invalid_xml_message(self):
        msg = ''
        if self.src_pkgfiles.article is None:
            messages = []
            messages.append(self.xml_error)
            messages.append(validation_status.STATUS_ERROR + ': ' + _('Unable to load {xml}. ').format(xml=self.xml_pkgfiles.file.filename) + '\n' + _('Open it with XML Editor or Web Browser to find the errors easily. '))
            msg = '\n'.join(messages)
        return msg

    def make(self):
        self._generate_xml(self.src_pkgfiles.file)
        self._generate_pack_xml()
        self._normalize_xml(self.dest_pkgfiles.file)
        self.report()


class ImageFilesOriginReport(object):

    def __init__(self, mkp_files_origin, renamed_href_items, package_path):
        self.package_path = package_path
        self.renamed_href_items = dict(renamed_href_items)
        self.mkp_files_origin = mkp_files_origin

    def report(self):
        rows = []
        if len(self.renamed_href_items) == 0:
            rows.append(html_reports.tag('h4', _('Article has no image')))
        else:
            rows.append('<ol>')
            for item in self.mkp_files_origin:
                rows.append(self.item_report(item))
            rows.append('</ol>')
        return html_reports.tag('h2', _('Images Origin Report')) + ''.join(rows)

    def item_report(self, item):
        renamed_href_items = dict(self.renamed_href_items)
        img_elem_info = '{} {}'.format(item.get('name'), item.get('id'))
        chosen_name = item.get('pkg_elem_href')
        pkg_elem_origin = item.get('pkg_elem_origin')
        pkg_elem_from_src = item.get('pkg_elem_from_src')
        pkg_elem_from_doc = item.get('pkg_elem_from_doc')

        elem_name = item.get('name')
        style = elem_name if elem_name in ['tabwrap', 'figgrp', 'equation'] else 'inline'
        rows = []
        rows.append('<li>')
        rows.append(html_reports.tag('h3', img_elem_info))
        rows.append(self.item_report_replacement(chosen_name, renamed_href_items.get(chosen_name)))
        rows.append(html_reports.tag('h4', pkg_elem_origin))
        rows.append('<div class="compare_images">')
        rows.append(self.display_image(self.package_path + '/' + renamed_href_items.get(chosen_name), "compare_" + style, pkg_elem_origin))
        if pkg_elem_from_src is not None:
            rows.append(self.display_image(pkg_elem_from_src, "compare_" + style, 'src'))
        if pkg_elem_from_doc is not None:
            rows.append(self.display_image(pkg_elem_from_doc, "compare_" + style, 'doc'))
        rows.append('</div>')
        rows.append('</li>')
        return '\n'.join(rows)

    def item_report_replacement(self, name, renamed):
        return html_reports.tag('h4', renamed if name == renamed else name + ' => ' + renamed)

    def display_image(self, img_filename, style, title):
        rows = []
        if title is not None:
            rows.append(html_reports.tag('h5', title))
        img_filename = 'file://' + img_filename.replace('.tiff', '.jpg').replace('.tif', '.jpg')
        return '<div class="{}">'.format(style) + html_reports.link(img_filename, html_reports.image(img_filename)) + '</div>'


def get_numbers(element_id):
    numbers = [i for i in element_id if i.isdigit()]
    return int(numbers)
