#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chrome browser automation — open URLs via Android Intent (order pages, admin panel, etc)."""

from typing import Optional


class ChromeAuto:
    def open_url(self, url: str) -> bool:
        try:
            from jnius import autoclass

            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            intent = Intent(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(url))
            PythonActivity.mActivity.startActivity(intent)
            return True
        except Exception as e:
            print(f"Open URL error: {e}")
            return False
