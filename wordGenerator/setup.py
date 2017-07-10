from cx_Freeze import setup, Executable
import sys

base = None

if sys.platform == 'win32':
    base = None


executables = [Executable("wordGenerator.py", base=base)]
packages = ["os","random","pickle","sys","argparse","numpy"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "Word Generator",
    options = options,
    version = "1",
    description = "Generates random words",
    executables = executables
)