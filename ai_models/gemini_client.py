#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API Client
Online AI for advanced responses, used as a JarvisBrain fallback
"""

import os
import json
import requests
from typing import Optional, Dict, List


class GeminiClient:
    """
    Google Gemini API Client

    Features:
    - Advanced text generation
    - Bengali language support
    - Customer service responses

    Note: reads GEMINI_API_KEY from the environment — never hardcode the key.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY', '')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-1.5-flash"
        self.initialized = bool(self.api_key)

    def generate(self, prompt: str, history: Optional[List[Dict]] = None,
                 temperature: float = 0.7) -> Optional[str]:
        """Generate text using Gemini API"""
        if not self.initialized:
            return None

        try:
            contents = []

            if history:
                for msg in history[-5:]:
                    role = "user" if msg.get('role') == 'user' else "model"
                    contents.append({"role": role, "parts": [{"text": msg.get('text', '')}]})

            contents.append({"role": "user", "parts": [{"text": prompt}]})

            url = f"{self.base_url}/models/{self.model}:generateContent"
            params = {"key": self.api_key}
            data = {
                "contents": contents,
                "generationConfig": {
                    "temperature": temperature, "maxOutputTokens": 500, "topP": 0.9
                }
            }

            response = requests.post(url, params=params, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                candidates = result.get('candidates', [{}])
                parts = candidates[0].get('content', {}).get('parts', [{}]) if candidates else [{}]
                return parts[0].get('text', '').strip() if parts else ''
            else:
                print(f"Gemini API error: {response.status_code}")
                return None

        except Exception as e:
            print(f"Gemini error: {e}")
            return None

    def analyze_product_review(self, review: str) -> Dict:
        """Analyze product review sentiment"""
        prompt = f"""Analyze this product review:
"{review}"

Return JSON with:
- sentiment (positive/negative/neutral)
- key_points (list)
- rating_estimate (1-5)
- concerns (list)"""

        response = self.generate(prompt, temperature=0.3)

        try:
            return json.loads(response) if response else {}
        except (json.JSONDecodeError, TypeError):
            return {'sentiment': 'neutral', 'key_points': [], 'rating_estimate': 3, 'concerns': []}

    def generate_marketing_text(self, product_name: str, features: List[str]) -> Optional[str]:
        """Generate marketing text for product"""
        prompt = (
            f"Write a short marketing description for:\n"
            f"Product: {product_name}\nFeatures: {', '.join(features)}\n\n"
            f"Write in Bengali and English. Keep it under 100 words."
        )
        return self.generate(prompt, temperature=0.8)
