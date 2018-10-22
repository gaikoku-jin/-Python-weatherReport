from cx_Freeze import setup, Executable
import sys
import requests
from multiprocessing import Queue

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("weatherReport.py", base=base)]

packages = ["idna"]

buildOptions = dict(excludes = ["tkinter"], includes =["idna.idnadata","multiprocessing"], optimize=1)

options = {
    'build_exe': {

        'packages':["multiprocessing"],
    },

}

setup(
    name = "<any name>",
    options = {"build_exe": buildOptions},
    version = "<any number>",
    description = '<any description>',
    executables = executables
)