# coding=utf-8

import os
import shutil
from datetime import datetime


from ..__init__ import _
from ..generics import encoding
from ..generics import fs_utils
from ..generics import xml_utils
from .data import pkg_reception
from .data import workarea
from .config import config
from .server import mailer
from .server import filestransfer


def call_converter(args, version):
    request = Request(args)
    request.read()
    if all([request.package_path, request.collection_acron]):
        errors = xml_utils.is_valid_xml_path(request.package_path)
        if len(errors) > 0:
            messages = []
            messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
            messages.append('ERROR: ' + _('Incorrect parameters'))
            messages.append('\n' + _('Usage') + ':')
            messages.append('python xml_converter.py <xml_folder> | <collection_acron>')
            messages.append(_('where') + ':')
            messages.append('  <xml_folder> = ' + _('path of folder which contains'))
            messages.append('  <collection_acron> = ' + _('collection acron'))
            messages.append('\n'.join(errors))
            encoding.display_message('\n'.join(messages))

    reception = XC_Reception(config.Configuration(config.get_configuration_filename(collection_acron)))
    if request.package_path is None and request.collection_acron is None:
        reception.display_form()
    else:
        package_paths = [request.package_path]
        if request.collection_acron is not None:
            package_paths = reception.queued_packages()
        for request.package_path in package_paths:
            try:
                reception.convert_package(request.package_path)
            except Exception as e:
                encoding.report_exception('convert_package', e, request.package_path)
                raise


