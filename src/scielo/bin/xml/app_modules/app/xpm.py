# coding=utf-8

import os

from ..__init__ import _
from . import interface
from ..generics import encoding
from ..generics import fs_utils
from .data import pkg_reception
from .data import pkg_checking
from .data import workarea
from .db import manager
from .pkg_processors import mkp_pkg
from .pkg_processors import pmc_pkgmaker

from .config import config


def call_make_packages(args, version):
    reception = pkg_reception.Reception(manager.Manager(config.Configuration()))

    request = Request(args)
    request.read()
    request.get_pkg_data(reception)

    requester = Requester(request.stage, request.INTERATIVE)
    if request.normalized_pkgfiles is None:
        if request.INTERATIVE is True:
            interface.display_form(False, None, requester.call_make_package_from_gui)
    else:
        requester.execute(request.rcvd_pkg, request.GENERATE_PMC)


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

    def get_pkg_data(self, reception):
        self.stage = 'xpm'
        self.normalized_pkgfiles = None
        self.outputs = {}
        if any([self.xml_path, self.acron]):
            if self.validate():
                if self.sgm_xml is not None:
                    scielo_pm = mkp_pkg.MarkupPackage(self.sgm_xml, self.acron)
                    scielo_pm.make()
                    self.wk = scielo_pm.wk_area
                    self.outputs = {scielo_pm.xml_pkgfiles.name: scielo_pm.sgmxml_outputs}
                    self.normalized_pkgfiles = [scielo_pm.xml_pkgfiles]
                    self.rcvd_pkg = reception.receive(
                        self.normalized_pkgfiles,
                        self.wk,
                        self.outputs)
                    self.stage = 'xml'
                else:
                    file = fs_utils.File(self.xml_list[0])
                    self.wk = workarea.Workarea(file.path + '_' + self.stage)
                    self.normalized_pkgfiles = reception.normalize(
                        self.xml_list, 'remote', self.wk.scielo_package_path)
                    self.rcvd_pkg = reception.receive(
                        self.normalized_pkgfiles,
                        self.wk,
                        None)

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
        self.configuration = config.Configuration()
        self.stage = stage
        self.reception = pkg_reception.Reception(manager.Manager(self.configuration))

    def call_make_package_from_gui(self, xml_path, GENERATE_PMC=False):
        encoding.display_message(_('Making package') + '...')
        xml_list = [xml_path + '/' + item for item in os.listdir(xml_path) if item.endswith('.xml')]

        file = fs_utils.File(xml_list[0])
        wk = workarea.Workarea(file.path + '_' + self.stage)

        normalized_pkgfiles = self.reception.normalize(
            xml_list, 'remote', self.wk.scielo_package_path)
        rcvd_pkg = self.reception.receive(normalized_pkgfiles, wk, None)

        encoding.display_message('...'*3)
        self.execute(rcvd_pkg, GENERATE_PMC)

        encoding.display_message('...'*4)
        return 'done', 'blue'

    def execute(self, rcvd_pkg, GENERATE_PMC=False):
        if rcvd_pkg is not None and len(rcvd_pkg.normalized_pkgfiles) > 0:

            pkg_checker = pkg_checking.PkgChecker(
                self.configuration, self.stage)
            checking = pkg_checking.PkgChecking(pkg_checker, rcvd_pkg)
            checking.check()

            files_location = workarea.AssetsDestinations(
                                rcvd_pkg.wk.scielo_package_path,
                                rcvd_pkg.issue_data.acron)

            checking.report(files_location)

            # pmc package
            if not pkg_checker.is_db_generation:
                pmc_package_maker = pmc_pkgmaker.PMCPackageMaker(
                    rcvd_pkg.wk,
                    rcvd_pkg.articles,
                    rcvd_pkg.outputs)
                if pkg_checker.is_xml_generation:
                    pmc_package_maker.make_report()
                if rcvd_pkg.pkg_issue_data.is_pmc_journal:
                    if GENERATE_PMC:
                        pmc_package_maker.make_package()
                    else:
                        encoding.display_message(
                            _('To generate PMC package, add -pmc as parameter'))

            # zip packages
            if not pkg_checker.is_xml_generation and not pkg_checker.is_db_generation:
                rcvd_pkg.pkgfolder.zip()
                for name, pkgfiles in rcvd_pkg.pkgfiles.items():
                    pkgfiles.zip(rcvd_pkg.pkgfolder.path + '_zips')
