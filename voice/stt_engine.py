#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Engine STT - Speech to Text
Vosk (Offline) + Google (Online) + Whisper (High Quality)
"""

import json
import os
import tempfile
import wave
from pathlib import Path
from typing import Optional
import speech_recognition as sr


class MultiEngineSTT:
    """
    Multi-engine Bengali Speech to Text

    Priority:
    1. Vosk (Offline, Fast)
    2. Google Speech (Online, Accurate)
    3. Whisper (High Quality, Slow)
    """

    def __init__(self, model_path: str = 'data/vosk_model'):
        self.recognizer = sr.Recognizer()
        self.vosk_model = None
        self.whisper_model = None

        self.engines = {
            'vosk': {'available': False, 'priority': 1},
            'google': {'available': True, 'priority': 2},
            'whisper': {'available': False, 'priority': 3}
        }

        self._init_vosk(model_path)
        self._init_whisper()

    def _init_vosk(self, model_path: str):
        try:
            from vosk import Model

            model_dir = Path(model_path)
            if model_dir.exists():
                self.vosk_model = Model(str(model_dir))
                self.engines['vosk']['available'] = True
        except Exception as e:
            print(f"Vosk init failed: {e}")

    def _init_whisper(self):
        try:
            import whisper
            self.whisper_model = whisper.load_model("base")
            self.engines['whisper']['available'] = True
        except Exception as e:
            print(f"Whisper init failed: {e}")

    def listen_bengali(self, timeout: int = 7, phrase_time_limit: int = 5) -> Optional[str]:
        """Listen and convert Bengali speech to text"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                return self._recognize_with_fallback(audio)
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except Exception as e:
            print(f"STT Error: {e}")
            return None

    def _recognize_with_fallback(self, audio: sr.AudioData) -> Optional[str]:
        if self.engines['vosk']['available']:
            result = self._recognize_vosk(audio)
            if result:
                return result

        if self.engines['google']['available']:
            result = self._recognize_google(audio)
            if result:
                return result

        if self.engines['whisper']['available']:
            result = self._recognize_whisper(audio)
            if result:
                return result

        return None

    def _recognize_vosk(self, audio: sr.AudioData) -> Optional[str]:
        if not self.vosk_model:
            return None

        try:
            from vosk import KaldiRecognizer

            recognizer = KaldiRecognizer(self.vosk_model, audio.sample_rate)
            data = audio.get_raw_data(convert_rate=16000, convert_width=2)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get('text', '').strip()
                if text:
                    return text

            result = json.loads(recognizer.FinalResult())
            text = result.get('text', '').strip()
            return text if text else None
        except Exception as e:
            print(f"Vosk error: {e}")
            return None

    def _recognize_google(self, audio: sr.AudioData) -> Optional[str]:
        try:
            text = self.recognizer.recognize_google(audio, language='bn-BD')
            return text.strip() if text else None
        except sr.UnknownValueError:
            print("Google could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Google API error: {e}")
            return None

    def _recognize_whisper(self, audio: sr.AudioData) -> Optional[str]:
        if not self.whisper_model:
            return None

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_path = f.name

            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(audio.sample_rate)
                wf.writeframes(audio.get_raw_data())

            result = self.whisper_model.transcribe(temp_path, language='bn')
            text = result.get('text', '').strip()
            return text if text else None
        except Exception as e:
            print(f"Whisper error: {e}")
            return None
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

    def calibrate_microphone(self, duration: int = 2):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=duration)

    def download_vosk_model(self, model_url: Optional[str] = None):
        """Download Vosk Bengali model"""
        import urllib.request
        import zipfile

        model_dir = Path('data/vosk_model')
        model_dir.mkdir(parents=True, exist_ok=True)

        if not model_url:
            model_url = "https://alphacephei.com/vosk/models/vosk-model-small-bn-0.22.zip"

        zip_path = model_dir / 'model.zip'

        urllib.request.urlretrieve(model_url, zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(model_dir)

        zip_path.unlink()
