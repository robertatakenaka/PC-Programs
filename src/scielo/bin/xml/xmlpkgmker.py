# coding=utf-8

import random
import os
import shutil
import tempfile
from datetime import datetime
import xml.etree.ElementTree as etree

from StringIO import StringIO

#xml_tags_which_has_href = ['graphic', 'inline-graphic', 'media', 'abbrev', 'award-group', 'bio', 'chem-struct', 'collab', 'conference', 'contrib', 'element-citation', 'email', 'ext-link', 'funding-source', 'inline-supplementary-material', 'institution', 'license', 'long-desc', 'mixed-citation', 'named-content', 'nlm-citation', 'product', 'related-article', 'related-object', 'self-uri', 'supplementary-material', 'uri']

xml_tags_which_has_href = ['graphic', 'inline-graphic', 'media', 'chem-struct', 'inline-supplementary-material', 'supplementary-material', ]
sgml_tags_which_has_href = ['graphic', 'supplmat', ]

try:
    import Image
    IMG_CONVERTER = True
except:
    IMG_CONVERTER = False

#from datetime import datetime

DEBUG = 'OFF'
# global variables
THIS_LOCATION = os.path.dirname(os.path.realpath(__file__))

CONFIG_JAVA_PATH = 'java'
CONFIG_JAR_PATH = THIS_LOCATION + '/../jar'
CONFIG_ENT_TABLE_PATH = THIS_LOCATION
CONFIG_VERSIONS_PATH = THIS_LOCATION + '/../pmc'


JAVA_PATH = CONFIG_JAVA_PATH
JAR_TRANSFORM = CONFIG_JAR_PATH + '/saxonb9-1-0-8j/saxon9.jar'
JAR_VALIDATE = CONFIG_JAR_PATH + '/XMLCheck.jar'
ENTITIES_TABLE_FILENAME = CONFIG_ENT_TABLE_PATH + '/entities2char'


def display_xml_in_html(node):
    if node is not None:
        return '<pre>' + etree.tostring(node).replace('<', '&lt;').replace('>', '&gt;') + '</pre>'
    return ''


def startswith_invalid_char(content):
    return content[0:1] in [' ', ',', '.', '-']


def endswith_invalid_char(content):
    return content[-1:] in [' ', ',', '-']


def log_images_errors(filename, label, files):
    files = [item for item in files if item is not None]
    if len(files) > 0:
        f = open(filename, 'a+')
        f.write('\n\n%s:\n%s\n%s' % (label, '=' * len(label), '\n'.join(files)) + '\n')
        f.close()


def log_message(filename, message):
    if message:
        f = open(filename, 'a+')
        f.write(message + '\n')
        f.close()


