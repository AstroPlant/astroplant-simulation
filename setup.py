#!/usr/bin/env python

from setuptools import setup

setup(
    name="astroplant-simulation",
    version="0.1",
    description="AstroPlant environment simulation",
    author="AstroPlant",
    author_email="thomas@kepow.org",
    url="https://astroplant.io",
    packages=["astroplant_simulation",],
    install_requires=["numpy~=1.0", "pillow~=8.0", "schedule~=0.6"],
)
