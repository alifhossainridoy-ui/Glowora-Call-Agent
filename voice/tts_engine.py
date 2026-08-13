#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Realistic TTS Engine - Bengali Voice Engine
3-Engine Hybrid System for Natural Bengali Speech
"""

import re
import hashlib
import time
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class VoiceProfile:
    name: str
    pitch: float
    speed: float
    volume: float
    emotion_map: Dict[str, tuple]


class RealisticTTSEngine:
    """
    Realistic Bengali TTS Engine

    Features:
    - Multi-engine fallback (gTTS -> Coqui -> Piper)
    - Emotion-aware speech
    - Voice caching
    - Natural pauses
    """

    def __init__(self, cache_dir: str = 'data/voice_cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.engines = {
            'gtts': {'available': True, 'priority': 1},
            'coqui': {'available': False, 'priority': 2},
            'piper': {'available': False, 'priority': 3}
        }

        self.profiles = {
            'default': VoiceProfile(
                name='Jarvis',
                pitch=1.0,
                speed=1.0,
                volume=0.9,
                emotion_map={
                    'neutral': (1.0, 1.0),
                    'happy': (1.15, 1.1),
                    'calm': (0.9, 0.85),
                    'professional': (1.0, 0.95),
                    'urgent': (1.2, 1.3),
                    'sympathetic': (0.85, 0.8)
                }
            )
        }

        self.current_profile = self.profiles['default']
        self.coqui_tts = None
        self.piper_tts = None
        self._init_engines()

    def _init_engines(self):
        """Initialize optional TTS engines if installed"""
        try:
            from TTS.api import TTS
            self.coqui_tts = TTS("tts_models/multilingual/multi-dataset/your_tts")
            self.engines['coqui']['available'] = True
        except Exception:
            self.coqui_tts = None

        try:
            import piper
            self.piper_tts = piper
            self.engines['piper']['available'] = True
        except Exception:
            self.piper_tts = None

    def speak(self, text: str, emotion: str = 'neutral', lang: str = 'bn'):
        """Speak text with emotion"""
        processed_text = self._preprocess_bengali(text)

        pitch_mod, speed_mod = self.current_profile.emotion_map.get(emotion, (1.0, 1.0))
        pitch = self.current_profile.pitch * pitch_mod
        speed = self.current_profile.speed * speed_mod
        volume = self.current_profile.volume

        audio_file = self._get_cached_audio(processed_text, emotion)
        if audio_file and audio_file.exists():
            self._play_audio(audio_file, volume)
            return

        for engine_name in sorted(self.engines.keys(), key=lambda x: self.engines[x]['priority']):
            if self.engines[engine_name]['available']:
                audio_file = self._generate_with_engine(engine_name, processed_text, pitch, speed, lang)
                if audio_file:
                    self._cache_audio(processed_text, emotion, audio_file)
                    self._play_audio(audio_file, volume)
                    return

        self._fallback_gtts(processed_text, emotion)

    def _preprocess_bengali(self, text: str) -> str:
        """Preprocess Bengali text for better TTS"""
        text = re.sub(r'([।!?,])', r'\1 ', text)
        text = text.replace('  ', ' ').replace('\n', '। ')
        text = re.sub(r'(\d+)', r' \1 ', text)
        return text.strip()

    def _get_cached_audio(self, text: str, emotion: str) -> Optional[Path]:
        cache_key = hashlib.md5(f"{text}_{emotion}".encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.mp3"
        return cache_file if cache_file.exists() else None

    def _cache_audio(self, text: str, emotion: str, audio_file: Path):
        cache_key = hashlib.md5(f"{text}_{emotion}".encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.mp3"
        if audio_file != cache_file:
            import shutil
            shutil.copy(audio_file, cache_file)

    def _generate_with_engine(self, engine: str, text: str, pitch: float, speed: float, lang: str) -> Optional[Path]:
        if engine == 'gtts':
            return self._generate_gtts(text, lang)
        elif engine == 'coqui' and self.coqui_tts:
            return self._generate_coqui(text, pitch, speed)
        elif engine == 'piper' and self.piper_tts:
            return self._generate_piper(text, pitch, speed)
        return None

    def _generate_gtts(self, text: str, lang: str) -> Path:
        from gtts import gTTS

        output_file = self.cache_dir / f"temp_gtts_{hashlib.md5(text.encode()).hexdigest()[:8]}.mp3"
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(str(output_file))
        return output_file

    def _generate_coqui(self, text: str, pitch: float, speed: float) -> Optional[Path]:
        if not self.coqui_tts:
            return None

        output_file = self.cache_dir / f"temp_coqui_{hashlib.md5(text.encode()).hexdigest()[:8]}.wav"
        try:
            self.coqui_tts.tts_to_file(
                text=text, file_path=str(output_file), speaker_wav=None, language="bn"
            )
            return output_file
        except Exception:
            return None

    def _generate_piper(self, text: str, pitch: float, speed: float) -> Optional[Path]:
        if not self.piper_tts:
            return None

        output_file = self.cache_dir / f"temp_piper_{hashlib.md5(text.encode()).hexdigest()[:8]}.wav"
        try:
            import subprocess
            subprocess.run(
                ['piper', '--model', 'bn_BN_model.onnx',
                 '--output_file', str(output_file), '--text', text],
                check=True
            )
            return output_file
        except Exception:
            return None

    def _fallback_gtts(self, text: str, emotion: str):
        """Fallback to gTTS with emotion simulation"""
        from gtts import gTTS
        from pydub import AudioSegment

        output_file = self.cache_dir / f"fallback_{hashlib.md5(text.encode()).hexdigest()[:8]}.mp3"

        tts = gTTS(text=text, lang='bn', slow=False)
        tts.save(str(output_file))

        try:
            audio = AudioSegment.from_mp3(str(output_file))

            if emotion == 'happy':
                audio = audio.speedup(playback_speed=1.1) + 3
            elif emotion == 'calm':
                audio = audio.speedup(playback_speed=0.9)
            elif emotion == 'urgent':
                audio = audio.speedup(playback_speed=1.2)

            audio.export(str(output_file), format="mp3")
        except Exception:
            pass

        self._play_audio(output_file, 0.9)

    def _play_audio(self, audio_file: Path, volume: float):
        """Play audio file"""
        from kivy.core.audio import SoundLoader

        sound = SoundLoader.load(str(audio_file))
        if sound:
            sound.volume = volume
            sound.play()
            while sound.state == 'play':
                time.sleep(0.1)

    def preload_voices(self):
        """Preload common phrases into cache"""
        common_phrases = ["Hello", "How can I help you", "Order confirmed", "Calling now", "Thank you"]
        for phrase in common_phrases:
            self._generate_gtts(phrase, 'bn')

    def set_voice_profile(self, profile_name: str):
        if profile_name in self.profiles:
            self.current_profile = self.profiles[profile_name]