def configure_versions_location():
    PMC_PATH = CONFIG_VERSIONS_PATH
    version_configuration = {}
    version_configuration['3.0'] = {}
    version_configuration['3.0']['sgm2xml'] = PMC_PATH + '/v3.0/xsl/sgml2xml/sgml2xml.xsl'

    version_configuration['3.0']['scielo'] = {}
    version_configuration['3.0']['scielo']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">'
    version_configuration['3.0']['scielo']['dtd'] = PMC_PATH + '/v3.0/dtd/journalpublishing3.dtd'
    version_configuration['3.0']['scielo']['css'] = PMC_PATH + '/v3.0/xsl/web/plus'
    version_configuration['3.0']['scielo']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/scielo-style/stylechecker.xsl'
    version_configuration['3.0']['scielo']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
    version_configuration['3.0']['scielo']['xsl_preview'] = PMC_PATH + '/v3.0/xsl/previewers/scielo-html-novo.xsl'
    version_configuration['3.0']['scielo']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/xml2pmc.xsl'

    version_configuration['3.0']['pmc'] = {}
    version_configuration['3.0']['pmc']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN" "{DTD_FILENAME}">'
    version_configuration['3.0']['pmc']['dtd'] = PMC_PATH + '/v3.0/dtd/journalpublishing3.dtd'
    version_configuration['3.0']['pmc']['css'] = PMC_PATH + '/v3.0/xsl/jpub/jpub-preview.css'
    version_configuration['3.0']['pmc']['xsl_prep_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/nlm-stylechecker.xsl'
    version_configuration['3.0']['pmc']['xsl_report'] = PMC_PATH + '/v3.0/xsl/nlm-style-4.6.6/style-reporter.xsl'
    version_configuration['3.0']['pmc']['xsl_preview'] = [PMC_PATH + '/v3.0/xsl/jpub/citations-prep/jpub3-PMCcit.xsl', PMC_PATH + '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
    #version_configuration['3.0']['pmc']['xsl_preview'] = None
    version_configuration['3.0']['pmc']['xsl_output'] = PMC_PATH + '/v3.0/xsl/sgml2xml/pmc.xsl'

    version_configuration['j1.0'] = {}
    version_configuration['j1.0']['sgm2xml'] = PMC_PATH + '/j1.0/xsl/sgml2xml/sgml2xml.xsl'

    version_configuration['j1.0']['scielo'] = {}
    version_configuration['j1.0']['scielo']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'

    version_configuration['j1.0']['scielo']['dtd'] = PMC_PATH + '/j1.0/dtd/jats1.0/JATS-journalpublishing1.dtd'
    version_configuration['j1.0']['scielo']['css'] = version_configuration['3.0']['scielo']['css']
    version_configuration['j1.0']['scielo']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/scielo-style/stylechecker.xsl'
    version_configuration['j1.0']['scielo']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.2/style-reporter.xsl'
    version_configuration['j1.0']['scielo']['xsl_preview'] = version_configuration['3.0']['scielo']['xsl_preview']
    version_configuration['j1.0']['scielo']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/xml2pmc.xsl'

    version_configuration['j1.0']['pmc'] = {}
    version_configuration['j1.0']['pmc']['doctype'] = '<!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN" "{DTD_FILENAME}">'
    version_configuration['j1.0']['pmc']['dtd'] = PMC_PATH + '/j1.0/dtd/jats1.0/JATS-journalpublishing1.dtd'
    version_configuration['j1.0']['pmc']['css'] = version_configuration['3.0']['pmc']['css']
    version_configuration['j1.0']['pmc']['xsl_prep_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.2/nlm-stylechecker.xsl'
    version_configuration['j1.0']['pmc']['xsl_report'] = PMC_PATH + '/j1.0/xsl/nlm-style-5.2/style-reporter.xsl'
    version_configuration['j1.0']['pmc']['xsl_preview'] = [PMC_PATH + '/j1.0/xsl/jpub/citations-prep/jpub1-PMCcit.xsl', PMC_PATH + '/v3.0/xsl/previewers/jpub-main-jpub3-html.xsl', ]
    #version_configuration['j1.0']['pmc']['xsl_preview'] = None
    version_configuration['j1.0']['pmc']['xsl_output'] = PMC_PATH + '/j1.0/xsl/sgml2xml/pmc.xsl'
    return version_configuration


###
def format_parameters(parameters):
    r = ''
    for k, v in parameters.items():
        if v != '':
            if ' ' in v:
                r += k + '=' + '"' + v + '" '
            else:
                r += k + '=' + v + ' '
    return r


### ENTITIES
class EntitiesTable:
    def __init__(self, filename='entities'):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        self.table_number2char = {}
        self.table_named2char = {}

        for line in lines:
            values = line.replace("\n", "").split('|')
            if len(values) != 5:
                print(line)
            else:
                char, number_ent, named_ent, ign2, no_accent = values
                if number_ent == '&#124;':
                    char = '|'
                if named_ent in ['&gt;', '&lt;', '&amp;']:
                    char = named_ent
                    #entity_char = named_ent.replace('&','').replace(';','')
                self.table_number2char[number_ent] = char
                if '&#x' in number_ent:
                    hex_ent = number_ent[2:-1]
                    dec_ent = str(int('0' + hex_ent, 16))
                    self.table_number2char['&#' + dec_ent + ';'] = char
                elif '&#' in number_ent:
                    dec_ent = number_ent[2:-1]
                    hex_ent = hex(int(dec_ent))
                    self.table_number2char['&#' + hex_ent[hex_ent.find('x'):] + ';'] = char
                    #self.table_number2char['&#x' + hex_ent[hex_ent.find('x')+1:].upper() + ';'] = char

                self.table_named2char[named_ent] = char
        try:
            f = open('ent_teste.txt', 'w')
            f.write('\n'.join(self.table_number2char.keys()))
            f.close()
        except:
            pass

    def is_valid_char(self, char):
        return (char != '' and not char in ['>', '<', '&'])

    def is_valid_named(self, named):
        return (named != '' and not named in ['&gt;', '&lt;', '&amp;'])

    def ent2chr(self, ent):
        r = self.table_number2char.get(ent, None)
        if r is None:
            r = self.table_named2char.get(ent, None)
        if r is None:
            r = ent
        return r


def convert_using_htmlparser(content):
    import HTMLParser
    entities = []

    h = HTMLParser.HTMLParser()
    new = content.replace('&', '_BREAK_&')
    parts = new.split('_BREAK_')
    for part in parts:
        if part.startswith('&'):
            ent = part[0:part.find(';')+1]
            if not ent in entities:
                try:
                    new_ent = h.unescape(ent).encode('utf-8', 'xmlcharrefreplace')
                except Exception as inst:
                    new_ent = ent
                    print('convert_using_htmlparser:')
                    print(ent)
                    print(inst)
                if not new_ent in ['<', '>', '&']:
                    content = content.replace(ent, new_ent)
                entities.append(ent)
    return content


def convert_ent_to_char(content, entities_table=None):
    def prefix_ent(N=7):
        return ''.join(random.choice('^({|~_`!QZ[') for x in range(N))

    not_found_named = []
    not_found_number = []
    if '&' in content:
        PREFIX_ENT = prefix_ent()
        while PREFIX_ENT in content:
            PREFIX_ENT = prefix_ent()

        ALLOWED_ENTITIES = {'&gt;': PREFIX_ENT + 'gt;', '&lt;': PREFIX_ENT + 'lt;', '&amp;': PREFIX_ENT + 'amp;', }
        for ent, new_ent in ALLOWED_ENTITIES.items():
            content = content.replace(ent, new_ent)

        if '&' in content:
            content = convert_using_htmlparser(content)

        if '&' in content:
            if entities_table:
                while '&' in content:
                    ent = content[content.find('&'):]
                    ent = ent[0:ent.find(';')+1]
                    char = entities_table.ent2chr(ent)
                    if char == ent:
                        content = content.replace(ent, ent.replace('&', PREFIX_ENT))
                        if '&#' in ent:
                            not_found_number.append(ent)
                        else:
                            not_found_named.append(ent)
                    else:
                        try:
                            content = content.replace(ent, char)
                        except Exception as e:
                            print(ent)
                            print(char)
                            print(e)

        if not_found_named:
            f = open('unknown_ent_named.txt', 'a+')
            f.write('\n'.join(not_found_named))
            f.close()
        if not_found_number:
            f = open('unknown_ent_number.txt', 'a+')
            f.write('\n'.join(not_found_number))
            f.close()
        content = content.replace(PREFIX_ENT, '&')

    return content


def convert_entities(content, entities_table=None):
    return convert_ent_to_char(content, entities_table)
    #return convert_entname(content, entities_table)


def convert_entname(content, entities_table=None):
    def prefix_ent(N=7):
        return ''.join(random.choice('^({|~_`!QZ[') for x in range(N))

    not_found_named = []

    if '&' in content:
        PREFIX_ENT = prefix_ent()
        while PREFIX_ENT in content:
            PREFIX_ENT = prefix_ent()

        ALLOWED_ENTITIES = {'&gt;': PREFIX_ENT + 'gt;', '&lt;': PREFIX_ENT + 'lt;', '&amp;': PREFIX_ENT + 'amp;', }
        for ent, new_ent in ALLOWED_ENTITIES.items():
            content = content.replace(ent, new_ent)

        if '&' in content:
            import HTMLParser
            h = HTMLParser.HTMLParser()
            try:
                content = h.unescape(content).decode('utf-8')
            except:
                #print('Unable to use h.unescape')
                pass

        content = content.replace('&#', PREFIX_ENT + '#')

        if '&' in content:
            if entities_table:
                while '&' in content:
                    ent = content[content.find('&'):]
                    ent = ent[0:ent.find(';')+1]

                    char = entities_table.ent2chr(ent)
                    if char == ent:
                        content = content.replace(ent, ent.replace('&', PREFIX_ENT))
                        not_found_named.append(ent)
                    else:
                        content = content.replace(ent, char)

        if not_found_named:
            f = open('unknown_ent_named.txt', 'a+')
            f.write('\n'.join(not_found_named))
            f.close()

        content = content.replace(PREFIX_ENT, '&')

    return content


### IMAGES
def img_to_jpeg(image_filename, jpg_path, replace=False):
    r = True
    if image_filename.endswith('.tiff') or image_filename.endswith('.eps') or image_filename.endswith('.tif'):
        image_name = os.path.basename(image_filename)
        jpg_filename = jpg_path + '/' + image_name[0:image_name.rfind('.')] + '.jpg'

        if not os.path.exists(jpg_filename) or replace:
            try:
                im = Image.open(image_filename)
                im.thumbnail(im.size)
                im.save(jpg_filename, "JPEG")
            except Exception as inst:
                if DEBUG == 'ON':
                    print('Unable to convert ')
                    print(image_filename)
                    print('to')
                    print(jpg_filename)
                    print(inst)
                    print('')
        r = os.path.exists(jpg_filename)
    return r


def images_to_jpeg(img_path, jpg_path, replace=False):
    r = False
    failures = []
    files = [f for f in os.listdir(img_path) if f.endswith('.tiff') or f.endswith('.eps') or f.endswith('.tif')]
    for f in files:
        #jpg_filename = jpg_path + '/' + f[0:f.rfind('.')] + '.jpg'
        image_filename = img_path + '/' + f
        if not img_to_jpeg(image_filename, jpg_path):
            failures.append(image_filename)

    converted = len(files)-len(failures)
    if converted != len(files):
        print('Converted ' + str(converted) + '/' + str(len(files)))
        print('Not converted')
        print('\n'.join(failures))
    r = len(files) == converted
    return r


### XML
def xml_validate(xml_filename, result_filename, dtd_validation=False):
    validation_type = ''

    if dtd_validation:
        validation_type = '--validate'

    if os.path.exists(result_filename):
        os.unlink(result_filename)
    temp_result_filename = result_filename + '.tmp'
    if os.path.exists(temp_result_filename):
        os.unlink(temp_result_filename)

    cmd = JAVA_PATH + ' -cp ' + JAR_VALIDATE + ' br.bireme.XMLCheck.XMLCheck ' + xml_filename + ' ' + validation_type + '>' + temp_result_filename
    #print(cmd)
    os.system(cmd)

    if os.path.exists(temp_result_filename):
        f = open(temp_result_filename, 'r')
        result_content = f.read().replace(xml_filename, os.path.basename(xml_filename))
        f.close()

        if 'ERROR' in result_content.upper():
            f = open(xml_filename, 'r')

            n = 0
            s = ''
            for line in f.readlines():
                if n > 0:
                    s += str(n) + ':' + line
                n += 1
            result_content += '\n' + s
    else:
        result_content = 'ERROR: Not valid. Unknown error.' + "\n" + cmd

    if 'ERROR' in result_content.upper():
        f = open(temp_result_filename, 'w')
        f.write(result_content)
        f.close()
        valid = False
    else:
        valid = True

    shutil.move(temp_result_filename, result_filename)

    return valid


def xml_is_well_formed(content):
    return load_xml(content)


def load_xml(content):
    def ignore_entities_in_math(content):
        if '<math' in content:
            temp = content.replace('<math', 'BREAKBEGINCONSERTA<math').replace('</math>', '</math>BREAKBEGINCONSERTA')
            splited = temp.split('BREAKBEGINCONSERTA')
            replaces = [(repl, repl.replace('&', '_MATHENT_')) for repl in splited if '</math>' in repl]
            for find, replace in replaces:
                content = content.replace(find, replace)
        return content
    if not '<' in content:
        # is a file
        try:
            r = etree.parse(content)
        except Exception as e:
            content = open(content, 'r').read()
    content = ignore_entities_in_math(content)
    if '<' in content:
        try:
            r = etree.parse(StringIO(content))
        except Exception as e:
            print('XML is not well formed')
            print(e)
            r = None
    return r


def xml_content_transform(content, xsl_filename):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.close()
    fp = open(f.name, 'w')
    fp.write(content)
    fp.close()
    f2 = tempfile.NamedTemporaryFile(delete=False)
    f2.close()
    if xml_transform(f.name, xsl_filename, f2.name):
        fp = open(f2.name, 'r')
        content = fp.read()
        fp.close()
        os.unlink(f2.name)
    if os.path.exists(f.name):
        os.unlink(f.name)
    return content


def xml_transform(xml_filename, xsl_filename, result_filename, parameters={}):
    error = False
    name = os.path.basename(result_filename)

    if os.path.exists(result_filename):
        os.unlink(result_filename)
    temp_result_filename = result_filename + '.tmp'
    if os.path.exists(temp_result_filename):
        os.unlink(temp_result_filename)
    cmd = JAVA_PATH + ' -jar ' + JAR_TRANSFORM + ' -novw -w0 -o "' + temp_result_filename + '" "' + xml_filename + '"  "' + xsl_filename + '" ' + format_parameters(parameters)

    print('Creating ' + name)
    os.system(cmd)
    #print(cmd)
    if not os.path.exists(temp_result_filename):
        print('  ERROR: Unable to create it.')

        f = open(temp_result_filename, 'w')
        f.write('ERROR: transformation error.\n')
        f.write(xml_filename)
        f.write(xsl_filename)
        f.write(result_filename)
        f.write(cmd)
        error = True

    shutil.move(temp_result_filename, result_filename)

    return (not error)


def tranform_in_steps(xml_filename, xsl_list, result_filename, parameters={}, fix_dtd_location=''):
    input_filename = xml_filename + '.in'
    output_filename = xml_filename + '.out'
    error = False

    shutil.copyfile(xml_filename, input_filename)
    if os.path.exists(result_filename):
        os.unlink(result_filename)

    for xsl in xsl_list:
        r = xml_transform(input_filename, xsl, output_filename, parameters)
        if r:
            if fix_dtd_location:
                f = open(output_filename, 'r')
                c = f.read()
                f.close()
                find = '"' + os.path.basename(fix_dtd_location) + '"'
                if find in c:
                    c = c.replace(find, '"' + fix_dtd_location + '"')
                    f = open(output_filename, 'w')
                    f.write(c)
                    f.close()
            shutil.copyfile(output_filename, input_filename)
        else:
            error = True
            break

    if os.path.exists(input_filename):
        os.unlink(input_filename)
    shutil.move(output_filename, result_filename)
    return not error


###
class XMLString(object):

    def __init__(self, content):
        self.content = content

    def fix_dtd_location(self, dtd_filename, doctype):
        if not dtd_filename in self.content:
            if not '<?xml ' in self.content:
                self.content = '<?xml version="1.0" encoding="utf-8"?>\n' + self.content

            if '<!DOCTYPE' in self.content:
                old_doctype = self.content[self.content.find('<!DOCTYPE'):]
                old_doctype = old_doctype[0:old_doctype.find('>')+1]
                self.content = self.content.replace(old_doctype, '')
            if not '<!DOCTYPE' in self.content:
                self.content = self.content.replace('\n<article ', doctype.replace('{DTD_FILENAME}', dtd_filename) + '\n<article ')

    def fix(self):
        self.content = self.content[0:self.content.rfind('>')+1]
        self.content = self.content[self.content.find('<'):]
        self.content = self.content.replace(' '*2, ' '*1)
        if not xml_is_well_formed(self.content) is None:
            self._fix_style_tags()
            if not xml_is_well_formed(self.content) is None:
                self._fix_open_close()
                xml_is_well_formed(self.content)

    def _fix_open_close(self):
        changes = []
        parts = self.content.split('>')
        for s in parts:
            if '<' in s:
                if not '</' in s and not '<!--' in s and not '<?' in s:

                    s = s[s.find('<')+1:]
                    if ' ' in s and not '=' in s:
                        test = s[s.find('<')+1:]
                        changes.append(test)
        for change in changes:
            print(change)
            self.content = self.content.replace('<' + test + '>', '[' + test + ']')

    def _fix_style_tags(self):
        rcontent = self.content
        tags = ['italic', 'bold', 'sub', 'sup']
        tag_list = []
        for tag in tags:
            tag_list.append('<' + tag + '>')
            tag_list.append('</' + tag + '>')
            rcontent = rcontent.replace('<' + tag + '>',  'BREAKBEGINCONSERTA<' + tag + '>BREAKBEGINCONSERTA').replace('</' + tag + '>', 'BREAKBEGINCONSERTA</' + tag + '>BREAKBEGINCONSERTA')
        if self.content != rcontent:
            parts = rcontent.split('BREAKBEGINCONSERTA')
            self.content = self._fix_problem(tag_list, parts)

    def _fix_problem(self, tag_list, parts):
        expected_close_tags = []
        ign_list = []
        k = 0
        for part in parts:
            if part in tag_list:
                tag = part
                print('\ncurrent:' + tag)
                if tag.startswith('</'):
                    print('expected')
                    print(expected_close_tags)
                    print('ign_list')
                    print(ign_list)
                    if tag in ign_list:
                        print('remove from ignore')
                        ign_list.remove(tag)
                        parts[k] = ''
                    else:
                        matched = False
                        if len(expected_close_tags) > 0:
                            matched = (expected_close_tags[-1] == tag)

                            if not matched:
                                print('not matched')

                                while not matched and len(expected_close_tags) > 0:

                                    ign_list.append(expected_close_tags[-1])
                                    parts[k-1] += expected_close_tags[-1]
                                    del expected_close_tags[-1]

                                    matched = (expected_close_tags[-1] == tag)

                                print('...expected')
                                print(expected_close_tags)
                                print('...ign_list')
                                print(ign_list)

                            if matched:
                                del expected_close_tags[-1]
                else:
                    expected_close_tags.append(tag.replace('<', '</'))
            k += 1
        return ''.join(parts)


class XMLMetadata:
    def __init__(self, content):
        self.root = load_xml(content)

    def _fix_issue_number(self, num, suppl=''):
        if num != '':
            if 'pr' in num:
                num = num.replace(' pr', '')
            else:
                parts = num.split()
                if len(parts) == 3:
                    num = parts[0]
                    suppl = parts[2]
                elif len(parts) == 2:
                    if 'sup' in parts[1].lower():
                        num, suppl = parts
                    elif 'sup' in parts[0].lower():
                        num = ''
                        suppl = parts[1]

        return [num, suppl]

    def _meta_xml(self, node):
        issn, volid, issueno, suppl, fpage, order = ['', '', '', '', '', '']
        issn = self.root.findtext('.//front/journal-meta/issn[1]')
        volid = node.findtext('./volume')
        issueno = node.findtext('./issue')
        suppl = node.findtext('./supplement')

        if volid is None:
            volid = ''
        if issueno is None:
            issueno = ''
        if suppl is None:
            suppl = ''

        issueno, suppl = self._fix_issue_number(issueno, suppl)
        order = node.findtext('.//article-id[@pub-id-type="other"]')
        fpage_node = node.find('./fpage')
        elocation_id = node.findtext('./elocation-id')

        if fpage_node is not None:
            fpage = fpage_node.text
            seq = fpage_node.attrib.get('seq')
        else:
            fpage = None
            seq = None
        if fpage is not None:
            if fpage.isdigit():
                fpage = str(int(fpage))
        if fpage is not None:
            if fpage == '0':
                fpage = None
        return [issn, volid, issueno, suppl, fpage, seq, elocation_id, order]

    def _metadata(self):
        issn, volid, issueno, suppl, fpage, seq, elocation_id, order = ['', '', '', '', '', '', '', '']
        if self.root:

            node = self.root.find('.//article-meta')
            if node is not None:
                issn, volid, issueno, suppl, fpage, seq, elocation_id, order = self._meta_xml(node)
            else:
                attribs = self.root.find('.').attrib
                issn = attribs.get('issn')
                volid = attribs.get('volid')
                issueno = attribs.get('issueno')
                supplvol = attribs.get('supplvol', '')
                supplno = attribs.get('supplno', '')
                suppl = supplno if supplno else supplvol
                fpage = attribs.get('fpage')
                seq = ''
                #seq = attribs.get('order')
                order = attribs.get('order')
                if issueno == 'ahead':
                    issueno = '00'
                    volid = '00'
        return [issn, volid, issueno, suppl, fpage, seq, elocation_id, order]

    def format_name(self, data, param_acron='', param_order=''):

        r = ''
        if data:
            issn, vol, issueno, suppl, fpage, seq, elocation_id, order = data

            if elocation_id is not None:
                page_or_order = elocation_id
            else:
                if fpage is not None:
                    page_or_order = fpage
                    if seq is not None:
                        page_or_order += '-' + seq
                elif order is not None:
                    page_or_order = order

                page_or_order = '00000' + page_or_order
                page_or_order = page_or_order[-5:]

            if issueno:
                issueno = '00' + issueno
                issueno = issueno[-2:]

            if suppl:
                suppl = 's' + suppl if suppl != '0' else 'suppl'

            issueid = []
            for item in [vol, issueno, suppl]:
                if item != '' and item is not None:
                    issueid.append(item)
            issueid = '-'.join(issueid)

            r = '-'.join([issn, param_acron, issueid, page_or_order])

        return r

    def xml_data_href_filenames(self):
        # g for graphics
        # i for inline
        # e for equation
        # s for supplementary
        #xml_tags_which_has_href = ['graphic', 'inline-graphic', 'media', 'chem-struct', 'inline-supplementary-material', 'supplementary-material', ]
        #sgml  = ['graphic', 'supplmat']
        tags_has_href = list(set(xml_tags_which_has_href + sgml_tags_which_has_href))
        
        href_list = {}
        invalid_attrib_id = []
        for tag in tags_has_href:
            # find parent of nodes which has @href
            nodes = self.root.findall('.//*[' + tag + ']')
            for node in nodes:
                attrib_id = node.attrib.get('id', '')
                filename = node.attrib.get('filename', None)
                if attrib_id == '':
                    attrib_id = node.find(tag).attrib.get('id', '')
                href = node.find(tag).attrib.get('{http://www.w3.org/1999/xlink}href', None)
                if href is None or href == '':
                    href = filename
                if not href is None:
                    if 'suppl' in tag or 'media' == tag:
                        suffix = 's'
                    elif 'inline' in tag:
                        suffix = 'i'
                    elif node.tag in ['equation', 'disp-formula']:
                        suffix = 'e'
                    else:
                        suffix = 'g'

                    if attrib_id == '':
                        attrib_id = '_' + str(len(invalid_attrib_id) + 1)
                        invalid_attrib_id.append(attrib_id)
                        suffix = 'g'
                    href_list[href] = suffix + attrib_id
                    
        return href_list

    def old_xml_data_href_filenames(self):
        r = {}

        for tag in ['fig', 'figgrp', 'tabwrap', 'equation', 'inline-display']:

            nodes = self.root.findall('.//' + tag)

            for n in nodes:
                if n.attrib.get('id') is not None:
                    id = n.attrib.get('id', '')
                    if '-' in id:
                        id = id[id.rfind('-')+1:]
                    if n.tag == 'equation':
                        id = 'e' + id
                    elif n.tag == 'inline-display':
                        id = 'i' + id
                    else:
                        id = 'g' + id
                    graphic_nodes = n.findall('graphic')

                    for graphic_node in graphic_nodes:
                        for attrib_name in graphic_node.attrib:
                            if 'href' in attrib_name:
                                href = graphic_node.attrib.get(attrib_name)
                                r[href] = id
                if n.attrib.get('filename') is not None:
                    r[n.attrib.get('filename')] = id

        return r

    def new_names_and_embedded_files(self, acron, alternative_id=''):
        new_name = self.format_name(self._metadata(), acron, alternative_id)
        href_filenames = self.xml_data_href_filenames()
        href_files = self.new_href_list(new_name, href_filenames)
        return (new_name, href_files)

    def new_href_list(self, new_name, href_filenames):
        items = []
        for href, suffix in href_filenames.items():
            items.append((href, new_name + '-' + suffix))
        return items

    def new_name_and_href_list(self, acron, alternative_id=''):
        #usado pela versao XPM5
        """
        return (new name, [(@href, suffix + parent id)])
        """
        new_name = self.format_name(self._metadata(), acron, alternative_id)
        href_filenames = self.xml_data_href_list()
        return (new_name, href_filenames)

    def xml_data_href_list(self):
        #usado pela versao XPM5
        # g for graphics
        # i for inline
        # e for equation
        # s for supplementary
        #xml_tags_which_has_href = ['graphic', 'inline-graphic', 'media', 'chem-struct', 'inline-supplementary-material', 'supplementary-material', ]
        #sgml  = ['graphic', 'supplmat']
        tags_has_href = list(set(xml_tags_which_has_href + sgml_tags_which_has_href))
        href_list = []
        invalid_attrib_id = []
        for tag in tags_has_href:
            # find parent of nodes which has @href
            nodes = self.root.findall('.//*[' + tag + ']')
            for node in nodes:
                attrib_id = node.attrib.get('id', '')
                filename = node.attrib.get('filename', None)
                if attrib_id == '':
                    attrib_id = node.find(tag).attrib.get('id', '')
                href = node.find(tag).attrib.get('{http://www.w3.org/1999/xlink}href', None)
                if href is None or href == '':
                    href = filename
                if not href is None:
                    if 'suppl' in tag or 'media' == tag:
                        suffix = 's'
                    elif 'inline' in tag:
                        suffix = 'i'
                    elif node.tag in ['equation', 'disp-formula']:
                        suffix = 'e'
                    else:
                        suffix = 'g'

                    if attrib_id == '':
                        attrib_id = '_' + str(len(invalid_attrib_id) + 1)
                        invalid_attrib_id.append(attrib_id)
                        suffix = 'g'
                    href_list.append((href, suffix + attrib_id))
                    
        return href_list    


class IDsReport(object):
    def __init__(self, node):
        self.root = node

    def generate_report(self):
        content = ''
        subarticles = {}

        elements = ['aff', 'fig', 'table-wrap', 'equation', 'fn'] + list(set([elem.tag for elem in self.root.findall('.//*[@id]')]))
        elements = list(set(elements))

        for elem_name in elements:
            totals, article, subarticles = self.get_matched_nodes(elem_name)
            if max(totals.values()) > 0:
                content += '<div class="CSS_Table_bicolor"><table>'
                content += '<tr><td>position/total</td><td>ID</td><td>article or subarticle</td><td>' + elem_name + '. Quantity found: ' + self.warning_totals(totals, elem_name) + '</td></tr>'

                for k in range(0, max(totals.values())):
                    art = article[k] if len(article) > k else None
                    content += self.display_data(art, subarticles, k, str(k+1) + '/' + str(max(totals.values())))
                    content += '<tr><td colspan="4"></td></tr>'
                content += '</table></div>'
        return content

    def warning_totals(self, totals, element_name):
        return ', '.join([str(v) + ' (in ' + k + ')' for k, v in totals.items()])
        
    def get_matched_nodes(self, element_name):
        totals = {}

        article_elements = self.root.findall('./front//' + element_name) + self.root.findall('./body//' + element_name) + self.root.findall('./back//' + element_name)
        totals['article'] = len(article_elements)
        k = 1
        subarticles_elements = {}
        for subart_node in self.root.findall('.//sub-article'):
            subart_id = subart_node.attrib.get('id', k)
            k += 1
            subarticles_elements[subart_id] = subart_node.findall('.//' + element_name)
            totals[subart_id] = len(subarticles_elements[subart_id])

        return (totals, article_elements, subarticles_elements)

    def display_data(self, article, subarticles, position, position_label):
        r = ''
        if article is None:
            r += '<tr><td>' + position_label + '</td><td>not found</td><td>article</td><td>not found</td></tr>'
        else:
            r += '<tr><td>' + position_label + '</td><td>' + article.attrib.get('id', '') + '</td><td>article</td><td>' + display_xml_in_html(article) + '</td></tr>'
        for subartid, subartdata in subarticles.items():
            if position < len(subartdata):
                r += '<tr><td>' + position_label + '</td><td>' + subartdata[position].attrib.get('id', '') + '</td><td>' + subartid + '</td><td>' + display_xml_in_html(subartdata[position]) + '</td></tr>'
            else:
                r += '<tr><td>' + position_label + '</td><td>not found</td><td>' + subartid + '</td><td>not found</td></tr>'
        return r


class HRefReport(object):
    def __init__(self, node, files):
        self.root = node
        self.files = files
        self.files_without_extensions = list(set([f[0:f.rfind('.')] for f in self.files]))

    def generate_report(self, xml_name):
        content = ''
        href_dict = {}
        xml_name = xml_name.replace('.xml', '')
        
        files = [f for f in self.files if f.startswith(xml_name + '-') or f.startswith(xml_name + '.')]
        
        elem_names = list(set([elem.tag for elem in self.root.findall('.//*[@{http://www.w3.org/1999/xlink}href]')]))
        for elem_name in elem_names:
            for parent in self.root.findall('.//*[' + elem_name + ']'):
                href_value = parent.find(elem_name).attrib.get('{http://www.w3.org/1999/xlink}href', None)
                if not href_value is None and not href_value.startswith('http'):
                    if href_dict.get(href_value, None) is None:
                        href_dict[href_value] = []
                    href_dict[href_value].append(parent)

        content += '<div class="CSS_Table_bicolor"><table>'
        content += '<tr><td></td><td>files in the package</td><td>href?</td></tr>'
        k = 0
        for f in files:
            k += 1
            test = 'yes' if (f in href_dict.keys() or f[0:f.rfind('.')] in href_dict.keys()) else 'no'
            content += '<tr><td>' + str(k) + '</td><td>' + f + '</td><td>' + test + '</td></tr>'
        content += '</table></div>'

        content += '<div class="CSS_Table_bicolor"><table>'
        content += '<tr><td></td><td>@href content</td><td>file exists?</td><td>href location</td></tr>'
        
        k = 0
        for href_key in sorted(href_dict.keys()):
            k += 1
            if len(href_dict[href_key]) > 1:
                content += '<tr><td colspan="4">' + href_key + ' occurres ' + str(len(href_dict[href_key])) + ' times</td></tr>'
            found = href_key in self.files
            if not found:
                found = href_key in self.files_without_extensions
            found = 'found' if found else 'not found'
            for item in href_dict[href_key]:
                content += '<tr><td>' + str(k) + '</td><td>' + href_key + '</td><td>' + found + '</td><td>' + display_xml_in_html(item) + '</td></tr>'
        content += '</table></div>'
        return content

    def warning_totals(self, totals, element_name):
        content = ''
        if len(list(set(totals.values()))) > 1:
            content += ', '.join([str(v) + '(in ' + k + ')' for k, v in totals.items()])
        return content

    def get_matched_nodes(self, element_name):
        totals = {}

        article_elements = self.root.findall('./front//' + element_name) + self.root.findall('./body//' + element_name) + self.root.findall('./back//' + element_name)
        totals['article'] = len(article_elements)
        k = 1
        subarticles_elements = {}
        for subart_node in self.root.findall('.//sub-article'):
            subart_id = subart_node.attrib.get('id', k)
            k += 1
            subarticles_elements[subart_id] = subart_node.findall('.//' + element_name)
            totals[subart_id] = len(subarticles_elements[subart_id])

        return (totals, article_elements, subarticles_elements)

    def display_data(self, article, subarticles, position, position_label):
        r = ''
        if article is None:
            r += '<tr><td>' + position_label + '</td><td>not found</td><td>article</td><td>not found</td></tr>'
        else:
            r += '<tr><td>' + position_label + '</td><td>' + article.attrib.get('id') + '</td><td>article</td><td><pre>' + display_xml_in_html(article) + '</td></tr>'
        for subartid, subartdata in subarticles.items():
            if position < len(subartdata):
                r += '<tr><td>' + position_label + '</td><td>' + subartdata[position].attrib.get('id') + '</td><td>' + subartid + '</td><td>' + display_xml_in_html(subartdata[position]) + '</td></tr>'
            else:
                r += '<tr><td>' + position_label + '</td><td>not found</td><td>' + subartid + '</td><td>not found</td></tr>'
        return r


class PkgReport(object):

    def __init__(self, pkg_path, report_path):
        self.pkg_path = pkg_path
        self.report_path = report_path

        self.lists = []
        self.lists.append(('Authors', 'authors.html', ['suffix', 'prefix', 'given-names', 'surname'], ['given-names', 'surname'], []))
        self.lists.append(('Publishers/Locations', 'publisher.html', ['type', 'publisher-name', 'publisher-loc'], [], []))
        self.lists.append(('Sources/Years', 'source.html', ['type', 'source', 'year'], ['type', 'source', 'year'], []))
        self.lists.append(('Affiliations', 'affs.html', ['xml', 'original', 'orgname', 'orgdiv1', 'orgdiv2', 'orgdiv3', 'city', 'state', 'country'], ['orgname', 'original'], ['city', 'state', 'country']))

    def load_data(self, xml_filename=None):
        self.filename_list = []

        self.content_validations = {}
        self.xml_content = {}

        if xml_filename is None:
            for filename in [f for f in os.listdir(self.pkg_path) if f.endswith('.xml')]:
                self._load_file(filename)
        else:
            if os.path.isfile(self.pkg_path + '/' + xml_filename):
                self._load_file(xml_filename)

    def _load_file(self, filename):
        node = load_xml(self.pkg_path + '/' + filename)
        if node is None:
            node = load_xml('<root></root>')
        self.filename_list.append(filename)
        self.xml_content[filename] = node
        self.content_validations[filename] = ContentValidation(node, filename)

    def statistics(self, messages):
        return '<div class="statistics"><p>Total of fatal errors = %s</p><p>Total of errors = %s</p><p>Total of warnings = %s</p></div>' % (str(len(messages.split('FATAL ERROR:')) - 1), str(len(messages.split('ERROR:')) - 1), str(len(messages.split('WARNING:')) - 1))

    def generate_articles_report(self, print_toc_report=True, old_names=None):
        expected_journal_meta = {}
        order_list = {}
        doi_list = {}
        order_is_zero = []
        order_ok = {}
        unordered = {}
        issue_header = ''
        html_report = HTMLReport()
        issue_label = ''
        pubdates = {}
        individual_errors = ''
        all_articles_errors = ''

        for filename in self.filename_list:
            content_validation = self.content_validations[filename]

            report_filename_prefix = filename.replace('.xml', '')
            if old_names is not None:
                report_filename_prefix = old_names[filename]

            id_report_content = '<h1>Report of @id</h1>' + IDsReport(self.xml_content[filename]).generate_report()
            html_report._html(self.report_path + '/' + report_filename_prefix + '_ids.html', '', html_report._css('toc') + html_report._css('bicolortable'), id_report_content)

            href_report_content = '<h1>Report of @href and files</h1>' + HRefReport(self.xml_content[filename], os.listdir(self.pkg_path)).generate_report(content_validation.filename)
            html_report._html(self.report_path + '/' + report_filename_prefix + '_href.html', '', html_report._css('toc') + html_report._css('bicolortable'), href_report_content)

            if expected_journal_meta == {}:
                for k, v in content_validation.issue_meta.items():
                    expected_journal_meta[k] = v
            expected_files = [f[0:f.rfind('.')] for f in os.listdir(self.pkg_path)]

            individual_fatal_errors = []
            #pubdate checking
            pubdate = content_validation.issue_date()
            if not pubdate in pubdates.keys():
                pubdates[pubdate] = []
            pubdates[pubdate].append(filename)
            # order checking
            order = content_validation.article_meta.get('order', 0)
            if order == 0:
                order_is_zero.append(content_validation.filename)
                row_idx = content_validation.filename
                individual_fatal_errors.append('<p class="error">ERROR: order must not be zero.</p>')
            else:
                if order in order_list.keys():
                    row_idx = content_validation.filename
                    individual_fatal_errors.append('<p class="error">ERROR: order is duplicated.</p>')
                else:
                    order_list[order] = []
                    row_idx = '00000' + str(order)
                    row_idx = row_idx[-5:]
            # doi checking
            doi = content_validation.article_meta.get('doi', None)
            if doi:
                if doi in doi_list.keys():
                    individual_fatal_errors.append('<p class="error">ERROR: doi is duplicated.</p>')
                else:
                    doi_list[doi] = []
                doi_list[doi].append(content_validation.filename)

            # validations
            content_validation.validations(expected_journal_meta, expected_files)

            individual_metadata = self._report_article_meta(content_validation)
            individual_errors = self._report_article_messages(content_validation, True)

            individual_lists = ''
            for title, report_filename, columns, required, desirable in self.lists:
                items = self.data_for_list(report_filename, content_validation)
                rows = self.data_in_table_format(content_validation.filename, items, columns, required, desirable)
                individual_lists += '<div class="list"><h1>' + title + '</h1>' + html_report.in_table_format(rows, columns) + '</div>'

            individual_header = ''.join(individual_fatal_errors) + individual_metadata
            individual_stat = self.statistics(individual_errors + ''.join(individual_fatal_errors))

            individual_report_content = '<h1>' + report_filename_prefix + '</h1>' + individual_stat + issue_header + '<div class="article">' + individual_header + individual_errors + '</div>' + individual_lists + id_report_content + href_report_content

            if row_idx.isdigit():
                order_ok[row_idx] = '<div class="article">' + individual_header + '</div>'
            else:
                unordered[row_idx] = '<div class="article">' + individual_header + '</div>'

            if not issue_header:
                # only once
                issue_header = self._report_journal_meta(content_validation)

            if not issue_label:
                # only once
                issue_label = content_validation.issue_label

            html_report._html(self.report_path + '/' + report_filename_prefix + '.contents.html', 'Report of contents validations required by SciELO', html_report._css('toc') + html_report._css('datareport') + html_report._css('bicolortable'), individual_report_content)
            all_articles_errors += individual_errors

        #issue_header +
        # doi, order, journal, sorted, unsorted.
        if print_toc_report:
            issue_errors = '<div class="issue-messages">'
            for k, v in doi_list.items():
                if len(v) > 1:
                    issue_errors += '<p>ERROR: %s is duplicated in %s</p>' % (k, ', '.join(v))
            for k, v in order_list.items():
                if len(v) > 1:
                    issue_errors += '<p>ERROR: %s is duplicated in %s</p>' % (k, ', '.join(v))
                if k == 0:
                    issue_errors += '<p>ERROR: %s is invalid value for %s</p>' % (k, ', '.join(v))
            if len(pubdates.items()) > 1:
                issue_errors += '<p>FATAL ERROR: All the articles must have the same value for pub-date/@date-type=pub or pub-date/@pub-type= ppub | epub-ppub | collection.</p>'
                for k, v in pubdates.items():
                    issue_errors += '<p> %s is a date in %s </p>' % (k, ', '.join(v))
            issue_errors += '</div>'

            toc_content = self.statistics(all_articles_errors + issue_errors) + issue_errors + issue_header

            keys = unordered.keys()
            keys.sort()
            for key in keys:
                toc_content += unordered[key]
            keys = order_ok.keys()
            keys.sort()
            for key in keys:
                toc_content += order_ok[key]
            html_report._html(self.report_path + '/toc.html', 'Report of contents validations required by SciELO', html_report._css('toc') + html_report._css('datareport'), '<h1>' + issue_label + '</h1>' + toc_content)

    def data_for_list(self, report_filename, content_validation):
        items = []
        if content_validation.xml is not None:
            if report_filename == 'authors.html':

                items = [author for author in content_validation.article_meta['author']]
                for ref in content_validation.refs:
                    for author in ref['author']:
                        a = {'id': ref.get('id', '')}
                        a.update(author)
                        items.append(a)
            elif report_filename == 'publisher.html':
                items = [content_validation.issue_meta] + content_validation.refs
            elif report_filename == 'source.html':
                items = content_validation.refs
            elif report_filename == 'affs.html':
                items = content_validation.article_meta['aff']
        return items

    def generate_lists(self):
        report = HTMLReport()
        issue_label = ''
        for title, report_filename, columns, required, desirable in self.lists:
            rows = []
            for filename in self.filename_list:
                content_validation = self.content_validations[filename]
                print(report_filename + ' (' + content_validation.filename + ')')
                items = self.data_for_list(report_filename, content_validation)
                rows += self.data_in_table_format(content_validation.filename, items, columns, required, desirable)
                if not issue_label:
                    issue_label = content_validation.issue_label

            report._html(self.report_path + '/' + report_filename, title, report._css('datareport') + report._css('toc'), '<h1>' + issue_label + '</h1>' + report.in_table_format(rows, columns))

    def data_in_table_format(self, filename, items, columns, required_items, desirable_items):
        rows = []
        # FIXME
        #print(required_items)

        for item in items:
            #print(item)
            row = {'id': filename, 'label': item.get('id', '')}
            for child in columns:
                row[child] = item.get(child, '')
                if row[child] == '' or row[child] is None:
                    if child in required_items:
                        row[child] = 'ERROR: Required data'
                    elif child in desirable_items:
                        row[child] = 'WARNING: Required data, if exists'
                else:
                    if not(row[child].strip()[0:1] == '<' and row[child].strip()[-1:] == '>'):
                        if startswith_invalid_char(row[child]):
                            row[child] = 'ERROR: %s starts with an invalid character (%s).' % (child, row[child][0:1])
                        if endswith_invalid_char(row[child]):
                            row[child] = 'ERROR: %s ends with an invalid character (%s).' % (child, row[child][-1:])
            #print(row)
            rows.append(row)
        return rows

    def _report_journal_meta(self, content_validation):
        data = '<div class="issue">'

        if content_validation.xml is not None:
            data += '<h2>%s, %s (%s)</h2>' % (content_validation.issue_meta.get('journal-title', ''), content_validation.issue_meta.get('volume', ''), content_validation.issue_meta.get('issue', ''))
            data += '<h3>nlm-ta: %s</h3>' % content_validation.issue_meta.get('nlm-ta', '')
            for item in ['eissn', 'pissn', 'publisher-name']:
                s = content_validation.issue_meta.get(item, '')
                if not s:
                    s = ''
                data += '<p>' + item + ': ' + s + '</p>'
        data += '</div>'
        return data

    #xxxx
    def _report_article_meta(self, content_validation):
        data = '<div class="article-data">'
        data += '<p class="filename">%s</p>' % content_validation.filename

        if content_validation.xml is None:
            data += '<h3>Invalid XML. Unable to read its data.</h3>'
        else:
            data += '<h2>%s</h2>' % content_validation.article_meta.get('subject', '')
            data += '<p class="article-type">%s</p>' % content_validation.article_meta.get('article-type', '')
            data += '<h3>[%s] %s</h3>' % (content_validation.article_meta.get('lang', '(missing language)'), content_validation.article_meta.get('article-title', ''))
            for lang, title in content_validation.article_meta.get('trans-title', {}).items():
                data += '<h4> [%s] %s</h4>' % (lang, title)

            data += '<p class="doi">%s</p>' % content_validation.article_meta.get('doi', '')

            for item in ['date-epub', 'date-ppub', 'date-epub-ppub', 'date-collection', 'date-pub', 'date-preprint']:
                data += '<p>' + item + ': ' + str(content_validation.article_meta.get(item, '')) + '</p>'
            data += '<p class="id">%s [fpage: <span class="fpage">%s</span> | fpage/@seq: <span class="fpage_seq">%s</span> | .//article-id[@pub-id-type="other"]: <span class="other-id">%s</span>]</p>' % (content_validation.article_meta['order'], content_validation.article_meta.get('fpage', ''), content_validation.article_meta.get('fpage_seq', ''), content_validation.article_meta.get('other id', ''))
            data += '<p class="fpage">pages: %s</p>' % (content_validation.article_meta.get('fpage', '') + '-' + content_validation.article_meta.get('lpage', ''))

            #data += '<p class="authors"></p>' % content_validation._format_as_table(content_validation.article_meta['author'], ['given-names', 'surname', 'prefix', 'suffix'])
            data += '<p class="sections">sections:<ul>%s</ul></p>' % ''.join(['<li>%s (%s)</li>' % (title, tp) for tp, title in content_validation.article_meta['text body sections']])

            items = []
            for author in content_validation.article_meta.get('author', []):
                prefix = '(%s) ' % author['prefix'] if author.get('prefix', None) is not None else ''
                suffix = ' (%s)' % author['suffix'] if author.get('suffix', None) is not None else ''

                if not author['surname']:
                    author['surname'] = 'ERROR: missing surname'
                if not author['given-names']:
                    author['given-names'] = 'ERROR: missing name'

                items.append(author['surname'] + suffix + ', ' + prefix + author['given-names'])
            data += '<p class="authors">authors: %s</p>' % '; '.join(items)

            data += '<p class="authors">collabs: %s</p>' % '; '.join(content_validation.article_meta.get('collab', []))

            if content_validation.article_meta.get('abstract', ''):
                data += '<p class="abstract"> [%s] %s</p>' % (content_validation.article_meta.get('lang', '??'), content_validation.article_meta.get('abstract', ''))

            for lang, abstract in content_validation.article_meta.get('trans-abstract', {}).items():
                data += '<p class="trans-abstract"> [%s] %s</p>' % (lang, abstract)

            kwg = content_validation.article_meta.get('kwd-group', {})
            if not kwg == {}:
                for lang, kwd_group in kwg.items():
                    kwd = '; '.join(kwd_group) if kwd_group else ''
                    data += '<p class="kwd-group">key words [%s]: %s</p>' % (lang, kwd)

            data += '<p class="ack">ack: %s</p><p class="funding">funding award-id: %s</p>' % (content_validation.article_meta['ack'], content_validation.article_meta['award-id'])
            data += '<p class="affs">%s</p>' % self._format_as_table(content_validation.article_meta['aff'], ['xml', 'original', 'orgname', 'orgdiv1', 'orgdiv2', 'orgdiv3', 'city', 'state', 'country', 'email'])

        data += '</div>'

        return data

    def _format_messages(self, messages):
        if messages is None:
            return ''
        elif isinstance(messages, (str, unicode)):
            return self._eval(messages)
        elif isinstance(messages, list):
            return ''.join([self._format_messages(item) for item in messages])
        elif isinstance(messages, dict):
            ref_messages = ''
            for label, msg in messages.items():
                if not label in ['id', 'xml']:
                    if isinstance(msg, (str, unicode)):
                        ref_messages += self._eval(msg)
                    elif msg is not None:
                        ref_messages += ''.join([self._format_messages(m) for m in msg])
            r = ''
            if not ref_messages == '':
                r = '<div class="group">'
                if 'id' in messages.keys():
                    r += '<p class="group-id">%s</p>' % messages['id']
                r += ref_messages
                if 'xml' in messages.keys():
                    r += '<p class="xml">%s</p>' % messages['xml'].replace('<', '&lt;').replace('>', '&gt;')
                r += '</div>'
            return r

    def _report_article_messages(self, content_validation, issue_msg=False):
        # self.article_meta_validations = {}
        # self.files_validations = ''
        # self.issue_meta_validations = None
        # self.refs_validations = []
        if content_validation.xml is None:
            return self._eval('ERROR: Invalid %s' % content_validation.filename)
        else:
            messages = []
            if issue_msg:
                messages.append(self._format_messages(content_validation.issue_meta_validations))
            messages.append(self._format_messages(content_validation.article_meta_validations))
            messages.append(self._format_messages(content_validation.files_validations))
            messages.append(self._format_messages(content_validation.refs_validations))
            return '<div class="article-messages">%s</div>' % ''.join(messages)

    def _report_issue_messages(self, content_validation):
        # self.article_meta_validations = {}
        # self.files_validations = ''
        # self.issue_meta_validations = None
        # self.refs_validations = []
        messages = []
        messages.append(self._format_messages(content_validation.issue_meta_validations))
        #messages.append(more)
        return '<div class="issue-messages">%s</div>' % ''.join(messages)

    def _format_result(self, result):
        return [self._eval(v) for k, v in result.items() if not v == self._eval(v)]

    def _format_as_table(self, data, columns):
        r = '<div class="CSSTableGenerator"><table>'
        r += '<tr>'
        for col in columns:    
            r += '<td>%s</td>' % col
        r += '</tr>'
        for item in data:
            r += '<tr>'
            for col in columns:
                content = item.get(col, '')
                if content is None:
                    content = ''
                if col == 'xml':
                    r += '<td>%s</td>' % content.replace('<', '&lt;').replace('>', '&gt;')
                else:
                    r += '<td>%s</td>' % content
            r += '</tr>'
        r += '</table></div>'
        return r

    def _eval(self, data):
        cls = 'error' if 'ERROR' in data else 'warning' if 'WARNING' in data else None
        if cls is None:
            return str(data)
        else:
            icon = ' ! ' if cls == 'warning' else ' X '
            return '<p class="p-%s"><span class="icon-%s"> %s </span><span class="text-%s"> %s</span></p>' % (cls, cls, icon, cls, data)


class HTMLReport(object):
    def __init__(self):
        f = open(CONFIG_VERSIONS_PATH + '/v3.0/xsl/scielo-style/datareport.css')
        self.css_content = f.read()
        f.close()

    def _css(self, name):
        f = open(CONFIG_VERSIONS_PATH + '/v3.0/xsl/scielo-style/' + name + '.css')
        css = f.read()
        f.close()
        return css

    def _table_(self, table_header, table_rows):
        return '<div class="CSSTableGenerator"><table>%s%s</table></div>' % (table_header, table_rows)

    def _table_rows(self, columns, data, cols):
        r = ''
        if data is None:
            data = []
        if columns:
            for row in data:
                r += '<tr>'
                for c in cols:
                    r += '<td>%s</td>' % row.get(c, '')
                for c in columns:

                    content = row.get(c, '')
                    if not content:
                        content = ''
                    if c == 'xml':
                        content = content.replace('<', '&lt;').replace('>', '&gt;')
                    r += '<td>%s</td>' % self._cell_css(content)
                r += '</tr>'
        else:
            for row in data:
                r += '<tr><td>%s</td></tr>' % row
        return r

    def _cell_css(self, data):
        if data is None:
            data = ''
        c = 'error' if 'ERROR' in data else 'warning' if 'WARNING' in data else None
        return data if c is None else '<span class="%s">%s</span>' % (c, data)

    def _table_header(self, columns, colums_default):
        header = ['<td>%s</td>' % data for data in columns]
        header = ''.join(header)
        return '<tr>%s%s</tr>' % (colums_default, header)

    def _html(self, filename, title, css_content, body):
        header = '<header><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><title>' + title + '</title><style>' + css_content + '</style></header>'
        procdate = datetime.now().isoformat()
        html = '<html>%s<body><p>%s %s</p><h1>%s</h1>%s</body></html>' % (header, procdate[0:10], procdate[11:19], title, body)

        import codecs

        f = codecs.open(filename, 'w', 'utf-8')
        f.write(html)
        f.close()

    def in_table_format(self, data, columns):
        table_header = self._table_header(columns, '<td>id</td><td>label</td>')
        table_data = self._table_rows(columns, data, ['id', 'label'])
        return self._table_(table_header, table_data)


class CheckList(object):

    def __init__(self, pkg_name, default_validator_version=None, entities_table=None):
        self.pkg_name = pkg_name
        self.entities_table = entities_table
        self.default_validator_version = default_validator_version
        if default_validator_version:
            self.set_validator_version(default_validator_version)
        #dtd_filename, xsl_prep_report, xsl_report, xsl_preview, css_filename
        
    def set_validator_version(self, validator_version):
        self.selected_validator_version = validator_version
        if validator_version == '1.0':
            self.selected_validator_version = 'j1.0'
        version_data = _versions_.get(self.selected_validator_version, {}).get(self.pkg_name)
        self.xsl_report = version_data.get('xsl_report', None)
        self.xsl_prep_report = version_data.get('xsl_prep_report', None)
        self.xsl_preview = version_data.get('xsl_preview', None)
        self.dtd_filename = version_data.get('dtd', None)
        self.css_filename = 'file:///' + version_data.get('css', None)
        self.xsl_output = version_data.get('xsl_output', None)
        self.doctype = version_data.get('doctype', None)
        self._report = []
        
    def is_well_formed(self, xml_filename):
        xml = xml_is_well_formed(xml_filename)
        if xml is None:
            print('Converting entities...')
            f = open(xml_filename, 'r')
            content = f.read()
            f.close()

            content = convert_entities(content, self.entities_table)

            xml = xml_is_well_formed(content)
            if not xml is None:
                f = open(xml_filename, 'w')
                f.write(content)
                f.close()
        return xml

    def check_validator_version(self, xml):
        if self.default_validator_version is None:
            version = xml.find('.').attrib.get('dtd-version', '1.0')
            self.set_validator_version(version)

    def get_copy(self, xml_filename):
        temp_dir = tempfile.mkdtemp()
        temp_xml_filename = temp_dir + '/' + os.path.basename(xml_filename)
        shutil.copyfile(xml_filename, temp_xml_filename)
        return temp_xml_filename

    def dtd_validation(self, xml_filename, report_filename):
        if self.dtd_filename:
            f = open(xml_filename, 'r')
            content = f.read()
            f.close()

            xml_str = XMLString(content)
            xml_str.fix_dtd_location(self.dtd_filename, self.doctype)

            if not content == xml_str.content:
                f = open(xml_filename, 'w')
                f.write(xml_str.content)
                f.close()

        return xml_validate(xml_filename, report_filename, True)

    def style_validation(self, xml_filename, style_checker_report):
        # STYLE CHECKER REPORT
        is_valid_style = False

        xml_report = style_checker_report.replace('.html', '.xml')
        if os.path.exists(xml_report):
            os.unlink(xml_report)

        if xml_transform(xml_filename, self.xsl_prep_report, xml_report):
            # Generate self.report.html
            #self.log('transform ' + xml_report + ' ' + self.xsl_report + ' ' + style_checker_report)
            if os.path.exists(style_checker_report):
                os.unlink(style_checker_report)

            if xml_transform(xml_report, self.xsl_report, style_checker_report):
                os.unlink(xml_report)

                if os.path.isfile(style_checker_report):
                    f = open(style_checker_report, 'r')
                    c = f.read()
                    f.close()

                    is_valid_style = ('Total of errors = 0' in c) and (('Total of warnings = 0' in c) or (not 'Total of warnings =' in c))

                    if not is_valid_style:
                        print('\nThere are ERRORS or WARNINGS')
                        print(style_checker_report)

        return is_valid_style

    def output(self, xml_filename, xml_output):
        if os.path.exists(xml_output):
            os.unlink(xml_output)
        return xml_transform(xml_filename, self.xsl_output, xml_output)

    def check_list(self, xml_filename, pkg_files, img_path, xsl_param_new_name=''):
        #well_formed, is_dtd_valid, report_ok, preview_ok, output_ok = (False, False, False, False, False)
        xml = self.is_well_formed(xml_filename)
        pkg_files.checking_xml_filename = xml_filename

        if xml:
            pkg_files.is_well_formed = True

            self.check_validator_version(xml)

            temp_xml_filename = self.get_copy(xml_filename)
            pkg_files.is_valid_dtd = self.dtd_validation(temp_xml_filename, pkg_files.dtd_validation_report)
            pkg_files.is_valid_style = self.style_validation(temp_xml_filename, pkg_files.style_checker_report)
            if pkg_files.xml_output:
                self.output(temp_xml_filename, pkg_files.xml_output)

            os.unlink(temp_xml_filename)
            shutil.rmtree(os.path.dirname(temp_xml_filename))

        return pkg_files


class ContentValidation(object):

    def __init__(self, xml, filename):
        self.xml = xml
        self.issue_meta = {}
        self.article_meta = {}
        self.refs = []
        self.href = []
        self.filename = filename
        self.issue_label = ''

        if self.xml is not None:

            article_node = self.xml.find('.')
            journal_meta = self.xml.find('.//journal-meta')
            self.issue_meta['publisher-name'] = journal_meta.findtext('.//publisher-name')
            self.issue_meta['nlm-ta'] = journal_meta.findtext('.//journal-id[@journal-id-type="nlm-ta"]')
            self.issue_meta['eissn'] = journal_meta.findtext('.//issn[@pub-type="epub"]')

            self.issue_meta['pissn'] = journal_meta.findtext('.//issn[@pub-type="ppub"]')
            self.issue_meta['journal-title'] = journal_meta.findtext('.//journal-title')

            article_meta = self.xml.find('.//article-meta')

            self.issue_meta['suppl'] = article_meta.findtext('./supplement')
            self.issue_meta['issue'] = article_meta.findtext('./issue')
            self.issue_meta['volume'] = article_meta.findtext('./volume')
            self.issue_label = '%s, %s (%s)' % (self.issue_meta.get('journal-title', ''), self.issue_meta.get('volume', ''), self.issue_meta.get('issue', ''))

            for tp in ['ppub', 'epub', 'epub-ppub', 'collection']:
                node = article_meta.find('.//pub-date[@pub-type="' + tp + '"]')
                if not node is None:
                    d = [node.findtext(elem) for elem in ['day', 'month', 'season', 'year']]
                    d = [item if item is not None else '' for item in d]
                    if any(d):
                        self.article_meta['date-' + tp] = '%s / %s%s / %s' % tuple(d)
            for tp in ['pub', 'preprint']:
                node = article_meta.find('.//pub-date[@date-type="' + tp + '"]')
                if not node is None:
                    d = [node.findtext(elem) for elem in ['day', 'month', 'season', 'year']]
                    d = [item if item is not None else '' for item in d]
                    if any(d):
                        self.article_meta['date-' + tp] = '%s / %s%s / %s' % tuple(d)
            # ------
            self.article_meta['filename'] = filename
            self.article_meta['article-type'] = article_node.attrib.get('article-type', '')
            self.article_meta['lang'] = article_node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)

            self.article_meta['doi'] = article_meta.findtext('.//article-id[@pub-id-type="doi"]')
            self.article_meta['other id'] = article_meta.findtext('.//article-id[@pub-id-type="other"]')

            self.article_meta['subject'] = '|'.join([node.text for node in article_meta.findall('.//subject')])

            self.article_meta['fpage_seq'] = ''
            if article_meta.findtext('.//fpage') is None:
                self.article_meta['fpage'] = ''
            else:
                self.article_meta['fpage'] = article_meta.findtext('.//fpage')
                self.article_meta['fpage_seq'] = article_meta.find('.//fpage').attrib.get('seq', '')

            if article_meta.findtext('.//lpage') is None:
                self.article_meta['lpage'] = ''
            else:
                self.article_meta['lpage'] = article_meta.findtext('.//lpage')
                self.article_meta['lpage_seq'] = article_meta.find('.//lpage').attrib.get('seq', '')

            article_title = article_meta.find('.//article-title')
            self.article_meta['article-title'] = self._node_xml_content(article_title)

            self.article_meta['award-id'] = ','.join([award.text for award in article_meta.findall('.//award-id')])
            self.article_meta['ack'] = self._node_xml_content(self.xml.find('.//ack'))

            self.article_meta['license'] = self._node_xml(self.xml.find('.//license'))
            self.article_meta['text body sections'] = []
            for node in self.xml.findall('.//body/sec'):
                title = node.findtext('.//title')
                tp = node.attrib.get('sec-type', '')
                self.article_meta['text body sections'].append((tp if tp is not None else '', title if title is not None else ''))

            for tp in ['received', 'accepted']:
                node = self.xml.find('.//date[@date-type="' + tp + '"]')
                if node is not None:
                    d = ''
                    y = node.findtext('year')
                    if y is None:
                        d += '0000'
                    else:
                        d += y
                    for item in [node.findtext('month'), node.findtext('day')]:
                        if item is None:
                            d += '00'
                        else:
                            item = '00' + item
                            d += item[-2:]
                    self.article_meta[tp + ' date (history)'] = d
            self.article_meta['aff'] = []
            for aff in article_meta.findall('.//aff'):
                a = {'id': aff.attrib.get('id')}
                for item in ['orgname', 'orgdiv1', 'orgdiv2', 'orgdiv3']:
                    a[item] = aff.findtext('institution[@content-type="' + item + '"]')
                
                for item in ['original', 'aff-pmc']:
                    a[item] = self._node_xml(aff.find('institution[@content-type="' + item + '"]'))
                a['email'] = aff.findtext('email')
                a['country'] = aff.findtext('country')
                a['city'] = aff.findtext('addr-line/named-content[@content-type="city"]')
                a['state'] = aff.findtext('addr-line/named-content[@content-type="state"]')

                a['xml'] = self._node_xml(aff)
                self.article_meta['aff'].append(a)

            self.article_meta['abstract'] = self._node_xml_content(article_meta.find('.//abstract'))

            #self.article_meta['lang'] = article_title.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', '??')
            self.article_meta['trans-title'] = {}
            for trans_title in article_meta.findall('.//trans-title-group'):
                lang = trans_title.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', '??')
                self.article_meta['trans-title'][lang] = trans_title.findtext('trans-title')
            self.article_meta['trans-abstract'] = {}

            for trans_abstract in article_meta.findall('.//trans-abstract'):
                lang = trans_abstract.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', '??')
                self.article_meta['trans-abstract'][lang] = self._node_xml_content(trans_abstract)

            self.article_meta['kwd-group'] = {}
            for kwd_group in article_meta.findall('.//kwd-group'):
                lang = kwd_group.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', kwd_group.attrib.get('lang', '??'))
                self.article_meta['kwd-group'][lang] = [self._node_xml_content(kwd) for kwd in kwd_group.findall('kwd')]

            self.article_meta['author'] = []
            for author in article_meta.findall('.//contrib//name'):
                a = {}
                a['given-names'] = author.findtext('.//given-names')
                a['surname'] = author.findtext('.//surname')
                a['suffix'] = author.findtext('.//suffix')
                a['prefix'] = author.findtext('.//prefix')
                self.article_meta['author'].append(a)

            self.article_meta['collab'] = [node.text for node in article_meta.findall('.//contrib//collab')]

            self.article_meta['order'] = self._order(self.article_meta['fpage'], self.article_meta['fpage_seq'], self.article_meta['other id'])

            for node in self.xml.findall('.//*[@{http://www.w3.org/1999/xlink}href]'):
                href = node.attrib.get('{http://www.w3.org/1999/xlink}href', None)
                if href is None:
                    print('href not found???')
                    print(self._node_xml(node))
                else:
                    self.href.append(href)

            for ref in self.xml.findall('.//ref'):
                r = {}
                r['id'] = ref.attrib.get('id', None)

                e = ref.find('element-citation')
                r['type'] = e.attrib.get('publication-type')
                r['mixed'] = self._node_xml_content(ref.find('mixed-citation'))

                r['author'] = []
                for author in ref.findall('.//name'):
                    a = {}
                    a['given-names'] = author.findtext('.//given-names')
                    a['surname'] = author.findtext('.//surname')
                    a['suffix'] = author.findtext('.//suffix')
                    a['prefix'] = author.findtext('.//prefix')
                    r['author'].append(a)

                r['collab'] = [node.text for node in ref.findall('.//collab')]
                r['lang'] = None
                node = ref.find('.//article-title')
                if node is not None:
                    r['lang'] = node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)
                else:
                    node = ref.find('.//chapter-title')
                    if node is not None:
                        r['lang'] = node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)

                    if r['lang'] is None:
                        node = ref.find('.//source')
                        if node is not None:
                            r['lang'] = node.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None)

                r['year'] = ref.findtext('.//year')
                r['source'] = ref.findtext('.//source')
                r['publisher-name'] = ref.findtext('.//publisher-name')
                r['publisher-loc'] = ref.findtext('.//publisher-loc')
                r['article-title'] = self._node_xml_content(ref.find('.//article-title'))
                r['chapter-title'] = self._node_xml_content(ref.find('.//chapter-title'))
                nodes = ref.findall('element-citation//ext-link')
                if nodes:
                    r['ext-link'] = [uri.text for uri in nodes]
                nodes = ref.findall('element-citation//uri')
                if nodes:
                    r['ext-link'] += [uri.text for uri in nodes]

                r['cited'] = ref.findtext('.//date-in-citation[@content-type="access-date"]')
                r['xml'] = self._node_xml(ref)
                self.refs.append(r)

    def issue_date(self):
        r = [self.article_meta.get('date-' + item) for item in ['ppub', 'epub-ppub', 'collection', 'pub']]
        r = [item for item in r if item is not None]
        return r[0] if r is not None else ''

    def article_date(self):
        r = [self.article_meta.get('date-' + item) for item in ['epub', 'preprint']]
        r = [item for item in r if item is not None]
        return r[0] if r is not None else ''

    def _node_xml(self, node):
        if not node is None:
            return etree.tostring(node)

    def _node_xml_content(self, node):
        if not node is None:
            xml = etree.tostring(node)
            if xml[0:1] == '<':
                xml = xml[xml.find('>') + 1:]
                xml = xml[0:xml.rfind('</')]
            return xml
        return ''

    def _order(self, fpage, fpage_seq, other_id):
        if other_id == '':
            other_id = None
        if fpage == '':
            fpage = None
        if other_id is None:
            if fpage is None:
                order = 0
            else:
                if fpage.isdigit():
                    order = int(fpage)
                else:
                    order = 0
        else:
            order = int(other_id)

        return str(order)

    def _validate_data(self, data, expected):
        if isinstance(data, dict):
            result = []
            for key, item in expected.items():
                if not item == data.get(key, ''):
                    result.append('ERROR: Invalid value for %s. Expected: %s.' % (data.get(key, ''), item))
            return result
        elif isinstance(data, (str, unicode)):
            if not data == expected:
                result = 'ERROR: Invalid value for %s. Expected: %s.' % (data, expected)
            return result

    def _validate_presence_data(self, msg_type, status, data, label_list, scope=None):
        _scope = scope + ': ' if not scope is None else ''
        result = []

        if isinstance(data, (str, unicode)):
            #if data.strip() and not '<' in data:
            if data.strip():
                if not(data.strip()[0:1] == '<' and data.strip()[-1:] == '>'):
                    
                    if startswith_invalid_char(data):
                        result.append('ERROR: ' + _scope + ' ' + label_list + ' starts with an invalid character (' + data[0:1] + ')')
                    if endswith_invalid_char(data):
                        print('.' + data + '.')
                        print('.' + data.strip() + '.')

                        result.append('ERROR: ' + _scope + ' ' + label_list + ' ends with an invalid character (' + data[-1:] + ')')
            else:
                result.append(msg_type + ': ' + _scope + ' ' + status + ' ' + label_list)
        elif isinstance(data, dict):
            for req in label_list:
                scope = '' if data.get('id', None) is None else data['id'] + ': '
                result += self._validate_presence_data(msg_type, status, data.get(req, None), req, scope)
        elif isinstance(data, list):
            for item in data:
                result += self._validate_presence_data(msg_type, status, item, label_list, scope)
            result = [error for error in result if error]
        else:
            if isinstance(label_list, str):
                result.append(msg_type + ': ' + _scope + ' ' + status + ' ' + label_list)
            else:
                result.append(msg_type + ': ' + _scope + ' ' + status + ' ' + ' | '.join(label_list))
        return result

    def _validate_conditional_required_data(self, data, required, scope=None):
        return self._validate_presence_data('WARNING', 'Required (if exists)', data, required, scope)

    def _validate_required_data(self, data, required, scope=None):
        return self._validate_presence_data('ERROR', 'Required', data, required, scope)

    def _validate_presence_of_at_least_one(self, data, labels):
        if not any(data):
            return 'ERROR: Required one of ' + ' | '.join(labels)
        
    def _validate_previous_and_next(self, previous, next, labels, max_distance=None):
        if previous is None:
            previous = 0
        if next is None:
            next = 0
        if isinstance(previous, str):
            if previous.isdigit():
                previous = int(previous)
        if isinstance(next, str):
            if next.isdigit():
                next = int(next)

        if isinstance(previous, int) and isinstance(next, int):
            dist = next - previous
            if previous > next:
                return 'ERROR: %s %s must come before %s.' % (labels, previous, next)
            elif max_distance:
                if dist > max_distance:
                    return 'WARNING: Check %s: %s and %s.' % (labels, previous, next)

    def surname_validation(self, authors):
        validation = []
        for a in authors:
            if ' ' in a.get('surname', ''):
                validation.append(a.get('surname', ''))
        if len(validation) > 0:
            validation = 'WARNING: Invalid surnames: ' + ', '.join(validation)
        else:
            validation = ''
        return validation

    def validations(self, expected_journal_meta, files):
        self.article_meta_validations = {}
        self.files_validations = ''
        self.issue_meta_validations = None
        self.refs_validations = []

        if self.xml is not None:
            self.issue_meta_validations = self._validate_required_data(self.issue_meta, ['publisher-name', 'journal-title', 'issue'], 'journal-meta and issue-meta')
            self.issue_meta_validations += self._validate_conditional_required_data(self.issue_meta, ['issue'], 'journal-meta and issue-meta')
            if expected_journal_meta:
                self.issue_meta_validations += self._validate_data(self.issue_meta, expected_journal_meta)

            if not self.issue_meta['suppl'] is None:
                self.issue_meta_validations += ['FATAL ERROR: do not use <supplement>, use <issue> to label supplement. E.g.: <issue>1 Suppl</issue>, <issue>1 Suppl 2</issue>, <issue>Suppl</issue>', '<issue>Suppl 1</issue>']
            if not self._has_only_letter_number_space(self.issue_meta['issue']):
                self.issue_meta_validations += ['FATAL ERROR: invalid characteres in issue tag: ' + self.issue_meta['issue']]
            #print(self.issue_meta_validations)
            # cleanit
            self.article_meta_validations['dates'] = self._validate_presence_of_at_least_one([self.article_meta.get('date-epub'), self.article_meta.get('date-ppub'), self.article_meta.get('date-epub-ppub'), self.article_meta.get('date-collection'), self.article_meta.get('date-pub'), self.article_meta.get('date-preprint')], ['epub date', 'ppub date', 'epub-ppub date', 'collection date', 'pub date', 'preprint date'])
            self.article_meta_validations['issns'] = self._validate_presence_of_at_least_one([self.issue_meta['pissn'], self.issue_meta['eissn']], ['print issn', 'e-issn'])

            order = self.article_meta.get('order', '0')
            if order.isdigit():
                if 0 < int(order) < 100000:
                    pass
                else:
                    self.article_meta_validations['order'] = 'FATAL ERROR: Invalid value for order. It must be a number 1-9999'
            else:
                self.article_meta_validations['order'] = 'FATAL ERROR: Invalid value for order. It must be a number 1-9999'

            required_items = ['article-title', 'subject', 'doi', 'fpage', 'license']
            for label in required_items:
                self.article_meta_validations[label] = self._validate_required_data(self.article_meta.get(label, None), label)
            required_items = ['abstract', 'received date (history)', 'accepted date (history)', 'text body sections']
            for label in required_items:
                self.article_meta_validations[label] = self._validate_conditional_required_data(self.article_meta.get(label, None), label)

            for trans_type in ['trans-abstract', 'trans-title', 'kwd-group']:
                translations = self.article_meta.get(trans_type, None)
                if translations:
                    for lang, t in translations.items():
                        if lang == '??':
                            self.article_meta_validations[trans_type] = self._validate_conditional_required_data(None, trans_type + ' lang')
                else:
                    self.article_meta_validations[trans_type] = self._validate_conditional_required_data(None, trans_type)

            self.article_meta_validations['pages'] = self._validate_previous_and_next(self.article_meta['fpage'], self.article_meta['lpage'], 'first page and last page', 20)

            self.article_meta_validations['history dates'] = self._validate_previous_and_next(self.article_meta.get('received', None), self.article_meta.get('accepted', None), 'received/accepted dates')

            #self.article_meta_validations['affs'] = self._validate_required_data(self.article_meta['aff'], ['orgname', 'city', 'state', 'country', 'full affiliation without tags'])
            self.article_meta_validations['affs'] = self.validate_content(self.article_meta['aff'], ['orgname', 'original'], ['city', 'state', 'country'], [])

            if self.article_meta['author']:
                self.article_meta_validations['author'] = self._validate_required_data(self.article_meta['author'], ['given-names', 'surname'])
                invalid_surname = self.surname_validation(self.article_meta['author'])
                if len(invalid_surname) > 0:
                    self.article_meta_validations['surnames'] = invalid_surname

            if not self.article_meta.get('award-id'):
                ack = self.article_meta.get('ack', None)
                if ack:
                    # PARA IGNORAR <p id="parag28">
                    if '<' in ack:
                        ack = ack.replace('<', '_BREAK_<')
                        ack = ack.split('_BREAK_')
                        new = ''
                        for item in ack:
                            if item.startswith('<'):
                                new += item[item.find('>'):]
                            else:
                                new += item
                        ack = new

                    if '&#' in ack:
                        ack = ack.replace('&#', '_BREAK_&#')
                        ack = ack.split('_BREAK_')
                        new = ''
                        for item in ack:
                            if item.startswith('&#'):
                                new += item[item.find(';'):]
                            else:
                                new += item
                        ack = new

                    if any([True for n in range(0, 10) if str(n) in ack]):
                        self.article_meta_validations['ack'] = 'WARNING: Check ack has contact number. %s' % self.article_meta.get('ack', None)
            count = len(self.refs)
            #print(count)
            self.article_meta_validations['ref-count'] = 'WARNING: Total of references = 0' if count == 0 else ''
            #print(self.article_meta_validations)
            for ref in self.refs:
                r = {}
                r = {'id': ref['id'], 'xml': ref['xml']}

                r['year-source'] = self._validate_required_data(ref, ['year', 'source', 'lang'])

                if not ref['type'] in ['journal', 'book', 'thesis', 'conf-proc', 'patent', 'report', 'software', 'web']:
                    r['type'] = 'ERROR: Invalid value for element-citation/@publication-type: %s. Expected: %s.' % (ref['type'], ' | '.join(['journal', 'book', 'thesis', 'conf-proc', 'patent', 'report', 'software', 'web']))

                if not ref['mixed']:
                    r['mixed'] = 'ERROR: Required mixed-citation'

                if ref['author']:
                    r['author'] = self._validate_required_data(ref['author'], ['given-names', 'surname'])
                    invalid_surname = self.surname_validation(ref['author'])
                    if len(invalid_surname) > 0:
                        r['surnames'] = invalid_surname

                r['authorship'] = self._validate_presence_of_at_least_one([ref.get('author'), ref.get('collab')], ['author', 'collab'])
                if ref['type'] == 'book':
                    r['publisher'] = self._validate_required_data(ref, ['publisher-name', 'publisher-loc'])
                if ref['type'] == 'web':
                    r['link'] = self._validate_required_data(ref, ['ext-link', 'cited'])
                self.refs_validations.append(r)

            r_files = ['<li>' + f + '</li>' for f in self.href if not f in files]

            self.files_validations = 'ERROR: Required files <ul>%s</ul>' % ''.join(r_files) if len(r_files) > 0 else ''

    def validate_content(self, data, required_items, conditional_required_items, invalid_characteres, scope=None):
        results = []
        if required_items:
            results.append(self._validate_required_data(data, required_items, scope))
        if conditional_required_items:
            results.append(self._validate_conditional_required_data(data, conditional_required_items, scope))
        if invalid_characteres:
            results.append(self._has_invalid_characteres(data, invalid_characteres))
        return results

    def _has_invalid_characteres(self, content, invalid_characteres):
        if any([True for c in invalid_characteres if c in content]):
            return 'ERROR: Invalid characteres in %s (%s)' % (content, ' | '.join(invalid_characteres))

    def _has_only_letter_number_space(self, content):
        r = False
        if len(content) > 0:
            valid = 'abcdefghijklmnopqrstuvwxyz'
            valid += valid.upper() + '1234567890 '
            for item in valid:
                content = content.replace(item, '')
            r = (len(content) == 0)
        return r


