#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ingredient reference database — short descriptions for common cosmetics actives."""

from typing import Dict, Optional

INGREDIENTS: Dict[str, str] = {
    "vitamin c": "Antioxidant that brightens skin and fades dark spots.",
    "niacinamide": "Reduces oiliness, pore size, and evens skin tone.",
    "hyaluronic acid": "Humectant that draws moisture into the skin.",
    "retinol": "Vitamin A derivative that reduces wrinkles and boosts cell turnover.",
    "salicylic acid": "Beta hydroxy acid that unclogs pores and treats acne.",
    "zinc oxide": "Mineral sunscreen agent providing broad-spectrum UV protection.",
    "ceramides": "Lipids that restore and maintain the skin's moisture barrier.",
    "argan oil": "Nourishing oil rich in vitamin E for hair and skin.",
    "activated charcoal": "Absorbs excess oil and impurities from pores.",
}


def lookup(ingredient: str) -> Optional[str]:
    return INGREDIENTS.get(ingredient.strip().lower())
