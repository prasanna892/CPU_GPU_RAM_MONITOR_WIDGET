# importing required module
import sys
import subprocess
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

# function to install requirment
def should_install_requirement(requirement):
    should_install = False
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, VersionConflict):
        should_install = True
    return should_install

# function to install missing package one by one and wait for completely install
def install_packages(requirement_list):
    try:
        requirements = [
            requirement
            for requirement in requirement_list
            if should_install_requirement(requirement)
        ]
        if len(requirements) > 0:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *requirements])
        else:
            print("Requirements already satisfied.")

    except Exception as e:
        print(e)

# function to get requirment module to install in list formate
def install(required_modules: list):
    install_packages(required_modules)