from riotgear.plugin import BasePlugin

import os
from pathlib import Path

DEFAULT_BOARD = "native"
DEFAULT_RIOTBASE = "$(CURDIR)/../RIOT"

MAKEFILE_TEMPLATE = """# name of your application
APPLICATION = {}

# If no BOARD is found in the environment, use this default:
BOARD ?= {}

# This has to be the absolute path to the RIOT base directory:
RIOTBASE ?= {}

# Comment this out to disable code in RIOT that does safety checking
# which is not needed in a production environment but helps in the
# development process:
DEVELHELP ?= 1

# Change this to 0 show compiler invocation lines by default:
QUIET ?= 1

include $(RIOTBASE)/Makefile.include
"""

MAIN_C_TEMPLATE = """#include <stdio.h>

int main(void)
{
    puts("Hello World!");

    printf("You are running RIOT on a(n) %s board.\\n", RIOT_BOARD);
    printf("This board features a(n) %s MCU.\\n", RIOT_MCU);

    return 0;
}
"""

class NewPlugin(BasePlugin):
    def __init__(self,
                 application=None,
                 board=None,
                 riotbase=None):
        if application is not None:
            app_path = Path(application)
        else:
            app_path = Path.cwd()

        if self._is_application(app_path):
            print("`{}` is already a RIOT application".format(app_path.parts[-1]))
            return

        self.application = app_path
        self.board = board
        self.riotbase = riotbase

    def entry(self):
        if not self.application.exists():
            self.application.mkdir(exist_ok=True)

        makefile = self.application / "Makefile"
        makefile.write_text(self._makefile())

        main_c = self.application / "main.c"
        main_c.write_text(MAIN_C_TEMPLATE)

    def _makefile(self):
        app = self.application.parts[-1]

        if self.board is not None:
            board = self.board
        else:
            board = DEFAULT_BOARD

        if self.riotbase is not None:
            riotbase = self.riotbase
        else:
            riotbase = DEFAULT_RIOTBASE

        return MAKEFILE_TEMPLATE.format(app, board, riotbase)

    def _is_application(self, path):
        makefile = path / "Makefile"
        return makefile.is_file()
