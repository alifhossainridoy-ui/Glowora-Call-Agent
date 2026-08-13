#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Cosmetics AI Assistant v2.0
Bangla language cosmetics business automation assistant
"""

import os
import sys
import json
import threading
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.jarvis_brain import JarvisBrain
from cosmetics.product_brain import CosmeticsProductBrain
from voice.tts_engine import RealisticTTSEngine
from voice.stt_engine import MultiEngineSTT

APP_NAME = "Jarvis Cosmetics AI"
VERSION = "2.0.0"
WAKE_WORDS = ["jarvis", "hello jarvis", "ei jarvis", "jarvish"]
STOP_WORDS = ["bondho koro", "thamo", "stop", "shutdown", "biday"]

COLORS = {
    'primary': (0.15, 0.45, 0.85, 1),
    'secondary': (0.95, 0.3, 0.5, 1),
    'accent': (1, 0.75, 0.2, 1),
    'success': (0.2, 0.8, 0.4, 1),
    'warning': (1, 0.6, 0.1, 1),
    'danger': (0.9, 0.2, 0.2, 1),
    'dark': (0.08, 0.08, 0.12, 1),
    'light': (0.95, 0.95, 0.97, 1),
    'card': (0.12, 0.14, 0.18, 1),
}

DEFAULT_BUSINESS = {
    "name": "Your Cosmetics Shop",
    "owner": "Sir",
    "phone": "017XXXXXXXX",
    "website": "https://your-cosmetics-shop.com",
    "address": "Your Address",
    "working_hours": "10 AM - 10 PM",
    "categories": [
        "Facial Cream", "Serum", "Sunscreen", "Moisturizer",
        "Cleanser", "Toner", "Makeup", "Lipstick", "Eyeshadow",
        "Perfume", "Body Lotion", "Hair Care", "Face Mask",
        "Eye Cream", "Lip Balm", "Primer", "BB Cream"
    ]
}


class JarvisMainUI(BoxLayout):
    status_text = StringProperty("Jarvis ready...")
    is_listening = BooleanProperty(False)
    is_speaking = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [15, 10, 15, 10]
        self.spacing = 10
        self._init_components()
        self._build_ui()
        self._setup_animations()
        Clock.schedule_once(self._delayed_init, 1.0)

    def _init_components(self):
        self.business = self._load_business_config()
        self.conversation_history = []
        self.is_auto_mode = True
        self.wake_sound = None
        self.success_sound = None
        self._load_sounds()

        self.product_brain = CosmeticsProductBrain()
        self.brain = JarvisBrain(self.business)
        self.brain.product_brain = self.product_brain

        try:
            self.tts = RealisticTTSEngine()
        except Exception:
            self.tts = None
        try:
            self.stt = MultiEngineSTT()
        except Exception:
            self.stt = None

    def _load_business_config(self):
        config_path = Path(__file__).parent.parent / 'data' / 'business_config.json'
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_BUSINESS

    def _load_sounds(self):
        assets_path = Path(__file__).parent.parent / 'assets' / 'sounds'
        try:
            self.wake_sound = SoundLoader.load(str(assets_path / 'wake_sound.mp3'))
            self.success_sound = SoundLoader.load(str(assets_path / 'success_sound.mp3'))
        except Exception:
            pass

    def _build_ui(self):
        self._build_header()
        self._build_status_bar()
        self._build_chat_area()
        self._build_quick_actions()
        self._build_control_panel()

    def _build_header(self):
        header = BoxLayout(size_hint_y=0.08, spacing=10)

        avatar = Image(source='assets/icons/bot_avatar.png', size_hint_x=0.12)
        header.add_widget(avatar)

        title_box = BoxLayout(orientation='vertical', size_hint_x=0.6)
        title = Label(
            text=f'[b]{APP_NAME}[/b]', markup=True, font_size='22sp',
            color=COLORS['light'], halign='left', valign='center'
        )
        title.bind(size=title.setter('text_size'))
        title_box.add_widget(title)

        subtitle = Label(
            text=f'v{VERSION} | {self.business["name"]}',
            font_size='12sp', color=(0.6, 0.6, 0.7, 1), halign='left'
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        title_box.add_widget(subtitle)
        header.add_widget(title_box)

        settings_btn = Button(
            text='Settings', font_size='14sp', size_hint_x=0.15,
            background_color=COLORS['card'], background_normal=''
        )
        settings_btn.bind(on_press=self._show_settings)
        header.add_widget(settings_btn)

        self.add_widget(header)

    def _build_status_bar(self):
        self.status_bar = BoxLayout(size_hint_y=0.06, padding=[10, 5])

        with self.status_bar.canvas.before:
            Color(*COLORS['card'])
            self.status_rect = RoundedRectangle(
                pos=self.status_bar.pos, size=self.status_bar.size, radius=[10]
            )
        self.status_bar.bind(pos=self._update_status_rect, size=self._update_status_rect)

        self.status_indicator = Label(
            text='O', font_size='20sp', color=COLORS['success'], size_hint_x=0.1
        )
        self.status_bar.add_widget(self.status_indicator)

        self.status_label = Label(
            text=self.status_text, font_size='14sp', color=COLORS['light'],
            size_hint_x=0.7, halign='left'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.status_bar.add_widget(self.status_label)

        self.auto_toggle = Button(
            text='AUTO', font_size='12sp', size_hint_x=0.2,
            background_color=COLORS['success'], background_normal=''
        )
        self.auto_toggle.bind(on_press=self._toggle_auto_mode)
        self.status_bar.add_widget(self.auto_toggle)

        self.add_widget(self.status_bar)

    def _build_chat_area(self):
        chat_container = BoxLayout(size_hint_y=0.55, padding=[5, 5])

        with chat_container.canvas.before:
            Color(0.06, 0.07, 0.1, 1)
            RoundedRectangle(pos=chat_container.pos, size=chat_container.size, radius=[15])

        scroll = ScrollView()
        self.chat_layout = GridLayout(
            cols=1, spacing=10, padding=[10, 10], size_hint_y=None
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))

        self._add_bot_message(
            f"Hello {self.business['owner']}!\n\n"
            f"I am Jarvis, your cosmetics business assistant.\n"
            f"I can help you with:\n\n"
            f"Order Management\n"
            f"Customer Calls\n"
            f"WhatsApp Auto Reply\n"
            f"Product Info & Suggestions\n"
            f"Reports & Analytics\n\n"
            f"Say 'Jarvis' to call me!"
        )

        scroll.add_widget(self.chat_layout)
        chat_container.add_widget(scroll)
        self.add_widget(chat_container)

    def _build_quick_actions(self):
        actions_box = GridLayout(cols=4, size_hint_y=0.18, spacing=8, padding=[5, 5])

        actions = [
            ('Orders', self._quick_order),
            ('Call', self._quick_call),
            ('WhatsApp', self._quick_whatsapp),
            ('Products', self._quick_product),
            ('Report', self._quick_report),
            ('Customer', self._quick_customer),
            ('Reminder', self._quick_reminder),
            ('All Orders', self._quick_all_orders),
        ]

        for label, callback in actions:
            btn = Button(
                text=label, font_size='14sp',
                background_color=COLORS['card'], background_normal='',
                color=COLORS['light']
            )
            btn.bind(on_press=callback)
            actions_box.add_widget(btn)

        self.add_widget(actions_box)

    def _build_control_panel(self):
        control = BoxLayout(size_hint_y=0.13, spacing=15, padding=[10, 5])

        self.mic_btn = Button(
            text='MIC', font_size='20sp', size_hint_x=0.25,
            background_color=COLORS['primary'], background_normal=''
        )
        self.mic_btn.bind(on_press=self._on_mic_press)
        control.add_widget(self.mic_btn)

        self.text_input = TextInput(
            hint_text='Type here or tap MIC...',
            font_size='16sp', multiline=False, size_hint_x=0.55,
            background_color=COLORS['card'], foreground_color=COLORS['light'],
            padding=[15, 15]
        )
        self.text_input.bind(on_text_validate=self._on_text_submit)
        control.add_widget(self.text_input)

        send_btn = Button(
            text='SEND', font_size='18sp', size_hint_x=0.2,
            background_color=COLORS['secondary'], background_normal=''
        )
        send_btn.bind(on_press=self._on_send_press)
        control.add_widget(send_btn)

        self.add_widget(control)

    def _setup_animations(self):
        self.mic_pulse = Animation(
            background_color=COLORS['secondary'], duration=0.5
        ) + Animation(background_color=COLORS['primary'], duration=0.5)
        self.mic_pulse.repeat = True

    def _update_status_rect(self, instance, value):
        self.status_rect.pos = instance.pos
        self.status_rect.size = instance.size

    def _add_user_message(self, text):
        msg_box = BoxLayout(size_hint_y=None, height=60, padding=[50, 5, 10, 5])
        with msg_box.canvas.before:
            Color(*COLORS['primary'])
            RoundedRectangle(pos=msg_box.pos, size=msg_box.size, radius=[15, 15, 2, 15])

        label = Label(text=text, font_size='15sp', color=COLORS['light'],
                      halign='right', valign='center')
        label.bind(size=label.setter('text_size'))
        msg_box.add_widget(label)
        self.chat_layout.add_widget(msg_box)
        self._scroll_to_bottom()

    def _add_bot_message(self, text):
        msg_box = BoxLayout(size_hint_y=None, height=80, padding=[10, 5, 50, 5])
        with msg_box.canvas.before:
            Color(*COLORS['card'])
            RoundedRectangle(pos=msg_box.pos, size=msg_box.size, radius=[15, 15, 15, 2])

        avatar = Image(source='assets/icons/bot_avatar.png', size_hint_x=0.12)
        msg_box.add_widget(avatar)

        label = Label(text=text, font_size='15sp', color=COLORS['light'],
                      halign='left', valign='center')
        label.bind(size=label.setter('text_size'))
        msg_box.add_widget(label)
        self.chat_layout.add_widget(msg_box)
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        Clock.schedule_once(lambda dt: setattr(self.chat_layout.parent, 'scroll_y', 0), 0.1)

    def _on_mic_press(self, instance):
        if self.is_listening:
            self._stop_listening()
        else:
            self._start_listening()

    def _start_listening(self):
        self.is_listening = True
        self.status_text = "Listening..."
        self.status_indicator.color = COLORS['warning']
        self.mic_pulse.start(self.mic_btn)
        if self.wake_sound:
            self.wake_sound.play()
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _stop_listening(self):
        self.is_listening = False
        self.status_text = "Jarvis ready..."
        self.status_indicator.color = COLORS['success']
        self.mic_pulse.stop(self.mic_btn)
        self.mic_btn.background_color = COLORS['primary']

    def _listen_thread(self):
        try:
            result = self.stt.listen_bengali() if self.stt else None
            if result:
                Clock.schedule_once(lambda dt: self._process_voice_result(result), 0)
            else:
                Clock.schedule_once(lambda dt: self._on_listen_error(), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt, err=str(e): self._on_listen_error(err), 0)

    def _process_voice_result(self, text):
        self._stop_listening()
        self._add_user_message(text)
        self._process_command(text)

    def _on_listen_error(self, error=None):
        self._stop_listening()
        msg = "Could not hear, please say again" if not error else f"Error: {error}"
        self.speak(msg)

    def speak(self, text, emotion='neutral'):
        self.is_speaking = True
        self.status_text = "Speaking..."
        self.status_indicator.color = COLORS['secondary']
        self._add_bot_message(text)

        def _speak_thread():
            try:
                if self.tts:
                    self.tts.speak(text, emotion=emotion)
            finally:
                Clock.schedule_once(lambda dt: self._on_speak_done(), 0)

        threading.Thread(target=_speak_thread, daemon=True).start()

    def _on_speak_done(self):
        self.is_speaking = False
        self.status_text = "Jarvis ready..."
        self.status_indicator.color = COLORS['success']
        if self.is_auto_mode and not self.is_listening:
            Clock.schedule_once(lambda dt: self._start_listening(), 1.5)

    def _on_text_submit(self, instance):
        text = instance.text.strip()
        if text:
            self._add_user_message(text)
            self._process_command(text)
            instance.text = ''

    def _on_send_press(self, instance):
        self._on_text_submit(self.text_input)

    def _process_command(self, command):
        cmd_lower = command.lower()
        if self.is_auto_mode and not any(w in cmd_lower for w in WAKE_WORDS):
            return

        response = self.brain.process(command, self.conversation_history)
        self.conversation_history.append({'role': 'user', 'text': command})
        self.conversation_history.append({'role': 'bot', 'text': response['text']})

        self.speak(response['text'], emotion=response.get('emotion', 'neutral'))

        if response.get('action'):
            self._execute_action(response['action'])

    def _execute_action(self, action):
        if platform != 'android':
            return

        action_type = action.get('type')

        if action_type == 'call':
            intent = Intent(Intent.ACTION_CALL)
            intent.setData(Uri.parse(f"tel:{action['number']}"))
            PythonActivity.mActivity.startActivity(intent)

        elif action_type == 'whatsapp':
            number = action.get('number', '')
            wa_number = number if number.startswith('88') else f"88{number}"
            intent = Intent(Intent.ACTION_VIEW)
            intent.setData(Uri.parse(f"https://wa.me/{wa_number}"))
            PythonActivity.mActivity.startActivity(intent)

        elif action_type in ('check_orders', 'confirm_order', 'generate_report'):
            url = action.get('url') or self.business.get('website', '')
            if url:
                intent = Intent(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(url))
                PythonActivity.mActivity.startActivity(intent)

    def _quick_order(self, instance): self._process_command("Jarvis check orders")
    def _quick_call(self, instance): self.text_input.text = "Jarvis call "; self.text_input.focus = True
    def _quick_whatsapp(self, instance): self.text_input.text = "Jarvis whatsapp "; self.text_input.focus = True
    def _quick_product(self, instance): self._process_command("Jarvis show products")
    def _quick_report(self, instance): self._process_command("Jarvis today report")
    def _quick_customer(self, instance): self._process_command("Jarvis customer list")
    def _quick_reminder(self, instance): self.text_input.text = "Jarvis set reminder "; self.text_input.focus = True
    def _quick_all_orders(self, instance): self._process_command("Jarvis all orders")

    def _toggle_auto_mode(self, instance):
        self.is_auto_mode = not self.is_auto_mode
        if self.is_auto_mode:
            instance.background_color = COLORS['success']
            instance.text = 'AUTO'
            self.speak("Auto mode on. Say Jarvis to call.")
        else:
            instance.background_color = COLORS['warning']
            instance.text = 'MANUAL'
            self.speak("Manual mode. Tap MIC to speak.")

    def _show_settings(self, instance):
        pass

    def _delayed_init(self, dt):
        Clock.schedule_once(lambda dt: self.speak(
            f"Hello {self.business['owner']}! Jarvis ready. Say 'Jarvis' to call.",
            emotion='happy'
        ), 0.5)


class JarvisCosmeticsApp(App):
    def build(self):
        Window.clearcolor = COLORS['dark']
        return JarvisMainUI()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    JarvisCosmeticsApp().run()
