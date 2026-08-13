#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stock synchronization — reconciles local product stock with website API stock levels."""

from typing import Dict, List
import requests

from cosmetics.product_brain import CosmeticsProductBrain


class InventorySync:
    def __init__(self, website_url: str, product_brain: CosmeticsProductBrain):
        self.website_url = website_url
        self.product_brain = product_brain

    def push_stock(self, product_id: str) -> bool:
        """Push local stock level for one product to the website API"""
        product = self.product_brain.products.get(product_id)
        if not product:
            return False
        try:
            requests.post(
                f"{self.website_url}/api/products/{product_id}/stock",
                json={'stock': product.stock}, timeout=10
            )
            return True
        except Exception as e:
            print(f"Stock push failed: {e}")
            return False

    def pull_stock(self) -> List[Dict]:
        """Pull stock levels from website and apply them locally"""
        try:
            response = requests.get(f"{self.website_url}/api/products/stock", timeout=10)
            if response.status_code != 200:
                return []
            updates = response.json().get('products', [])
            for item in updates:
                pid = item.get('id')
                stock = item.get('stock')
                if pid in self.product_brain.products and stock is not None:
                    self.product_brain.products[pid].stock = stock
                    self.product_brain._save_to_db(self.product_brain.products[pid])
            return updates
        except Exception as e:
            print(f"Stock pull failed: {e}")
            return []
