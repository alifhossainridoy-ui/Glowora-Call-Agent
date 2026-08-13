#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Order Management System
Handle orders from website, track status, auto-notify customers
"""

import json
import sqlite3
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Order:
    id: str
    customer_name: str
    customer_phone: str
    customer_address: str
    products: List[Dict]
    total_amount: float
    status: str  # pending, confirmed, processing, shipped, delivered, cancelled
    payment_status: str  # pending, paid, cod
    payment_method: str  # cod, bkash, nagad, card
    created_at: str
    updated_at: str
    notes: str = ""
    delivery_date: Optional[str] = None
    tracking_number: Optional[str] = None


class OrderManager:
    """
    Order Management System

    Features:
    - Check new orders from website API
    - Confirm / cancel / ship / deliver orders
    - Daily reports
    """

    def __init__(self, website_url: str, db_path: str = 'data/orders.db'):
        self.website_url = website_url
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        self.orders: Dict[str, Order] = {}
        self.load_orders()

    def _init_database(self):
        """Initialize orders database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                customer_name TEXT,
                customer_phone TEXT,
                customer_address TEXT,
                products TEXT,
                total_amount REAL,
                status TEXT DEFAULT 'pending',
                payment_status TEXT DEFAULT 'pending',
                payment_method TEXT,
                created_at TEXT,
                updated_at TEXT,
                notes TEXT,
                delivery_date TEXT,
                tracking_number TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def load_orders(self):
        """Load orders from database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()

        for row in rows:
            order = Order(
                id=row[0], customer_name=row[1], customer_phone=row[2],
                customer_address=row[3],
                products=json.loads(row[4]) if row[4] else [],
                total_amount=row[5], status=row[6], payment_status=row[7],
                payment_method=row[8], created_at=row[9], updated_at=row[10],
                notes=row[11] or "", delivery_date=row[12], tracking_number=row[13]
            )
            self.orders[order.id] = order

        conn.close()

    def _save_order(self, order: Order):
        """Save order to database"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO orders
            (id, customer_name, customer_phone, customer_address, products,
             total_amount, status, payment_status, payment_method, created_at,
             updated_at, notes, delivery_date, tracking_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order.id, order.customer_name, order.customer_phone,
            order.customer_address, json.dumps(order.products),
            order.total_amount, order.status, order.payment_status,
            order.payment_method, order.created_at, order.updated_at,
            order.notes, order.delivery_date, order.tracking_number
        ))

        conn.commit()
        conn.close()

    def check_new_orders(self) -> List[Order]:
        """Check for new orders from website API"""
        try:
            new_orders = self._fetch_from_api()
            for order_data in new_orders:
                order = self._create_order_from_data(order_data)
                self.orders[order.id] = order
                self._save_order(order)
        except Exception as e:
            print(f"Order sync failed: {e}")

        return [o for o in self.orders.values() if o.status == 'pending']

    def _fetch_from_api(self) -> List[Dict]:
        """Fetch pending orders from the website's API"""
        api_url = f"{self.website_url}/api/orders?status=pending"
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                return response.json().get('orders', [])
        except Exception:
            pass
        return []

    def _create_order_from_data(self, data: Dict) -> Order:
        """Create Order object from API data"""
        return Order(
            id=data.get('order_id', ''),
            customer_name=data.get('customer_name', ''),
            customer_phone=data.get('customer_phone', ''),
            customer_address=data.get('address', ''),
            products=data.get('products', []),
            total_amount=float(data.get('total', 0)),
            status=data.get('status', 'pending'),
            payment_status=data.get('payment_status', 'pending'),
            payment_method=data.get('payment_method', 'cod'),
            created_at=data.get('created_at', datetime.now().isoformat()),
            updated_at=datetime.now().isoformat()
        )

    def confirm_order(self, order_id: str) -> bool:
        """Confirm an order"""
        if order_id not in self.orders:
            return False

        order = self.orders[order_id]
        order.status = 'confirmed'
        order.updated_at = datetime.now().isoformat()

        self._save_order(order)
        self._update_website_status(order_id, 'confirmed')
        return True

    def cancel_order(self, order_id: str, reason: str = "") -> bool:
        """Cancel an order"""
        if order_id not in self.orders:
            return False

        order = self.orders[order_id]
        order.status = 'cancelled'
        order.notes = reason
        order.updated_at = datetime.now().isoformat()

        self._save_order(order)
        self._update_website_status(order_id, 'cancelled')
        return True

    def ship_order(self, order_id: str, tracking_number: str) -> bool:
        """Mark order as shipped"""
        if order_id not in self.orders:
            return False

        order = self.orders[order_id]
        order.status = 'shipped'
        order.tracking_number = tracking_number
        order.updated_at = datetime.now().isoformat()

        self._save_order(order)
        return True

    def deliver_order(self, order_id: str) -> bool:
        """Mark order as delivered"""
        if order_id not in self.orders:
            return False

        order = self.orders[order_id]
        order.status = 'delivered'
        order.updated_at = datetime.now().isoformat()

        if order.payment_method == 'cod':
            order.payment_status = 'paid'

        self._save_order(order)
        return True

    def get_order(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id)

    def get_orders_by_status(self, status: str) -> List[Order]:
        return [o for o in self.orders.values() if o.status == status]

    def get_today_orders(self) -> List[Order]:
        today = datetime.now().strftime('%Y-%m-%d')
        return [o for o in self.orders.values() if o.created_at.startswith(today)]

    def get_pending_orders(self) -> List[Order]:
        return self.get_orders_by_status('pending')

    def get_confirmed_orders(self) -> List[Order]:
        return self.get_orders_by_status('confirmed')

    def get_daily_report(self) -> Dict:
        """Generate daily report"""
        today_orders = self.get_today_orders()

        total_sales = sum(o.total_amount for o in today_orders if o.status != 'cancelled')

        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_orders': len(today_orders),
            'total_sales': total_sales,
            'pending': len([o for o in today_orders if o.status == 'pending']),
            'confirmed': len([o for o in today_orders if o.status == 'confirmed']),
            'cancelled': len([o for o in today_orders if o.status == 'cancelled']),
            'cod_orders': len([o for o in today_orders if o.payment_method == 'cod']),
            'online_payments': len([o for o in today_orders if o.payment_method != 'cod'])
        }

    def get_customer_orders(self, phone: str) -> List[Order]:
        return [o for o in self.orders.values() if o.customer_phone == phone]

    def _update_website_status(self, order_id: str, status: str):
        """Update order status on website"""
        try:
            api_url = f"{self.website_url}/api/orders/{order_id}/status"
            requests.post(api_url, json={'status': status}, timeout=10)
        except Exception:
            pass

    def get_low_stock_alerts(self, product_brain) -> List[Dict]:
        """Get products that need restocking"""
        low_stock = product_brain.get_low_stock(threshold=10)
        return [
            {'product_id': p.id, 'name': p.name, 'stock': p.stock, 'needed': 50 - p.stock}
            for p in low_stock
        ]
