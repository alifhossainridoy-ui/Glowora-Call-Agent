#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp Full Automation
Opens chats and pre-fills messages via Android Intent / ADB, on your own device.
No API needed - controls the phone's own WhatsApp app.
"""

import time
import subprocess
from typing import Optional, Dict, List


class WhatsAppFullAuto:
    """
    WhatsApp Automation

    Features:
    - Open a chat with a pre-filled message
    - Send order confirmations / follow-ups / delivery notices from templates
    - Bulk messaging (opens one chat at a time, user taps send)
    """

    def __init__(self):
        self.package_name = "com.whatsapp"  # or "com.whatsapp.w4b" for Business
        self.device_connected = self._check_device()
        self.message_templates = self._load_templates()
        self.last_message = ""

    def _check_device(self) -> bool:
        """Check if an Android device is connected via ADB"""
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
            lines = [l for l in result.stdout.splitlines()[1:] if l.strip()]
            return any(l.endswith('device') for l in lines)
        except Exception:
            return False

    def _load_templates(self) -> Dict[str, str]:
        """Load message templates"""
        return {
            'order_confirm': """Assalamu Alaikum!

Your order has been confirmed at {business_name}.

Order ID: {order_id}
Product: {product}
Price: TK{price}

Delivery: 2-3 business days
Payment: Cash on Delivery

Thank you for shopping with us!

{business_name}
{phone}""",

            'follow_up': """Assalamu Alaikum!

This is {business_name}. We noticed you were interested in our products.

Would you like to:
- See our new arrivals
- Get a special discount
- Know about ongoing offers

Reply to let us know!

{business_name}""",

            'delivery': """Assalamu Alaikum!

Your order #{order_id} is out for delivery today.

Please keep your phone available.

Thank you!
{business_name}""",

            'thank_you': """Assalamu Alaikum!

Thank you for your purchase from {business_name}!

We hope you love your products. Please share your feedback.

Follow us for new arrivals and offers!

{business_name}"""
        }

    def _normalize_number(self, number: str) -> str:
        """Normalize a Bangladeshi phone number to international format"""
        number = ''.join(ch for ch in number if ch.isdigit())
        if number.startswith('0'):
            return '88' + number
        if not number.startswith('88'):
            return '88' + number
        return number

    def send_message(self, number: str, message: str,
                     business_info: Optional[Dict] = None) -> bool:
        """
        Open a WhatsApp chat with the message pre-filled.
        The user still taps Send in WhatsApp — this does not auto-send.

        Args:
            number: Phone number (01XXXXXXXXX format)
            message: Message text
            business_info: Business details for template substitution
        """
        number = self._normalize_number(number)

        if business_info:
            message = message.format(**business_info)

        try:
            self._open_whatsapp_chat(number, message)
            self.last_message = message
            return True
        except Exception as e:
            print(f"WhatsApp send error: {e}")
            return False

    def _open_whatsapp_chat(self, number: str, message: str):
        """Open WhatsApp chat with pre-filled text using Android Intent (preferred)"""
        try:
            from jnius import autoclass

            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            wa_url = f"https://wa.me/{number}"

            intent = Intent(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(wa_url))
            intent.setPackage(self.package_name)
            intent.putExtra("android.intent.extra.TEXT", message)

            PythonActivity.mActivity.startActivity(intent)

        except Exception as e:
            print(f"Intent error: {e}")
            self._open_via_adb(number)

    def _open_via_adb(self, number: str):
        """Open WhatsApp chat via ADB using an Android intent (no shell string injection)"""
        wa_url = f"https://wa.me/{number}"
        subprocess.run([
            'adb', 'shell', 'am', 'start', '-a', 'android.intent.action.VIEW',
            '-d', wa_url, '-p', self.package_name
        ], timeout=15)
        time.sleep(1)

    def send_template(self, number: str, template_name: str,
                      template_data: Dict, business_info: Dict) -> bool:
        """Send a template message"""
        template = self.message_templates.get(template_name, '')
        if not template:
            return False

        data = {**business_info, **template_data}
        message = template.format(**data)

        return self.send_message(number, message)

    def send_order_confirmation(self, number: str, order_id: str,
                                product: str, price: float,
                                business_info: Dict) -> bool:
        """Send order confirmation message"""
        return self.send_template(
            number, 'order_confirm',
            {'order_id': order_id, 'product': product, 'price': price},
            business_info
        )

    def send_follow_up(self, number: str, business_info: Dict) -> bool:
        """Send follow-up message"""
        return self.send_template(number, 'follow_up', {}, business_info)

    def send_delivery_notice(self, number: str, order_id: str,
                             business_info: Dict) -> bool:
        """Send delivery notice"""
        return self.send_template(number, 'delivery', {'order_id': order_id}, business_info)

    def send_thank_you(self, number: str, business_info: Dict) -> bool:
        """Send thank you message"""
        return self.send_template(number, 'thank_you', {}, business_info)

    def bulk_message(self, numbers: List[str], message: str, delay: int = 5) -> Dict[str, bool]:
        """
        Open chats for multiple numbers with the same pre-filled message.

        Args:
            numbers: List of phone numbers
            message: Message text
            delay: Delay between chats in seconds (avoid triggering spam detection)
        """
        results = {}

        for number in numbers:
            success = self.send_message(number, message)
            results[number] = success

            if not success:
                print(f"Failed to open chat for {number}")

            time.sleep(delay)

        return results

    def check_whatsapp_installed(self) -> bool:
        """Check if WhatsApp is installed"""
        try:
            result = subprocess.run(
                ['adb', 'shell', 'pm', 'list', 'packages', self.package_name],
                capture_output=True, text=True, timeout=10
            )
            return self.package_name in result.stdout
        except Exception:
            return False
