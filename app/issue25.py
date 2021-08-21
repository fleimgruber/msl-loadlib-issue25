import logging
import os
import sys

LOGGER = logging.getLogger(__name__)

from msl.loadlib import Client64


class TheApp(Client64):
    def __init__(self):
        LOGGER.debug("determining whether running in a frozen dist")
        if getattr(sys, "frozen", False):
            base = "."
        else:
            base = os.path.join(os.path.dirname(__file__))
        vendor_path = os.path.join(base, "vendor")
        LOGGER.debug(f"trying to create 64-bit client with sys path {vendor_path}")
        Client64.__init__(
            self, module32="app.lib_wrapper", append_sys_path=vendor_path,
        )

    def add(self, a, b):
        return self.request32("add", a, b)


if __name__ == "__main__":
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)

    app = TheApp()

    app.add()
    print('3 + 5 =', app.add(3, 5))
