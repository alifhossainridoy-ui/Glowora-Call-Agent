#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bengali text normalization helpers shared by STT/TTS."""

import re

BANGLA_DIGITS = str.maketrans('０১২৩৪৫৬৭৮৯', '0123456789') if False else str.maketrans(
    '০১২৩৪৫৬৭৮৯', '0123456789'
)


def normalize_digits(text: str) -> str:
    """Convert Bangla numerals to Arabic numerals."""
    return text.translate(BANGLA_DIGITS)


def collapse_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def strip_markup(text: str) -> str:
    """Remove Kivy markup tags before sending text to TTS."""
    return re.sub(r'\[/?[a-zA-Z=,#0-9 ]+\]', '', text)


def prepare_for_speech(text: str) -> str:
    text = strip_markup(text)
    text = normalize_digits(text)
    return collapse_whitespace(text)
