import logging

from prodtools.utils import email_service

LOGGER = logging.getLogger(__name__)

class Mailer(object):

    def __init__(self, config):
        self.config = config
        self.mailer = None
        if config.is_enabled_email_service:
            self.mailer = email_service.EmailService(config.email_sender_name, config.email_sender_email,
                config.email_server)

    def send_message(self, to, subject, text, attaches=[]):
        if not self.config.is_enabled_email_service:
            LOGGER.info("Could not send this email. The mailer service is disabled")
            return None
        elif self.mailer is None:
            LOGGER.info(
                "Could not send this email. The mailer service isn't configured"
            )
            return None
        self.mailer.send_message(to, subject, text, attaches)

    def mail_invalid_packages(self, invalid_pkg_files):
        icon = u"\u274C"
        subject = "{}: {} ".format(
            self.config.email_subject_invalid_packages, icon)
        body = "{}{}\n\nPackages are not .zip file or has no XML file"

        for invalid_pkg in invalid_pkg_files:
            self.send_message(
                self.config.email_to,
                subject + invalid_pkg,
                body.format(
                    self.config.email_text_invalid_packages,
                    invalid_pkg
                )
            )

    def mail_failure(self, subject: str, text: str, package: str) -> None:
        """Informa falhas gerais ocorridas durante a conversão de pacotes SPS"""
        subject = "{} {}: {}".format(
            self.config.email_subject_conversion_failure, subject, package
        )
        self.send_message(self.config.email_to_adm, subject, text)

    def mail_results(self, package_folder, results, report_location):
        if self.config.is_enabled_email_service:
            self.send_message(self.config.email_to, self.config.email_subject_package_evaluation + u' ' + package_folder + u': ' + results, report_location)

