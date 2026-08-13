#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bengali/English prompt templates shared by TinyLlama and Gemini clients."""

SYSTEM_PROMPT_BN = (
    "তুমি জার্ভিস, একজন সহায়ক কসমেটিক্স ব্যবসার সহকারী। "
    "তুমি পণ্যের সুপারিশ, অর্ডার ব্যবস্থাপনা এবং গ্রাহক সেবায় সাহায্য করো।"
)

SYSTEM_PROMPT_EN = (
    "You are Jarvis, a helpful cosmetics business assistant. "
    "You help with product recommendations, order management, and customer service."
)


def customer_reply_prompt(query: str, context: str = '') -> str:
    return f"Customer query: {query}\nContext: {context}\nProfessional reply:"


def product_description_prompt(product_name: str, ingredients: list) -> str:
    return f"Write a short product description for {product_name}.\nIngredients: {', '.join(ingredients)}\nDescription:"
