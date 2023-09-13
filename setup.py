#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="enigma",
    version="0.1",
    description="Python emulation of Enigma M3.",
    author="Mizaimao",
    packages=find_packages(include=["enigma", "enigma.*"]),
)
