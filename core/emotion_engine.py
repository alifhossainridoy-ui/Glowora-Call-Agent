#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emotion Engine
Detect emotion from text and control voice emotion
"""

from typing import Dict


class EmotionEngine:
    """
    Emotion Detection and Control

    Detects emotion from user commands and sets
    appropriate response emotion for TTS
    """

    def __init__(self):
        self.emotion_patterns = {
            'happy': {
                'keywords': ['happy', 'great', 'awesome', 'excellent', 'thank',
                             'thanks', 'good', 'wonderful', 'perfect', 'love',
                             'valo', 'bhalo', 'dhonnobad', 'shukria', 'khusi'],
                'response_emotion': 'happy'
            },
            'urgent': {
                'keywords': ['urgent', 'emergency', 'now', 'quick', 'hurry',
                             'joldi', 'tara', 'attonko', 'joruri'],
                'response_emotion': 'urgent'
            },
            'frustrated': {
                'keywords': ['bad', 'terrible', 'worst', 'problem', 'issue',
                             'error', 'not working', 'kharap', 'somossa'],
                'response_emotion': 'sympathetic'
            },
            'question': {
                'keywords': ['what', 'how', 'why', 'when', 'where', 'which',
                             'ki', 'kemon', 'kobe', 'kothay'],
                'response_emotion': 'calm'
            },
            'order': {
                'keywords': ['order', 'buy', 'purchase', 'confirm', 'delivery',
                             'ordar', 'kena', 'confirm koro'],
                'response_emotion': 'professional'
            }
        }

    def detect(self, command: str, response_text: str = '') -> str:
        """Detect emotion from command"""
        command = command.lower()

        scores = {}
        for emotion, data in self.emotion_patterns.items():
            score = sum(1 for kw in data['keywords'] if kw in command)
            if score > 0:
                scores[emotion] = score

        if scores:
            best_emotion = max(scores, key=scores.get)
            return self.emotion_patterns[best_emotion]['response_emotion']

        return 'neutral'

    def get_voice_params(self, emotion: str) -> Dict:
        """Get voice parameters for emotion"""
        params = {
            'neutral': {'pitch': 1.0, 'speed': 1.0, 'volume': 0.9},
            'happy': {'pitch': 1.15, 'speed': 1.1, 'volume': 0.95},
            'calm': {'pitch': 0.9, 'speed': 0.85, 'volume': 0.8},
            'professional': {'pitch': 1.0, 'speed': 0.95, 'volume': 0.9},
            'urgent': {'pitch': 1.2, 'speed': 1.3, 'volume': 1.0},
            'sympathetic': {'pitch': 0.85, 'speed': 0.8, 'volume': 0.85}
        }
        return params.get(emotion, params['neutral'])