class ValidationResult(object):

    def __init__(self, pkg_path, report_path, xml_output_path=None, suffix='', preview_path=None):
        self.pkg_path = pkg_path
        self.report_path = report_path
        self.xml_output_path = xml_output_path
        self.preview_path = preview_path

        for d in [pkg_path, report_path, xml_output_path, preview_path]:
            if not d is None and not d == '':
                if not os.path.exists(d):
                    os.makedirs(d)

        self.suffix = suffix
        self.is_well_formed = False
        self.is_valid_style = False
        self.is_valid_dtd = False

    def name(self, curr_name, new_name):
        self.dtd_validation_report = self.report_path + '/' + curr_name + self.suffix + '.dtd.txt'
        self.log_filename = self.report_path + '/' + curr_name + self.suffix + '.log'
        self.style_checker_report = self.report_path + '/' + curr_name + self.suffix + '.rep.html'

        if self.preview_path == self.pkg_path:
            self.html_preview = self.pkg_path + '/' + new_name + '.html'
        elif not self.preview_path is None:
            self.html_preview = self.preview_path + '/' + curr_name + self.suffix + '.xml.html'
        else:
            self.html_preview = None

        if self.xml_output_path is None:
            self.xml_output = self.pkg_path + '/' + new_name + '.xml'
        else:
            self.xml_output = self.xml_output_path + '/' + new_name + '.xml'
        self.xml_name = curr_name
        self.new_name = new_name
        self.is_well_formed = False
        self.is_valid_style = False
        self.is_valid_dtd = False

    def manage_result(self, ctrl_filename):
        if ctrl_filename is None:
            if self.is_valid_dtd is True:
                os.unlink(self.dtd_validation_report)
            if self.is_valid_style is True:
                os.unlink(self.style_checker_report)
            if self.is_well_formed:
                if os.path.isfile(self.log_filename):
                    os.unlink(self.log_filename)
            else:
                f = open(self.dtd_validation_report, 'a+')
                f.write('XML is not well formed')
                f.close()
        else:
            err_filename = ctrl_filename.replace('.ctrl', '.err')
            f = open(ctrl_filename, 'w')
            f.write('Finished')
            f.close()

            f = open(err_filename, 'a+')
            if self.is_well_formed:
                if os.path.isfile(self.log_filename):
                    os.unlink(self.log_filename)
            else:
                f.write(self.checking_xml_filename + ': XML is not well formed')

            if not self.is_valid_dtd:
                if os.path.isfile(self.dtd_validation_report):
                    f.write('\nDTD errors report\n' + ('='*len('DTD errors report')) + '\n' + open(self.dtd_validation_report).read())
                else:
                    f.write('Unable to generate ' + self.dtd_validation_report)

            elif not self.is_valid_style:
                if not os.path.isfile(self.style_checker_report):
                    f.write('Unable to generate ' + self.style_checker_report)

            f.close()


