
import os
import platform
from ...generics import system
from ...generics import encoding


so = platform.platform().lower()


def info(venv_path):
    if 'windows' in so:
        venv_path = venv_path.replace('/', '\\')
        activate = '{}\\Scripts\\activate'.format(venv_path)
        deactivate = '{}\\Scripts\\deactivate'.format(venv_path)
        sep = ' & '
    else:
        activate = 'source {}/bin/activate'.format(venv_path)
        deactivate = 'deactivate'
        sep = ';'
    if venv_path is None or not os.path.isdir(venv_path):
        activate = ''
        deactivate = ''
    return activate, deactivate, sep


class AppCaller(object):

    def __init__(self, venv_path=None):
        self.venv_path = venv_path
        self.activate_command, self.deactivate_command, self.sep = info(venv_path)

    def install(self, requirements_file, requirements_checker):
        if self.venv_path is not None:
            if not os.path.isdir(self.venv_path):
                system.run_command('pip install virtualenv', True)
                system.run_command(u'virtualenv {}'.format(self.venv_path), True)
        self.install_requirements(
            requirements_file,
            requirements_checker)

    def execute(self, commands):
        _commands = []
        encoding.debugging('app_caller.execute()', commands)
        if os.path.isdir(self.venv_path):
            _commands.append(u'echo Activating {}'.format(self.venv_path))
            _commands.append(self.activate_command)
            _commands.append('python -V')
        _commands.extend(commands)
        if os.path.isdir(self.venv_path):
            _commands.append(self.deactivate_command)
            _commands.append(u'echo Deactivating {}'.format(self.venv_path))
        _commands = [item for item in _commands if len(item) > 0]
        encoding.debugging('app_caller.execute()', self.sep.join(_commands))
        encoding.debugging(self.sep.join(_commands))
        system.run_command(self.sep.join(_commands))

    def install_requirements(self, requirements_file, requirements_checker):
        commands = []
        commands.append('pip install -r {}'.format(requirements_file))
        commands.append('python {}'.format(requirements_checker))
        self.execute(commands)
