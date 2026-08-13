#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Daily/weekly business report formatting on top of OrderManager."""

from datetime import datetime, timedelta
from typing import Dict, List

from business.order_manager import OrderManager


class ReportGenerator:
    def __init__(self, order_manager: OrderManager):
        self.order_manager = order_manager

    def daily_text_report(self) -> str:
        r = self.order_manager.get_daily_report()
        return (
            f"Daily Report — {r['date']}\n\n"
            f"Total Orders: {r['total_orders']}\n"
            f"Total Sales: TK{r['total_sales']:.2f}\n"
            f"Pending: {r['pending']} | Confirmed: {r['confirmed']} | Cancelled: {r['cancelled']}\n"
            f"COD: {r['cod_orders']} | Online Payment: {r['online_payments']}"
        )

    def weekly_report(self) -> Dict:
        """Aggregate daily reports over the last 7 days (in-memory orders only)."""
        today = datetime.now()
        days: List[str] = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

        totals = {'total_orders': 0, 'total_sales': 0.0}
        for day in days:
            day_orders = [o for o in self.order_manager.orders.values() if o.created_at.startswith(day)]
            totals['total_orders'] += len(day_orders)
            totals['total_sales'] += sum(o.total_amount for o in day_orders if o.status != 'cancelled')

        totals['from'] = days[-1]
        totals['to'] = days[0]
        return totals
