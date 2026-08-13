#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cosmetics Product Brain
Product catalog, recommendations, skin matching
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Product:
    id: str
    name: str
    name_bn: str
    category: str
    price: float
    stock: int
    description: str
    description_bn: str
    ingredients: List[str]
    skin_types: List[str]
    concerns: List[str]
    usage: str
    usage_bn: str
    warnings: str
    warnings_bn: str
    brand: str
    size: str
    rating: float
    reviews_count: int
    is_active: bool = True


class CosmeticsProductBrain:
    """
    Cosmetics Product Intelligence Engine

    Features:
    - Product catalog management
    - Skin type matching
    - Concern-based recommendations
    - Ingredient analysis
    - Price comparison
    """

    def __init__(self, db_path: str = 'data/products.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        self.products: Dict[str, Product] = {}
        self.load_products()

    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                name_bn TEXT,
                category TEXT,
                price REAL,
                stock INTEGER DEFAULT 0,
                description TEXT,
                description_bn TEXT,
                ingredients TEXT,
                skin_types TEXT,
                concerns TEXT,
                usage TEXT,
                usage_bn TEXT,
                warnings TEXT,
                warnings_bn TEXT,
                brand TEXT,
                size TEXT,
                rating REAL DEFAULT 0,
                reviews_count INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            )
        ''')

        conn.commit()
        conn.close()

    def load_products(self, json_path: str = 'data/products.json'):
        """Load products from JSON file"""
        json_file = Path(json_path)
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for p in data.get('products', []):
                    product = Product(**p)
                    self.products[product.id] = product
                    self._save_to_db(product)

    def _save_to_db(self, product: Product):
        """Save product to database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO products
            (id, name, name_bn, category, price, stock, description, description_bn,
             ingredients, skin_types, concerns, usage, usage_bn, warnings, warnings_bn,
             brand, size, rating, reviews_count, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product.id, product.name, product.name_bn, product.category,
            product.price, product.stock, product.description, product.description_bn,
            json.dumps(product.ingredients), json.dumps(product.skin_types),
            json.dumps(product.concerns), product.usage, product.usage_bn,
            product.warnings, product.warnings_bn, product.brand, product.size,
            product.rating, product.reviews_count, int(product.is_active)
        ))

        conn.commit()
        conn.close()

    def get_product(self, query: str) -> Optional[Product]:
        """Get product by name or ID"""
        query = query.lower()

        for pid, product in self.products.items():
            if query == pid.lower() or query == product.name.lower():
                return product

        for pid, product in self.products.items():
            if query in product.name.lower() or query in product.name_bn.lower():
                return product

        for pid, product in self.products.items():
            if query in product.category.lower():
                return product

        return None

    def recommend(self, skin_type: Optional[str] = None,
                  concern: Optional[str] = None,
                  budget: Optional[float] = None) -> List[Product]:
        """Recommend products based on skin type and concern"""
        matches = []

        for product in self.products.values():
            if not product.is_active or product.stock <= 0:
                continue

            score = 0

            if skin_type and skin_type.lower() in [s.lower() for s in product.skin_types]:
                score += 3

            if concern and concern.lower() in [c.lower() for c in product.concerns]:
                score += 3

            if budget and product.price > budget:
                continue

            score += product.rating * 0.5

            if score > 0:
                matches.append((score, product))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in matches[:5]]

    def search_by_ingredient(self, ingredient: str) -> List[Product]:
        """Search products by ingredient"""
        ingredient = ingredient.lower()
        return [
            p for p in self.products.values()
            if any(ingredient in ing.lower() for ing in p.ingredients)
        ]

    def get_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        category = category.lower()
        return [
            p for p in self.products.values()
            if category in p.category.lower() and p.is_active
        ]

    def check_stock(self, product_id: str) -> int:
        """Check product stock"""
        product = self.products.get(product_id)
        return product.stock if product else 0

    def update_stock(self, product_id: str, quantity: int):
        """Update product stock"""
        if product_id in self.products:
            self.products[product_id].stock += quantity
            self._save_to_db(self.products[product_id])

    def get_low_stock(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock"""
        return [
            p for p in self.products.values()
            if p.stock <= threshold and p.is_active
        ]

    def add_product(self, product: Product):
        """Add new product"""
        self.products[product.id] = product
        self._save_to_db(product)

    def get_all_categories(self) -> List[str]:
        """Get all unique categories"""
        categories = {p.category for p in self.products.values()}
        return sorted(categories)

    def get_popular_products(self, limit: int = 10) -> List[Product]:
        """Get popular products by rating and reviews"""
        sorted_products = sorted(
            self.products.values(),
            key=lambda p: (p.rating * p.reviews_count),
            reverse=True
        )
        return sorted_products[:limit]
