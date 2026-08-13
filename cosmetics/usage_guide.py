#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates a bilingual usage instruction block for a product."""

from cosmetics.product_brain import Product


def format_usage(product: Product, lang: str = 'en') -> str:
    if lang == 'bn':
        text = f"{product.name_bn}\n\n{product.usage_bn}\n\n"
        if product.warnings_bn:
            text += f"সতর্কতা: {product.warnings_bn}"
        return text

    text = f"{product.name}\n\n{product.usage}\n\n"
    if product.warnings:
        text += f"Warning: {product.warnings}"
    return text
