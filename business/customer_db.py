#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customer Database
Tracks customers seen through orders/calls/WhatsApp for follow-ups and history.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Customer:
    phone: str
    name: str = ""
    address: str = ""
    total_orders: int = 0
    total_spent: float = 0.0
    last_contact: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""


class CustomerDatabase:
    def __init__(self, db_path: str = 'data/customers.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                phone TEXT PRIMARY KEY,
                name TEXT,
                address TEXT,
                total_orders INTEGER DEFAULT 0,
                total_spent REAL DEFAULT 0,
                last_contact TEXT,
                notes TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def upsert(self, customer: Customer):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (phone, name, address, total_orders, total_spent, last_contact, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(phone) DO UPDATE SET
                name=excluded.name, address=excluded.address,
                total_orders=excluded.total_orders, total_spent=excluded.total_spent,
                last_contact=excluded.last_contact, notes=excluded.notes
        ''', (customer.phone, customer.name, customer.address, customer.total_orders,
              customer.total_spent, customer.last_contact, customer.notes))
        conn.commit()
        conn.close()

    def record_order(self, phone: str, name: str, address: str, amount: float):
        customer = self.get(phone) or Customer(phone=phone, name=name, address=address)
        customer.name = name or customer.name
        customer.address = address or customer.address
        customer.total_orders += 1
        customer.total_spent += amount
        customer.last_contact = datetime.now().isoformat()
        self.upsert(customer)

    def get(self, phone: str) -> Optional[Customer]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE phone = ?", (phone,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return Customer(phone=row[0], name=row[1], address=row[2],
                         total_orders=row[3], total_spent=row[4],
                         last_contact=row[5], notes=row[6] or "")

    def get_all(self) -> List[Customer]:
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY last_contact DESC")
        rows = cursor.fetchall()
        conn.close()
        return [Customer(phone=r[0], name=r[1], address=r[2], total_orders=r[3],
                          total_spent=r[4], last_contact=r[5], notes=r[6] or "") for r in rows]

    def get_top_customers(self, limit: int = 10) -> List[Customer]:
        return sorted(self.get_all(), key=lambda c: c.total_spent, reverse=True)[:limit]
