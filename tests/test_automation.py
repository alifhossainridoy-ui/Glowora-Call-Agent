#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from automation.whatsapp_full_auto import WhatsAppFullAuto


class TestWhatsAppAuto(unittest.TestCase):
    def setUp(self):
        self.wa = WhatsAppFullAuto()

    def test_normalize_number_local_format(self):
        self.assertEqual(self.wa._normalize_number("01712345678"), "8801712345678")

    def test_normalize_number_already_international(self):
        self.assertEqual(self.wa._normalize_number("8801712345678"), "8801712345678")

    def test_template_rendering(self):
        template = self.wa.message_templates['order_confirm']
        rendered = template.format(
            business_name="Test Shop", phone="017", order_id="1", product="Cream", price=100
        )
        self.assertIn("Test Shop", rendered)
        self.assertIn("Order ID: 1", rendered)


if __name__ == '__main__':
    unittest.main()