class Normalizer(object):

    def __init__(self, entities_table, version_converter):
        self.entities_table = entities_table
        self.version_converter = version_converter

    def normalize_content(self, xml_filename, src_path, dest_path, acron):
        log = []

        is_sgmxml = xml_filename.endswith('.sgm.xml')
        xml_name = os.path.basename(xml_filename)
        xml_name = xml_name.replace('.sgm.xml', '').replace('.xml', '')
        new_name = xml_name

        log.append('xml name:' + xml_name)

        f = open(xml_filename)
        content = f.read()
        content = content.replace('mml:', '')
        f.close()

        # fix problems of XML format
        if is_sgmxml:
            xml_fix = XMLString(content)
            xml_fix.fix()
            if not xml_fix.content == content:
                content = xml_fix.content

            content = xml_content_transform(content, self.version_converter)

            xml_fix = XMLString(content)
            if not xml_fix.content == content:
                content = xml_fix.content
        content = convert_entities(content, self.entities_table)

        if xml_is_well_formed(content) is not None:
            #new name and href list
            new_name, href_list = XMLMetadata(content).new_name_and_href_list(acron, xml_name)

            #href and new href list
            curr_and_new_href_list = self.generate_curr_and_new_href_list(xml_name, new_name, href_list)

            # related files and href files list
            not_found, related_files_list, href_files_list = self.matched_files(xml_name, new_name, curr_and_new_href_list, src_path)

            log.append('new name:' + new_name)
            log.append('Total of related files: ' + str(len(related_files_list)))
            log.append('\n'.join(['   ' + c + ' => ' + n for c, n in sorted(related_files_list)]))

            log.append('Total of @href: ' + str(len(href_list)))
            log.append('\n'.join(['   ' + c for c, n in sorted(href_list)]))

            log.append('Total of @href files: ' + str(len(curr_and_new_href_list)))
            log.append('\n'.join(['   ' + c + ' => ' + n for c, n in curr_and_new_href_list]))

            log.append('Total of @href files found: ' + str(len(href_files_list)))
            log.append('\n'.join(['   ' + c + ' => ' + n for c, n in sorted(href_files_list)]))

            if len(not_found) > 0:
                log.append('\nTotal of @href files not found:\n   ' + '\n  '.join(not_found))

            if len(curr_and_new_href_list) > 0:
                content = self.normalize_href(content, curr_and_new_href_list)

            jpg_created = self.rename_files(related_files_list, href_files_list, src_path, dest_path)
            log.append('\n'.join(jpg_created))

            f = open(dest_path + '/' + new_name + '.xml', 'w')
            f.write(content)
            f.close()
        else:
            log.append('XML is not well formed')

            f = open(dest_path + '/incorrect_' + new_name + '.xml', 'w')
            f.write(content)
            f.close()
        return (new_name, log)

    def generate_curr_and_new_href_list(self, xml_name, new_name, href_list):
        r = []
        for href, suffix_and_id in href_list:
            if xml_name in href:
                file_suffix = href.replace(xml_name, '')
                if file_suffix[0:1] == '-':
                    file_suffix = file_suffix[1:]
                if file_suffix[0:1] != suffix_and_id[0:1]:
                    new = new_name + '-' + suffix_and_id[0:1] + file_suffix
                else:
                    new = new_name + '-' + file_suffix
            else:
                new = new_name + '-' + suffix_and_id[0:1] + href

            if new[new.rfind('.'):] in ['.jpg', '.tiff', '.eps', '.tiff']:
                new = new[0:new.rfind('.')]
            r.append((href, new))
        return list(set(r))

    def matched_files(self, xml_name, new_name, curr_and_new_href_list, src_path):
        """
        return [(src file, new name)]
        """
        href_files_list = []
        not_found = []
        related_files_list = [(f, new_name + f[f.rfind('.'):]) for f in os.listdir(src_path) if f.startswith(xml_name + '.')]
        for curr, new in curr_and_new_href_list:
            if os.path.isfile(src_path + '/' + curr):
                href_files_list.append((curr, new))
            else:
                # curr and new has no extension
                found = [(f, new + f[f.rfind('.'):]) for f in os.listdir(src_path) if f.startswith(curr + '.')]
                if len(found) == 0:
                    curr_noext = curr[0:curr.rfind('.')]
                    found = [(f, new + f[f.rfind('.'):]) for f in os.listdir(src_path) if f.startswith(curr_noext + '.')]
                if len(found) == 0:
                    not_found.append(curr)
                else:
                    href_files_list += found
        href_files_list = sorted(list(set(href_files_list)))
        return (not_found, related_files_list, href_files_list)

    def normalize_href(self, content, curr_and_new_href_list):
        #print(curr_and_new_href_list)
        for current, new in curr_and_new_href_list:
            print(current + ' => ' + new)
            content = content.replace('href="' + current, 'href="' + new)
            content = content.replace(' filename="' + current, ' filename="' + new)
        return content

    def rename_files(self, related_files_list, href_files_list, src_path, dest_path):
        jpg_created = []
        for curr, new in related_files_list:
            shutil.copyfile(src_path + '/' + curr, dest_path + '/' + new)
            
        for curr, new in href_files_list:
            shutil.copyfile(src_path + '/' + curr, dest_path + '/' + new)
            
            if IMG_CONVERTER:
                ext = curr[curr.rfind('.'):]
                if ext in ['.tiff', '.tif', '.eps']:
                    name = curr[0:curr.rfind('.')]
                    if not os.path.isfile(src_path + '/' + name + '.jpg'):
                        # converter para .jpg
                        if img_to_jpeg(dest_path + '/' + new, dest_path):
                            jpg_created.append('created ' + new.replace(ext, '.jpg'))
        return jpg_created


