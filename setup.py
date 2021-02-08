#!/usr/bin/env python3

import sys
from setuptools import setup

# Make sure I have the right Python version.
if sys.version_info[:2] < (3, 8):
    print("pyMDMix requires Python 3.7 or later. Python %d.%d detected" % sys.version_info[:2])
    print("Please upgrade your version of Python.")
    sys.exit(1)


def getRequirements():
    requirements = []
    with open("requirements.txt", "r") as reqfile:
        for line in reqfile.readlines():
            requirements.append(line.strip())
    return requirements


def getVersion():
    return "4.0.0"


setup(
    name="pymdmix-core",
    zip_safe=False,
    version=getVersion(),
    description="Molecular Dynamics with organic solvent mixtures setup and analysis",
    author="ggutierrez-bio",
    author_email="",
    url="https://github.com/ggutierrez-bio/mdmix4",
    packages=["pymdmix_core"],
    inlcude_package_data=True,
    data_files=[("pymdmix", ["defaults/pymdmix_core.yml"])],
    # package_dir={"pymdmix_core": "pymdmix_core"},
    scripts=["bin/mdmix"],
    install_requires=getRequirements(),
)
