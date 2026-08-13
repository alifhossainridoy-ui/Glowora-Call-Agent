#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.jarvis_brain import JarvisBrain
from cosmetics.product_brain import CosmeticsProductBrain


class TestJarvisBrain(unittest.TestCase):
    def setUp(self):
        self.brain = JarvisBrain({"name": "Test Shop", "owner": "Test"})
        self.brain.product_brain = CosmeticsProductBrain()

    def test_greeting(self):
        response = self.brain.process("hello", [])
        self.assertIn('text', response)

    def test_check_orders_intent(self):
        response = self.brain.process("check orders", [])
        self.assertEqual(response.get('action', {}).get('type'), 'check_orders')

    def test_call_intent_extracts_number(self):
        response = self.brain.process("call 01712345678", [])
        self.assertEqual(response.get('action', {}).get('number'), '01712345678')

    def test_unknown_command(self):
        response = self.brain.process("asdkjaslkdj random gibberish", [])
        self.assertIn('text', response)


if __name__ == '__main__':
    unittest.main()
