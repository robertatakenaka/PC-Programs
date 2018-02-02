# coding=utf-8

import os

from ..__init__ import _
from . import interface
from ..generics import encoding
from ..generics import fs_utils
from .data import pkg_reception
from .data import pkg_checking
from .data import workarea
from .pkg_processors import mkp_pkg
from .config import config


def call_make_packages(args, version):
    request = Request(args)
    request.read()
    request.get_pkg_data()
    requester = Requester(request.stage, request.INTERATIVE)
    if request.normalized_pkgfiles is None:
        if request.INTERATIVE is True:
            interface.display_form(False, None, requester.call_make_package_from_gui)
    else:
        requester.execute(request.normalized_pkgfiles, request.wk, request.GENERATE_PMC)


class Request(object):

    def __init__(self, args):
        self.read(args)

    def read(self, args):
        self.INTERATIVE = True
        self.GENERATE_PMC = False
        args = encoding.fix_args(args)
        self.script = args[0]
        self.xml_path = None
        self.acron = None

        items = []
        for item in args:
            if item == '-auto':
                self.INTERATIVE = False
            elif item == '-pmc':
                self.GENERATE_PMC = True
            else:
                items.append(item)

        if len(items) == 3:
            self.script, self.xml_path, self.acron = items
        elif len(items) == 2:
            self.script, self.xml_path = items
        if self.xml_path is not None:
            self.xml_path = self.xml_path.replace('\\', '/')

    def validate(self):
        errors = self.evaluate_xml_path()
        if len(errors) > 0:
            messages = []
            messages.append('\n===== ATTENTION =====\n')
            messages.append('ERROR: ' + _('Incorrect parameters'))
            messages.append('\n' + _('Usage') + ':')
            messages.append('python ' + script + ' <xml_src> [-auto]')
            messages.append(_('where') + ':')
            messages.append('  <xml_src> = ' + _('XML filename or path which contains XML files'))
            messages.append('  [-auto]' + _('optional parameter to omit report'))
            messages.append('\n'.join(errors))
            encoding.display_message('\n'.join(messages))
            return False
        return True

    def get_pkg_data(self):
        self.stage = 'xpm'
        self.normalized_pkgfiles = None
        self.outputs = {}
        if any([self.xml_path, self.acron]):
            if self.validate():
                if self.sgm_xml is not None:
                    scielo_pm = mkp_pkg.MarkupPackage(self.sgm_xml, self.acron)
                    scielo_pm.make()
                    self.outputs = {scielo_pm.xml_pkgfiles.name: scielo_pm.sgmxml_outputs}
                    self.normalized_pkgfiles = [scielo_pm.xml_pkgfiles]
                    self.stage = 'xml'
                else:
                    file = fs_utils.File(self.xml_list[0])
                    self.wk = workarea.Workarea(file.path + '_' + self.stage)
                    pkg_received = pkg_reception.ReceivedPackage(self.xml_list)
                    pkg_received.normalize('remote')
                    self.normalized_pkgfiles = pkg_received.pkgfiles
                    self.outputs = pkg_received.outputs

    def evaluate_xml_path(self):
        errors = []
        self.sgm_xml = None
        self.xml_list = None

        if self.xml_path is None:
            errors.append(_('Missing XML location. '))
        else:
            if os.path.isfile(self.xml_path):
                if self.xml_path.endswith('.sgm.xml'):
                    self.sgm_xml = self.xml_path
                elif self.xml_path.endswith('.xml'):
                    self.xml_list = [self.xml_path]
                else:
                    errors.append(_('Invalid file. XML file required. '))
            elif os.path.isdir(self.xml_path):
                self.xml_list = [self.xml_path + '/' + item for item in os.listdir(self.xml_path) if item.endswith('.xml')]

                if len(self.xml_list) == 0:
                    errors.append(_('Invalid folder. Folder must have XML files. '))
            else:
                errors.append(_('Missing XML location. '))
        return errors


class Requester(object):

    def __init__(self, stage, INTERATIVE=True):
        configuration = config.Configuration()
        self.stage = stage
        self.parameters = pkg_checking.ValidationsParameters(configuration, INTERATIVE, stage)

    def call_make_package_from_gui(self, xml_path, GENERATE_PMC=False):
        encoding.display_message(_('Making package') + '...')
        xml_list = [xml_path + '/' + item for item in os.listdir(xml_path) if item.endswith('.xml')]

        file = fs_utils.File(xml_list[0])
        wk = workarea.Workarea(file.path + '_' + self.stage)

        encoding.display_message('...'*2)
        pkg_received = pkg_reception.ReceivedPackage(xml_list)
        pkg_received.normalize('remote')

        encoding.display_message('...'*3)
        self.execute(pkg_received.pkgfiles, wk, GENERATE_PMC)

        encoding.display_message('...'*4)
        return 'done', 'blue'

    def execute(self, normalized_pkgfiles, wk, GENERATE_PMC=False):
        if len(normalized_pkgfiles) > 0:
            pkg_info = pkg_reception.PkgInfo(normalized_pkgfiles, wk)

            pkg_checker = pkg_checking.PackageChecker(
                self.parameters, pkg_info)
            pkg_checker.check()
            files_location = workarea.AssetsDestinations(
                                pkg_info.wk.scielo_package_path,
                                pkg_info.issue_data.acron)

            pkg_checker.report(files_location)

            # pmc package
            if not self.parameters.is_db_generation:
                pmc_package_maker = pmc_pkgmaker.PMCPackageMaker(
                    pkg_info.wk,
                    pkg_info.articles,
                    pkg_info.outputs)
                if self.parameters.is_xml_generation:
                    pmc_package_maker.make_report()
                if pkg_info.pkg_issue_data.is_pmc_journal:
                    if GENERATE_PMC:
                        pmc_package_maker.make_package()
                    else:
                        encoding.display_message(
                            _('To generate PMC package, add -pmc as parameter'))

            # zip packages
            if not self.parameters.is_xml_generation and not self.parameters.is_db_generation:
                pkg_info.pkgfolder.zip()
                for name, pkgfiles in pkg_info.pkgfiles.items():
                    pkgfiles.zip(pkg_info.pkgfolder.path + '_zips')
