#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SMS automation — thin convenience wrapper over PhoneDialer.send_sms."""

from typing import Dict, List
from automation.phone_dialer import PhoneDialer


class SMSAuto:
    def __init__(self):
        self.dialer = PhoneDialer()

    def send(self, number: str, message: str) -> bool:
        return self.dialer.send_sms(number, message)

    def bulk_send(self, numbers: List[str], message: str) -> Dict[str, bool]:
        return {n: self.send(n, message) for n in numbers}
