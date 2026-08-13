#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cosmetics.product_brain import CosmeticsProductBrain


class TestProducts(unittest.TestCase):
    def setUp(self):
        self.brain = CosmeticsProductBrain()

    def test_get_product(self):
        p = self.brain.get_product("Glow Brightening")
        self.assertIsNotNone(p)

    def test_recommend(self):
        recs = self.brain.recommend(skin_type='oily', concern='acne')
        self.assertTrue(len(recs) > 0)

    def test_low_stock(self):
        low = self.brain.get_low_stock(threshold=100)
        self.assertIsInstance(low, list)


if __name__ == '__main__':
    unittest.main()