class XPM5(object):
    def __init__(self, sci_validator, pmc_validator, acron, default_version, entities_table):
        version_converter = _versions_.get(default_version, {}).get('sgm2xml')
        self.normalizer = Normalizer(entities_table, version_converter)
        
        self.acron = acron
        self.sci_validator = sci_validator
        self.pmc_validator = pmc_validator

    def add_href_extensions(self, xml_filename):
        name = os.path.basename(xml_filename).replace('.xml', '')
        path = os.path.dirname(xml_filename)
        fp = open(xml_filename, 'r')
        xml = fp.read()
        fp.close()
        for f in os.listdir(path):
            if f.startswith(name + '.') or f.startswith(name + '-'):
                f_without_ext = f[0:f.rfind('.')]
                xml = xml.replace('href="' + f_without_ext + '"', 'href="' + f + '"')
        fp = open(xml_filename, 'w')
        fp.write(xml)
        fp.close()

    def validate_packages(self, xml_name, new_name, scielo_validation_result, pmc_validation_result, err_filename, ctrl_filename):
        xsl_new_name = new_name if new_name != xml_name else ''
        img_path = scielo_validation_result.pkg_path

        if os.path.isfile(scielo_validation_result.pkg_path + '/' + new_name + '.xml'):
            if xml_is_well_formed(scielo_validation_result.pkg_path + '/' + new_name + '.xml'):
                scielo_validation_result = self.sci_validator.check_list(scielo_validation_result.pkg_path + '/' + new_name + '.xml', scielo_validation_result, img_path)
                scielo_validation_result.manage_result(ctrl_filename)

                if os.path.exists(pmc_validation_result.pkg_path + '/' + new_name + '.xml'):
                    self.add_href_extensions(pmc_validation_result.pkg_path + '/' + new_name + '.xml')
                    pmc_validation_result = self.pmc_validator.check_list(pmc_validation_result.pkg_path + '/' + new_name + '.xml', pmc_validation_result, img_path, xsl_new_name)

                    if ctrl_filename is None:
                        pmc_validation_result.manage_result(None)

                    if os.path.exists(pmc_validation_result.xml_output):
                        #self.add_href_extensions(pmc_validation_result.xml_output)
                        print('  Finished')
                    else:
                        print('\nUnable to create ' + pmc_validation_result.xml_output)
                        log_message(err_filename, 'Unable to create ' + pmc_validation_result.xml_output)
                else:
                    print('Unable to create ' + pmc_validation_result.pkg_path + '/' + new_name + '.xml')
                    log_message(err_filename, 'Unable to create ' + pmc_validation_result.pkg_path + '/' + new_name + '.xml')
            else:
                print('XML is not well formed: ' + scielo_validation_result.pkg_path + '/' + new_name + '.xml')
                log_message(err_filename, 'XML is not well formed: ' + scielo_validation_result.pkg_path + '/' + new_name + '.xml')
        else:
            print('Problem to load XML file. See ' + scielo_validation_result.pkg_path + '/incorrect_' + new_name + '.xml')
            log_message(err_filename, 'Problem to load XML file. See ' + scielo_validation_result.pkg_path + '/incorrect_' + new_name + '.xml')

    def make_packages(self, files, ctrl_filename, work_path, scielo_val_res, pmc_val_res):
        old_names = {}

        for path in [scielo_val_res.pkg_path, pmc_val_res.pkg_path]:
            if os.path.isdir(path):
                for f in os.listdir(path):
                    if os.path.isfile(path + '/' + f):
                        os.unlink(path + '/' + f)
            else:
                os.makedirs(path)

        for xml_filename in files:
            xml_path = os.path.dirname(xml_filename)
            xml_filename = os.path.basename(xml_filename)
            print('\n== %s ==\n' % xml_filename)

            xml_name = xml_filename.replace('.sgm.xml', '').replace('.xml', '')

            wrk_path = work_path + '/' + xml_name

            for path in [wrk_path]:
                if os.path.isdir(path):
                    for f in os.listdir(path):
                        if os.path.isfile(path + '/' + f):
                            os.unlink(path + '/' + f)
                else:
                    os.makedirs(path)

            log_filename = scielo_val_res.report_path + '/' + xml_name + '.log'
            err_filename = scielo_val_res.report_path + '/' + xml_name + '.err.txt'

            for f in [log_filename, err_filename]:
                if os.path.isfile(f):
                    os.unlink(f)

            log_message(err_filename, 'Report of files / DTD errors\n' + '-'*len('Report of files / DTD errors'))

            new_name, log = self.normalizer.normalize_content(xml_path + '/' + xml_filename, xml_path, wrk_path, self.acron)

            self.copy_files_to_packages_folder(wrk_path, scielo_val_res.pkg_path, pmc_val_res.pkg_path, new_name)

            old_names[new_name + '.xml'] = xml_name

            log_message(err_filename, '\n'.join(log))

            scielo_val_res.name(xml_name, new_name)
            pmc_val_res.name(xml_name, new_name)

            self.validate_packages(xml_name, new_name, scielo_val_res, pmc_val_res, err_filename, ctrl_filename)

        report = PkgReport(scielo_val_res.pkg_path, scielo_val_res.report_path)
        if ctrl_filename is None:
            # o prefixo dos nomes do arquivos dos relatorios devem ser igual ao nome do xml do pacote
            report.load_data()
            report.generate_articles_report(True, old_names)
            report.generate_lists()
        else:
            if not os.path.isfile(ctrl_filename):
                f = open(ctrl_filename, 'w')
                f.write('Finished')
                f.close()
            # o prefixo dos nomes do arquivos dos relatorios devem ser igual ao nome do xml original (old_names)
            if new_name is not None:
                report.load_data(new_name + '.xml')
                report.generate_articles_report(False, old_names)

    def copy_files_to_packages_folder(self, wrk_path, scielo_pkg_path, pmc_pkg_path, new_name):
        for f in os.listdir(scielo_pkg_path):
            if f.startswith(new_name + '.') or f.startswith(new_name + '-'):
                os.unlink(scielo_pkg_path + '/' + f)
        for f in os.listdir(pmc_pkg_path):
            if f.startswith(new_name + '.') or f.startswith(new_name + '-'):
                os.unlink(pmc_pkg_path + '/' + f)

        for f in os.listdir(wrk_path):
            shutil.copyfile(wrk_path + '/' + f, scielo_pkg_path + '/' + f)
            if not f.endswith('.jpg'):
                shutil.copyfile(wrk_path + '/' + f, pmc_pkg_path + '/' + f)


