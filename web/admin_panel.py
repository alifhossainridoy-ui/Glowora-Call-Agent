#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Admin panel automation — convenience wrapper choosing API vs scraper based on availability."""

from typing import Dict, List, Optional

from web.api_client import APIClient
from web.website_scraper import WebsiteScraper


class AdminPanel:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.api = APIClient(base_url, api_key)
        self.scraper = WebsiteScraper(base_url)
        self._scraper_logged_in = False

    def get_pending_orders(self, fallback_username: Optional[str] = None,
                           fallback_password: Optional[str] = None) -> List[Dict]:
        result = self.api.get('/api/orders', params={'status': 'pending'})
        if result is not None:
            return result.get('orders', [])

        if fallback_username and fallback_password:
            if not self._scraper_logged_in:
                self._scraper_logged_in = self.scraper.login(fallback_username, fallback_password)
            if self._scraper_logged_in:
                return self.scraper.get_new_orders()

        return []
