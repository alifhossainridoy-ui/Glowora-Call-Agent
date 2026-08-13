#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smart follow-up system — flags customers who haven't ordered or been contacted recently."""

from datetime import datetime, timedelta
from typing import List

from business.customer_db import CustomerDatabase, Customer


class FollowUpEngine:
    def __init__(self, customer_db: CustomerDatabase, stale_days: int = 14):
        self.customer_db = customer_db
        self.stale_days = stale_days

    def get_due_for_follow_up(self) -> List[Customer]:
        """Customers not contacted in `stale_days` days."""
        cutoff = datetime.now() - timedelta(days=self.stale_days)
        due = []
        for customer in self.customer_db.get_all():
            try:
                last = datetime.fromisoformat(customer.last_contact)
            except ValueError:
                continue
            if last < cutoff:
                due.append(customer)
        return due
