#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from voice.bengali_processor import normalize_digits, prepare_for_speech


class TestBengaliProcessor(unittest.TestCase):
    def test_normalize_digits(self):
        self.assertEqual(normalize_digits("দাম ৪৫০ টাকা"), "দাম 450 টাকা")

    def test_prepare_for_speech_strips_markup(self):
        result = prepare_for_speech("[b]Hello[/b]  world")
        self.assertEqual(result, "Hello world")


class TestTTSEngine(unittest.TestCase):
    def test_import_and_construct(self):
        try:
            from voice.tts_engine import RealisticTTSEngine
        except ImportError:
            self.skipTest("kivy/gtts not installed in this environment")
            return
        tts = RealisticTTSEngine(cache_dir='data/voice_cache')
        self.assertIn('gtts', tts.engines)


if __name__ == '__main__':
    unittest.main()
