#!/usr/bin/env python3

import sys
import os
from setuptools import setup

# Make sure I have the right Python version.
if sys.version_info[:2] < (3, 8):
    print("pyMDMix requires Python 3.7 or later. Python %d.%d detected" % sys.version_info[:2])
    print("Please upgrade your version of Python.")
    sys.exit(1)

# Make sure AMBERHOME environ variable is set
if not os.environ.get("AMBERHOME"):
    print("AMBERHOME env variable not set! Please set this variable pointing to AMBER package installation directory.")
    sys.exit(1)

script_list = ["src/mdmix"]


def getRequirements():
    requirements = []
    with open("requirements.txt", "r") as reqfile:
        for line in reqfile.readlines():
            requirements.append(line.strip())
    return requirements


def getVersion():
    return "0.4.0"


setup(
    name="pymdmix",
    zip_safe=False,
    version=getVersion(),
    description="Molecular Dynamics with organic solvent mixtures setup and analysis",
    author="ggutierrez-bio",
    author_email="",
    url="https://github.com/ggutierrez-bio/mdmix4",
    packages=["pymdmix"],
    package_dir={"pymdmix": "pymdmix"},
    scripts=script_list,
    install_requires=getRequirements(),
)