def call_make_packages(args, version):
    validated_packages(args, version)


def validated_packages(args, version):
    src, acron, v, error_message = cxpmker_read_inputs(args)
    scielo_pkg_path = None
    if v is not None:
        version = v
    if error_message == '':
        ctrl_filename, r_xml_source, scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path = cxpmker_files_and_paths(src)

        cxpmker_make_packages(report_path, scielo_pkg_path, pmc_pkg_path, acron, version, r_xml_source, wrk_path, ctrl_filename)
    else:
        print(error_message)
    return [scielo_pkg_path, acron]


def cxpmker_read_inputs(args):
    args = [arg.replace('\\', '/') for arg in args]

    script_name = args[0]
    src = ''
    acron = None
    xml_src = None
    version = None
    if len(args) == 2:
        ign, src = args
    elif len(args) == 3:
        ign, src, acron = args

    if os.path.isfile(src):
        if src.endswith('.sgm.xml'):
            xml_src = src
            temp = xml_src.split('/')
            acron = temp[len(temp)-4]
            version = 'j1.0'
            print(acron)
        elif src.endswith('.xml'):
            xml_src = src
    elif os.path.isdir(src):
        if len([f for f in os.listdir(src) if f.endswith('.xml')]) > 0:
            xml_src = src

    messages = []
    if xml_src is None or acron is None:
        messages.append('\n===== ATTENTION =====\n')
        messages.append('ERROR: Incorrect parameters')
        messages.append('\nUsage:')
        messages.append('python xml_package_maker <xml_src> <acron>')
        messages.append('where:')
        messages.append('  <xml_src> = XML filename or path which contains XML files')
        messages.append('  <acron> = journal acronym')
        print(args)
    return (xml_src, acron, version, '\n'.join(messages))


