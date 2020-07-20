import os
import pathlib
import shutil

CODE_PATH = pathlib.Path(__file__).parent.absolute()
PACKAGE_PATH = CODE_PATH.parent.absolute()

def setupVenv():
    # create virtual environment for python
    print("CREATING VIRTUAL ENVIRONMENT")
    # get cwd
    cwd = os.getcwd()
    print("Current directory:", cwd)
    print("Package directory:", PACKAGE_PATH)
    # change directory to package folder then install
    print("Changing directory to:", PACKAGE_PATH)
    os.chdir(PACKAGE_PATH)
    print("Creating virtual environment in the following directory:", PACKAGE_PATH)
    os.system("python3 -m venv env")
    # change directory back
    print("Changing directory to:", cwd)
    os.chdir(cwd)
    print("DONE")

    return

def addActivator():
    print("ADDING ACTIVATOR FOR VENV")
    print("Code directory:", CODE_PATH)
    print("Package directory:", PACKAGE_PATH)
    # get path to activate_this file
    file_path = str(CODE_PATH) + "/activate_this.py"
    print("File path:", file_path)
    # get path to bin folder
    bin_path = str(PACKAGE_PATH) + "/env/bin/"
    print("env/bin directory:", bin_path)
    # add activate_this.py
    shutil.copyfile(file_path, bin_path + "activate_this.py")
    print("DONE")

    return

def activate(): 
    print("ACTIVATING VENV")
    activator = str(PACKAGE_PATH) + "/env/bin/activate_this.py"

    # activate
    with open(activator) as f:
        exec(f.read(), {'__file__': activator})
    print("ACTIVATED")

    return

def install():
    # install packages
    # -----------------
    # get cwd
    cwd = os.getcwd()
    print("Current directory:", cwd)
    print("Package directory:", PACKAGE_PATH)
    os.chdir(PACKAGE_PATH)
    print("Changed directory to:", os.getcwd())

    print("INSTALLING DEPENDENCIES")
    os.system("pip install --upgrade pip")
    # install dependencies
    os.system("pip install -r requirements.txt")
    # change directory back
    print("Changing directory to:", cwd)
    os.chdir(cwd)
    print("DONE")

    return
