# coding=utf-8

import os
from __init__ import _

import email_service
import xc_config


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


def get_mailer(config):
    if config.is_enabled_email_service:
        return email_service.EmailService(config.email_sender_name, config.email_sender_email)


def get_configuration(collection_acron):
    config = None
    f = configuration_filename(collection_acron)
    errors = invalid_configuration_file_message(f)
    if len(errors) > 0:
        print('\n'.join(errors))
    else:
        config = xc_config.XMLConverterConfiguration(f)
        if not config.valid:
            config = None
    return config


def configuration_filename(collection_acron):
    if collection_acron is None:
        filename = CURRENT_PATH + '/../../scielo_paths.ini'
    else:
        filename = CURRENT_PATH + '/../config/' + collection_acron + '.xc.ini'
    return filename


def invalid_configuration_file_message(configuration_filename):
    messages = []
    if configuration_filename is None:
        messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
        messages.append('ERROR: ' + _('No configuration file was informed'))
    elif not os.path.isfile(configuration_filename):
        messages.append('\n===== ' + _('ATTENTION') + ' =====\n')
        messages.append('ERROR: ' + _('unable to read XML Converter configuration file: ') + configuration_filename)
    return messages


def run_remote_mkdirs(user, server, path):
    try:
        print('ssh ' + user + '@' + server + ' "mkdir -p ' + path + '"')
        os.system('ssh ' + user + '@' + server + ' "mkdir -p ' + path + '"')
    except:
        pass


def run_rsync(source, user, server, dest):
    try:
        print('nohup rsync -CrvK ' + source + '/* ' + user + '@' + server + ':' + dest + '&\n')
        os.system('nohup rsync -CrvK ' + source + '/* ' + user + '@' + server + ':' + dest + '&\n')
    except:
        pass


def run_scp(source, user, server, dest):
    try:
        print('nohup scp -r ' + source + ' ' + user + '@' + server + ':' + dest + '&\n')
        os.system('nohup scp -r ' + source + ' ' + user + '@' + server + ':' + dest + '&\n')
    except:
        pass
