#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Periodic order checker — polls OrderManager and reports newly arrived pending orders."""

from typing import Callable, List
from business.order_manager import Order, OrderManager


class OrderChecker:
    def __init__(self, order_manager: OrderManager):
        self.order_manager = order_manager
        self._seen_ids = set(order_manager.orders.keys())

    def check_for_new(self) -> List[Order]:
        """Returns orders not seen since the last check_for_new() call."""
        self.order_manager.check_new_orders()
        current_ids = set(self.order_manager.orders.keys())
        new_ids = current_ids - self._seen_ids
        self._seen_ids = current_ids
        return [self.order_manager.orders[i] for i in new_ids]

    def watch(self, on_new_order: Callable[[Order], None], interval_seconds: int = 60):
        """Blocking loop — call in a background thread."""
        import time
        while True:
            for order in self.check_for_new():
                on_new_order(order)
            time.sleep(interval_seconds)
