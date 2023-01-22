##Build.py
from TouchPortalAPI import tppbuild

# first, some values which may be used in multiple places below
# the base file name for the plugin's main file, w/out .py extension
#pluginFileName = "Better Raids"

"""
PLUGIN_MAIN: This lets tppbuild know where your main python plugin file is located so it will know which file to compile.
"""
PLUGIN_MAIN = "./src/process_checker.py"

"""
PLUGIN_EXE_NAME: This defines what you want your plugin executable to be named. tppbuild will also use this for the .tpp file in the format:
                `pluginname + "_v" + version + "_" + os_name + ".tpp"`
                If left blank, the file name from PLUGIN_MAIN is used (w/out .py extension).
"""
PLUGIN_EXE_NAME = "Process_Monitor"

"""
PLUGIN_EXE_ICON: This should be a path to a .ico file. However if png passed in, it will automatically converted to ico.
"""
PLUGIN_EXE_ICON = r""


"""
PLUGIN_ENTRY: This can be either path to entry.tp or path to a python file that contains infomation about entry.
Note if you pass in a entry.tp, tppbuild will automatically validate the json. If you pass in a python file, it will
build entry.tp & validate it for you. If validation fails, tppbuild will exit.
"""
PLUGIN_ENTRY = "entry.tp"  # Here we just use the same file as the plugin's main code since that contains all the definitions for entry.tp.

PLUGIN_ENTRY_INDENT = 2

""" This is the root folder name that will be inside of .tpp """
PLUGIN_ROOT = "Process_Monitor"

""" Path to icon file used in entry.tp for category `imagepath`, if any. If left blank, TP will use a default icon. """
PLUGIN_ICON = r""

""" This tells tppbuild where you want finished build tpp to be saved at. Default "./" meaning current dir where tppbuild is running from. """
OUTPUT_PATH = r"./"

""" PLUGIN_VERSION: A version string for the generated .tpp file name. This example reads the `__version__` from the example plugin's code. """
import json
import os

entry = os.path.join(os.path.split(__file__)[0], PLUGIN_ENTRY)
with open(entry, "r") as f:
    PLUGIN_VERSION = str(json.load(f)['version'])

# Or just set the PLUGIN_VERSION manually.
#PLUGIN_VERSION = "1.6"

"""
If you have any required file(s) that your plugin needs, put them in this list.
"""
ADDITIONAL_FILES = ["./src/start.sh", "./src/process_monitor_icon"]

"""
Any additional arguments to be passed to Pyinstaller. Optional.
"""
ADDITIONAL_PYINSTALLER_ARGS = [
    "--log-level=WARN",
    "--noconsole"
]

ADDITIONAL_TPPSDK_ARGS = [""]

# validateBuild()

if __name__ == "__main__":
    tppbuild.runBuild()
