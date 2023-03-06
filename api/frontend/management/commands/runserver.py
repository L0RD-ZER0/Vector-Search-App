import sys
from os import getcwd as _cwd
import sys as _sys
import signal
import atexit

from django.core.management.commands.runserver import Command as RunServer


class Command(RunServer):
    def inner_run(self, *args, **options):
        self.pre_start()
        super().inner_run(*args, **options)

    def pre_start(self):
        _sys.path.append(_cwd())
        import libs
        libs.init()
        atexit.register(self._exit)
        # signal.signal(signal.SIGINT, self._handle_SIGINT)

    def _exit(self):
        import libs
        libs.teardwn()

    def _handle_SIGINT(self, sig, frame):
        self._exit()
        sys.exit(0)