def cxpmker_files_and_paths(xml_source):
    if xml_source.endswith('.sgm.xml'):
        f = xml_source
        ctrl_filename = f.replace('.sgm.xml', '.ctrl.txt')
        r_xml_source = [cxpmker_markup_src_path(f) + '/' + os.path.basename(f)]
        scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path = cxpmker_markup_paths(xml_source, f)
        #version = 'j1.0'
    else:
        if os.path.isfile(xml_source):
            r_xml_source = [xml_source]
        else:
            r_xml_source = [xml_source + '/' + f for f in os.listdir(xml_source) if f.endswith('.xml')]

        now = datetime.now().isoformat().replace(':', '').replace('T', '').replace('-', '')
        now = now[0:now.find('.')]

        ctrl_filename = None
        scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path = cxpmker_xpm_paths(xml_source, now)

    return (ctrl_filename, r_xml_source, scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path)


def cxpmker_markup_src_path(sgmxml_filename):
    # sgmxml_path = serial/acron/issue/pmc/pmc_work/article
    xml_name = os.path.basename(sgmxml_filename)
    sgmxml_path = os.path.dirname(sgmxml_filename)

    # pmc_path = serial/acron/issue/pmc
    pmc_path = os.path.dirname(os.path.dirname(sgmxml_path))

    # other files path = serial/acron/issue/pmc/src or serial/acron/issue/pmc/pmc_src
    pmc_src = pmc_path + '/src'
    if not os.path.isdir(pmc_src):
        pmc_src = pmc_path + '/pmc_src'
    if not os.path.isdir(pmc_src):
        os.makedirs(pmc_src)

    shutil.copyfile(sgmxml_filename, pmc_src + '/' + xml_name)
    return pmc_src


