#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phone Dialer + Call Management
Automated calling using Android Intent, with ADB fallback (argument-list, no shell injection)
"""

import time
import subprocess
from typing import Optional


class PhoneDialer:
    """
    Phone automation for calls and SMS

    Features:
    - Make calls
    - Send SMS (opens the SMS app pre-filled — user taps send)
    - Call history / duration tracking
    - Redial
    """

    def __init__(self):
        self.current_call = None
        self.call_history = []

    def make_call(self, number: str) -> bool:
        """Make a phone call"""
        try:
            from jnius import autoclass

            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            intent = Intent(Intent.ACTION_CALL)
            intent.setData(Uri.parse(f"tel:{number}"))

            PythonActivity.mActivity.startActivity(intent)

            self.current_call = {
                'number': number,
                'start_time': time.time(),
                'status': 'dialing'
            }

            return True

        except Exception as e:
            print(f"Call error: {e}")
            return self._call_via_adb(number)

    def _call_via_adb(self, number: str) -> bool:
        """Make call via ADB (argument list, not a shell string)"""
        try:
            subprocess.run([
                'adb', 'shell', 'am', 'start', '-a', 'android.intent.action.CALL',
                '-d', f'tel:{number}'
            ], timeout=15, check=True)
            return True
        except Exception:
            return False

    def send_sms(self, number: str, message: str) -> bool:
        """Open the SMS app pre-filled with number and message"""
        try:
            from jnius import autoclass

            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            intent = Intent(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(f"sms:{number}"))
            intent.putExtra("sms_body", message)

            PythonActivity.mActivity.startActivity(intent)

            return True

        except Exception as e:
            print(f"SMS error: {e}")
            return self._sms_via_adb(number, message)

    def _sms_via_adb(self, number: str, message: str) -> bool:
        """Send SMS intent via ADB (argument list, not a shell string)"""
        try:
            subprocess.run([
                'adb', 'shell', 'am', 'start', '-a', 'android.intent.action.SENDTO',
                '-d', f'sms:{number}', '--es', 'sms_body', message
            ], timeout=15, check=True)
            return True
        except Exception:
            return False

    def end_call(self) -> bool:
        """End current call"""
        try:
            subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_ENDCALL'], timeout=10)

            if self.current_call:
                self.current_call['end_time'] = time.time()
                self.current_call['duration'] = (
                    self.current_call['end_time'] - self.current_call['start_time']
                )
                self.call_history.append(self.current_call)
                self.current_call = None

            return True
        except Exception:
            return False

    def get_call_duration(self) -> Optional[float]:
        """Get current call duration"""
        if self.current_call and self.current_call.get('start_time'):
            return time.time() - self.current_call['start_time']
        return None

    def redial(self) -> bool:
        """Redial last number"""
        if self.call_history:
            last_number = self.call_history[-1]['number']
            return self.make_call(last_number)
        return False

    def get_call_history(self) -> list:
        """Get call history"""
        return self.call_history

    def send_order_call_script(self, number: str, order_id: str,
                               product_name: str, business_name: str) -> bool:
        """Call customer and print a suggested script for the shop owner to read"""
        script = f"""Assalamu Alaikum!

This is {business_name}.

Your order #{order_id} for {product_name} has been confirmed.

Total: Please check your message for details.

Delivery: 2-3 business days.

Thank you for shopping with us!"""

        success = self.make_call(number)
        print(f"Call Script:\n{script}")
        return success
