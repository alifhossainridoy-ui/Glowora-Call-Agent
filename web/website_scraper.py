#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Website Scraper
Automated scraping of website orders and data (fallback when no API is available)
"""

from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebsiteScraper:
    """
    Website Scraper for Order Management

    Features:
    - Login to admin panel
    - Scrape new orders
    - Update order status
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.driver = None
        self.logged_in = False

    def start_browser(self):
        """Start headless browser"""
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)

    def login(self, username: str, password: str) -> bool:
        """Login to admin panel"""
        if not self.driver:
            self.start_browser()

        try:
            self.driver.get(f"{self.base_url}/admin/login")

            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(username)

            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(password)

            login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_btn.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
            )

            self.logged_in = True
            return True

        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def get_new_orders(self) -> List[Dict]:
        """Get new orders from admin panel"""
        if not self.logged_in:
            return []

        try:
            self.driver.get(f"{self.base_url}/admin/orders?status=pending")

            orders_table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "orders-table"))
            )

            orders = []
            rows = orders_table.find_elements(By.TAG_NAME, "tr")

            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 5:
                    orders.append({
                        'order_id': cells[0].text,
                        'customer': cells[1].text,
                        'phone': cells[2].text,
                        'total': cells[3].text,
                        'status': cells[4].text
                    })

            return orders

        except Exception as e:
            print(f"Get orders failed: {e}")
            return []

    def update_order_status(self, order_id: str, status: str) -> bool:
        """Update order status"""
        if not self.logged_in:
            return False

        try:
            self.driver.get(f"{self.base_url}/admin/orders/{order_id}")

            status_select = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "status"))
            )
            status_select.send_keys(status)

            update_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            update_btn.click()

            return True

        except Exception as e:
            print(f"Update status failed: {e}")
            return False

    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logged_in = False