class XC_Reception(object):

    def __init__(self, configuration):
        self.configuration = configuration

        self.mailer = mailer.Mailer(configuration)
        self.transfer = filestransfer.FilesTransfer(configuration)
        self.parameters = pkg_checking.ValidationsParameters(configuration, INTERATIVE=configuration.interative_mode, stage='xc')

    def display_form(self):
        if self.configuration.interative_mode is True:
            from . import interface
            interface.display_form(self.parameters.stage == 'xc', None, self.call_convert_package)

    def call_convert_package(self, package_path):
        self.convert_package(package_path)
        return 'done', 'blue'

    def convert_package(self, package_path):
        if package_path is None:
            return False

        wk = workarea.Workarea(package_path + '_xc')

        items = [item for item in os.listdir(package_path) if item.endswith('.xml')]
        received = pkg_reception.ReceivedPackage(items)
        received.normalize('local')
        pkg_info = pkg_reception.PkgInfo(received.pkgfiles, wk)

        encoding.display_message(package_path)
        xc_status = 'interrupted'

        scilista_items = []

        try:
            if len(pkg_info.articles) > 0:
                files_location = workarea.AssetsDestinations(
                                pkg_info.wk.scielo_package_path,
                                pkg_info.issue_data.acron,
                                pkg_info.issue_data.issue_label,
                                self.configuration.serial_path,
                                self.configuration.local_web_app_path,
                                self.configuration.web_app_site)

                pkg_checker = pkg_checking.PackageChecker(
                    self.parameters, pkg_info)
                pkg_checker.check()

                pkg_converter = pkg_conversion.PkgConverter(
                    pkg_checker.registered,
                    pkg_info,
                    pkg_checker.validations_reports,
                    not self.configuration.interative_mode,
                    self.configuration.local_web_app_path,
                    self.configuration.web_app_site
                    )
                scilista_items = pkg_converter.convert()

                pkg_checker.report(files_location, pkg_converter)

                if pkg_checker.registered.issue_files is not None:
                    pkg_checker.registered.issue_files.save_reports(files_location.report_path)
                if self.configuration.web_app_site is not None:
                    for article_files in pkg_info.pkgfiles.values():
                        # copia os xml para report path
                        article_files.copy_xml(files_location.report_path)

                statistics_display = pkg_checker.main_report.validations.statistics_display(html_format=False)                
                xc_status = pkg_converter.xc_status
                subject = ' '.join(EMAIL_SUBJECT_STATUS_ICON.get(xc_status, [])) + ' ' + statistics_display
                mail_content = '<html><body>' + html_reports.link(pkg_checker.main_report.report_link, pkg_checker.main_report.report_link) + '</body></html>'
                mail_info = subject, mail_content
                encoding.display_message(scilista_items)
        except Exception as e:

            if self.configuration.queue_path is not None:
                fs_utils.delete_file_or_folder(package_path)
            self.mailer.mail_step1_failure(pkg_info.pkgfolder.name, e)
            encoding.report_exception('convert_package', e, pkg_info.pkgfolder.name)
            raise
        if len(scilista_items) > 0:
            acron, issue_id = scilista_items[0].split(' ')
            try:
                if xc_status in ['accepted', 'approved']:
                    if self.configuration.collection_scilista is not None:
                        fs_utils.append_file(self.configuration.collection_scilista, '\n'.join(scilista_items) + '\n')
                    self.transfer.transfer_website_files(acron, issue_id)
            except Exception as e:
                self.mailer.mail_step2_failure(pkg_info.pkgfolder.name, e)
                raise
            try:
                if mail_info is not None and self.configuration.email_subject_package_evaluation is not None:
                    mail_subject, mail_content = mail_info
                    self.mailer.mail_results(pkg_info.pkgfolder.name, mail_subject, mail_content)
                self.transfer.transfer_report_files(acron, issue_id)

            except Exception as e:
                self.mailer.mail_step3_failure(pkg_info.pkgfolder.name, e)
                if len(package_path) == 1:
                    encoding.report_exception('convert_package()', e, 'exception as step 3')
        encoding.display_message(_('finished'))

    def queued_packages(self):
        pkg_paths, invalid_pkg_files = self.queue_packages()
        if pkg_paths is None:
            pkg_paths = []
        if len(invalid_pkg_files) > 0:
            self.mailer.mail_invalid_packages(invalid_pkg_files)
        return pkg_paths

    def queue_packages(self):
        download_path = self.configuration.download_path
        temp_path = self.configuration.temp_path
        queue_path = self.configuration.queue_path
        archive_path = self.configuration.archive_path

        invalid_pkg_files = []
        proc_id = datetime.now().isoformat()[11:16].replace(':', '')
        temp_path = temp_path + '/' + proc_id
        queue_path = queue_path + '/' + proc_id
        pkg_paths = []

        if os.path.isdir(temp_path):
            fs_utils.delete_file_or_folder(temp_path)
        if os.path.isdir(queue_path):
            fs_utils.delete_file_or_folder(queue_path)

        if archive_path is not None:
            if not os.path.isdir(archive_path):
                os.makedirs(archive_path)

        if not os.path.isdir(temp_path):
            os.makedirs(temp_path)

        for pkg_name in os.listdir(download_path):
            if fs_utils.is_compressed_file(download_path + '/' + pkg_name):
                shutil.copyfile(download_path + '/' + pkg_name, temp_path + '/' + pkg_name)
            else:
                pkg_paths.append(pkg_name)
            fs_utils.delete_file_or_folder(download_path + '/' + pkg_name)

        for pkg_name in os.listdir(temp_path):
            queued_pkg_path = queue_path + '/' + pkg_name
            if not os.path.isdir(queued_pkg_path):
                os.makedirs(queued_pkg_path)

            if fs_utils.extract_package(temp_path + '/' + pkg_name, queued_pkg_path):
                if archive_path is not None:
                    if os.path.isdir(archive_path):
                        shutil.copyfile(temp_path + '/' + pkg_name, archive_path + '/' + pkg_name)
                pkg_paths.append(queued_pkg_path)
            else:
                invalid_pkg_files.append(pkg_name)
                fs_utils.delete_file_or_folder(queued_pkg_path)
            fs_utils.delete_file_or_folder(temp_path + '/' + pkg_name)
        fs_utils.delete_file_or_folder(temp_path)

        return (pkg_paths, invalid_pkg_files)


class Request(object):

    def __init__(self, args):
        self.read(args)

    def read(self, args):
        args = encoding.fix_args(args)

        self.script = args[0]
        self.package_path = None
        self.collection_acron = None

        if len(args) == 2:
            self.script, param = args
        if os.path.isfile(param) or os.path.isdir(param):
            self.package_path = param
        else:
            self.collection_acron = param
