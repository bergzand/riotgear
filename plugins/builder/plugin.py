from riotgear.plugin import BasePlugin

import subprocess
import multiprocessing  # CPU count


class BuildPlugin(BasePlugin):

    def __init__(self,
                 board=None,
                 application=None,
                 jobs=None,
                 docker=False):

        self.board = board
        self.application = application

        core_count = multiprocessing.cpu_count()
        self.jobs = jobs if jobs is not None else core_count
        self.use_docker = docker

    def entry(self):
        call = ['make', 'all', 'BOARD={}'.format(self.board)]
        call.append("-j{}".format(self.jobs))
        if self.use_docker:
            call.append("BUILD_IN_DOCKER=1")
            call.append("DOCKER_MAKE_ARGS=-j{}".format(self.jobs))
        print(call)
        subprocess.call(call, cwd=self.application)
