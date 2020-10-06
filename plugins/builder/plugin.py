from riotgear.plugin import BasePlugin

import subprocess
import multiprocessing  # CPU count
import os
from pathlib import Path


class BuildPlugin(BasePlugin):

    def __init__(self,
                 board=None,
                 application=None,
                 jobs=None,
                 docker=False):

        self.board = board
        if application is not None:
            app_path = Path(application)
        else:
            app_path = Path.cwd()

        if not self._is_application(app_path):
            print("No RIOT application found")
            return

        self.application = app_path
        core_count = multiprocessing.cpu_count()
        self.jobs = jobs if jobs is not None else core_count
        self.use_docker = docker

    def _is_application(self, path):
        makefile = path / "Makefile"
        return makefile.is_file()

    def entry(self):
        call_args = ['BOARD={}'.format(self.board)]
        call_args.append("-j{}".format(self.jobs))
        if self.use_docker:
            call_args.append("BUILD_IN_DOCKER=1")
            call_args.append("DOCKER_MAKE_ARGS=-j{}".format(self.jobs))
        self.build(call_args)

    def build(self, call_args):
        call = ['make', 'all']
        call.extend(call_args)
        subprocess.call(call, cwd=self.application)
