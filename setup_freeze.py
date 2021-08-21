#!/usr/bin/python
import sys

from cx_Freeze import setup, Executable

# env = "app"

include_files = list([("vendor/", "vendor/")])

if sys.platform == "win32":
    base = None
    packages = ["pkg_resources", "app"]
    build_exe_options = {
        "packages": packages,
        "include_msvcr": True,
        "include_files": include_files,
    }

setup(
    name="app",
    version="0.1.0",
    description="An App",
    author="fleimgruber",
    author_email="fabio.leimgruber@posteo.eu",
    url="https://github.com/fleimgruber/app.git",
    options={"build_exe": build_exe_options},
    executables=[Executable("app/issue25.py", targetName="issue25.exe", base=base),],
)
