#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android Accessibility Service helper
Screen reading / tapping / scrolling via ADB (argument-list calls — no shell injection)
"""

import subprocess
from typing import Optional, List, Tuple


class JarvisAccessibilityService:
    """
    Android Accessibility Service helper for Jarvis

    Features:
    - Click coordinates / scroll / navigate
    - Type text in the focused field
    - Take screenshots
    - Read the currently focused app

    Note: actually reading screen content by element text requires a real
    Android AccessibilityService (Java/Kotlin) registered in the APK manifest;
    this class covers the ADB-drivable subset usable from Python.
    """

    def __init__(self):
        self.enabled = False

    def enable(self) -> bool:
        """Enable accessibility service for this app"""
        try:
            subprocess.run([
                'adb', 'shell', 'settings', 'put', 'secure', 'enabled_accessibility_services',
                'org.jarvis.cosmetics/org.jarvis.cosmetics.JarvisAccessibilityService'
            ], timeout=10, check=True)
            self.enabled = True
            return True
        except Exception:
            return False

    def tap(self, x: int, y: int) -> bool:
        """Tap a screen coordinate"""
        try:
            subprocess.run(['adb', 'shell', 'input', 'tap', str(int(x)), str(int(y))], timeout=10, check=True)
            return True
        except Exception:
            return False

    def type_text(self, text: str) -> bool:
        """Type text in the currently focused field"""
        try:
            chunk_size = 100
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i + chunk_size]
                subprocess.run(['adb', 'shell', 'input', 'text', chunk], timeout=10, check=True)
            return True
        except Exception:
            return False

    def scroll(self, direction: str = 'down', distance: int = 500) -> bool:
        """Scroll the screen"""
        try:
            if direction == 'down':
                args = ['500', '1500', '500', str(1500 - distance)]
            elif direction == 'up':
                args = ['500', '500', '500', str(500 + distance)]
            elif direction == 'left':
                args = ['800', '1000', str(800 - distance), '1000']
            elif direction == 'right':
                args = ['200', '1000', str(200 + distance), '1000']
            else:
                return False
            subprocess.run(['adb', 'shell', 'input', 'swipe', *args], timeout=10, check=True)
            return True
        except Exception:
            return False

    def press_back(self):
        subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_BACK'], timeout=10)

    def press_home(self):
        subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_HOME'], timeout=10)

    def press_recent(self):
        subprocess.run(['adb', 'shell', 'input', 'keyevent', 'KEYCODE_APP_SWITCH'], timeout=10)

    def take_screenshot(self, filename: str = "screen.png") -> str:
        """Take a screenshot and pull it to the local machine"""
        remote_path = f"/sdcard/{filename}"
        subprocess.run(['adb', 'shell', 'screencap', '-p', remote_path], timeout=15)
        subprocess.run(['adb', 'pull', remote_path], timeout=15)
        return filename

    def get_current_app(self) -> str:
        """Get currently focused app/window"""
        try:
            result = subprocess.run(
                ['adb', 'shell', 'dumpsys', 'window'],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.splitlines():
                if 'mCurrentFocus' in line:
                    return line.strip()
        except Exception:
            pass
        return ""

    def read_screen_text(self) -> List[str]:
        """Placeholder — real implementation needs the registered AccessibilityService."""
        return []

    def find_text_coordinates(self, text: str) -> Optional[Tuple[int, int]]:
        """Placeholder — parse a UI Automator XML dump to locate element coordinates."""
        return None
