import logging
import os
import sys

LOGGER = logging.getLogger(__name__)

LOGGER.debug("importing CLR")
import clr

LOGGER.debug("importing MSL loadlib 32-bit Server")
from msl.loadlib import Server32


class CAN32Wrapper(Server32):
    def __init__(self, host, port, quiet, **kwargs):
        if getattr(sys, "frozen", False):
            base = os.getcwd()
        else:
            base = os.path.dirname(os.path.dirname(__file__))
        dlls = [
            "cpp_lib32",
        ]
        self.dll_path = os.path.join(base, "vendor")
        sys.path.append(self.dll_path)
        self.import_dlls = [clr.AddReference(dll) for dll in dlls]

        LOGGER.debug(f"trying to create 32-bit server with DLL path {self.dll_path}")
        Server32.__init__(
            self,
            os.path.join(self.dll_path, "vendor_plugin.dll"),
            "net",
            host,
            port,
            quiet,
        )

        self.LP = self.lib.vendor_plugin.LoadPlugins

    def Connect(self, hostname):
        # load LN
        self.api3 = self.LP.GetInterfaceApi3(self.dll_path)
        # log events
        self.api3.ErrorEvent += self.OnErrorEvent
        # try connect to inverter
        success = self.api3.Connect(3, "", hostname, False)
        if not success:
            raise ValueError("API connected check returned False.")

    def add(self, a, b):
        """should do an actual lib call:
        
        self.lib.add(a, b)
        """
        return a + b
