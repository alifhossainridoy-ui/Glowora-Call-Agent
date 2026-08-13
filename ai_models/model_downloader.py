#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convenience entry point for downloading offline models (TinyLlama, Vosk)."""

from ai_models.tinyllama_manager import TinyLlamaManager
from voice.stt_engine import MultiEngineSTT


def download_all():
    print("Downloading TinyLlama...")
    TinyLlamaManager().download_model()

    print("Downloading Vosk Bengali STT model...")
    MultiEngineSTT().download_vosk_model()


if __name__ == '__main__':
    download_all()
