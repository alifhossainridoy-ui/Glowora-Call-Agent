#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smart response generation — bridges JarvisBrain output to speech-ready text."""

from typing import Dict
from voice.bengali_processor import prepare_for_speech


def to_speech_text(response: Dict) -> str:
    """Strip markup/normalize digits so TTS engines get clean text."""
    return prepare_for_speech(response.get('text', ''))
