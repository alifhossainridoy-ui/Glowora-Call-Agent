#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Price, offer, and stock helpers layered on top of CosmeticsProductBrain."""

from typing import List, Optional
from cosmetics.product_brain import CosmeticsProductBrain, Product


class PriceEngine:
    def __init__(self, product_brain: CosmeticsProductBrain):
        self.product_brain = product_brain

    def products_under_budget(self, budget: float) -> List[Product]:
        return [p for p in self.product_brain.products.values()
                if p.is_active and p.price <= budget]

    def apply_discount(self, product_id: str, percent: float) -> Optional[float]:
        product = self.product_brain.products.get(product_id)
        if not product:
            return None
        return round(product.price * (1 - percent / 100), 2)

    def cheapest_in_category(self, category: str) -> Optional[Product]:
        items = self.product_brain.get_by_category(category)
        return min(items, key=lambda p: p.price) if items else None