def cxpmker_markup_paths(pmc_src, sgmxml_filename):
    sgmxml_path = os.path.dirname(sgmxml_filename)
    pmc_path = os.path.dirname(pmc_src)

    scielo_pkg_path = pmc_path + '/xml_package'
    pmc_pkg_path = pmc_path + '/pmc_package'
    report_path = sgmxml_path
    preview_path = None
    wrk_path = sgmxml_path
    return (scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path)


def cxpmker_xpm_paths(src, now):
    if os.path.isfile(src):
        path = os.path.dirname(src) + '_' + now
    else:
        path = src + '_' + now

    scielo_pkg_path = path + '/scielo_package'
    pmc_pkg_path = path + '/pmc_package'
    report_path = path + '/errors'
    wrk_path = path + '/wrk'
    preview_path = None
    return (scielo_pkg_path, pmc_pkg_path, report_path, preview_path, wrk_path)


def cxpmker_make_packages(report_path, scielo_pkg_path, pmc_pkg_path, acron, version, xml_source, wrk_path, ctrl_filename):

    if not os.path.exists(report_path):
        os.makedirs(report_path)

    sci_val_res = ValidationResult(scielo_pkg_path, report_path, pmc_pkg_path, '', None)
    pmc_val_res = ValidationResult(pmc_pkg_path, report_path, None, '.pmc', None)

    sci_validator = CheckList('scielo', version, entities_table)
    pmc_validator = CheckList('pmc', version)

    xml_pkg_mker = XPM5(sci_validator, pmc_validator, acron, version, entities_table)
    xml_pkg_mker.make_packages(xml_source, ctrl_filename, wrk_path, sci_val_res, pmc_val_res)

    #if ctrl_filename is None:
    #    report = PkgReport(scielo_pkg_path, report_path)
    #    report.load_data()
    #    report.generate_articles_report()
    #    report.generate_lists()

    print('\n=======')
    print('\nGenerated packages in:\n' + '\n'.join([scielo_pkg_path, pmc_pkg_path, ]))
    for report_path in list(set([report_path, report_path, ])):
        if os.listdir(report_path):
            print('\nReports in: ' + report_path)
    print('\n==== END ===\n')


###
_versions_ = configure_versions_location()
entities_table = EntitiesTable(ENTITIES_TABLE_FILENAME)
