#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="jarvis-cosmetics-ai",
    version="2.0.0",
    description="Bengali voice AI assistant for cosmetics business automation",
    packages=find_packages(exclude=("tests", "app")),
    python_requires=">=3.8",
)
