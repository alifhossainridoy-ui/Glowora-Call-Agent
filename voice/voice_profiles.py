#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Emotion-to-voice-parameter mapping, shared reference used by tts_engine and core.emotion_engine."""

from typing import Dict

EMOTION_VOICE_PARAMS: Dict[str, Dict[str, float]] = {
    'neutral': {'pitch': 1.0, 'speed': 1.0, 'volume': 0.9},
    'happy': {'pitch': 1.15, 'speed': 1.1, 'volume': 0.95},
    'calm': {'pitch': 0.9, 'speed': 0.85, 'volume': 0.8},
    'professional': {'pitch': 1.0, 'speed': 0.95, 'volume': 0.9},
    'urgent': {'pitch': 1.2, 'speed': 1.3, 'volume': 1.0},
    'sympathetic': {'pitch': 0.85, 'speed': 0.8, 'volume': 0.85},
}


def get_params(emotion: str) -> Dict[str, float]:
    return EMOTION_VOICE_PARAMS.get(emotion, EMOTION_VOICE_PARAMS['neutral'])
