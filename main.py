#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Root-level entry point required by Buildozer (it looks for main.py in
source.dir). Delegates to app/main.py so the package layout used by
`core`, `voice`, `cosmetics`, etc. (all siblings of app/) stays intact.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import JarvisCosmeticsApp

if __name__ == '__main__':
    JarvisCosmeticsApp().run()
