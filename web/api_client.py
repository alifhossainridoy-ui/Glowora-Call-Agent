#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thin REST API client used by OrderManager / InventorySync when the website exposes an API."""

from typing import Any, Dict, Optional
import requests


class APIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}

    def get(self, path: str, params: Optional[Dict] = None) -> Optional[Any]:
        try:
            resp = requests.get(f"{self.base_url}{path}", params=params,
                                 headers=self.headers, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"API GET {path} failed: {e}")
        return None

    def post(self, path: str, data: Optional[Dict] = None) -> Optional[Any]:
        try:
            resp = requests.post(f"{self.base_url}{path}", json=data,
                                  headers=self.headers, timeout=self.timeout)
            if resp.status_code in (200, 201):
                return resp.json()
        except Exception as e:
            print(f"API POST {path} failed: {e}")
        return None
