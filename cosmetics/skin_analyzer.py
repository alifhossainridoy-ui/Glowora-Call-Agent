#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skin analysis engine — thin wrapper around JarvisBrain's skin-type logic for reuse outside chat."""

from typing import Optional
from core.jarvis_brain import JarvisBrain


class SkinAnalyzer:
    def __init__(self):
        self._brain = JarvisBrain({})

    def detect_skin_type(self, text: str) -> Optional[str]:
        return self._brain._extract_skin_type(text.lower())

    def detect_concern(self, text: str) -> Optional[str]:
        return self._brain._extract_concern(text.lower())

    def get_routine(self, skin_type: str) -> str:
        return self._brain._get_skin_analysis(skin_type)
