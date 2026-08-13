#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TinyLlama Offline LLM Manager
Runs AI locally without internet, as a fallback when JarvisBrain's intent
matching has low confidence.
"""

from pathlib import Path
from typing import Optional, Dict, List


class TinyLlamaManager:
    """
    TinyLlama 1.1B Parameter Model Manager

    Features:
    - Run completely offline
    - Bengali-aware text generation
    - Customer response generation
    """

    def __init__(self, model_path: str = 'data/models/tinyllama'):
        self.model_path = Path(model_path)
        self.model = None
        self.tokenizer = None
        self.initialized = False

        self._init_model()

    def _init_model(self):
        """Initialize TinyLlama model, if transformers + weights are available"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer

            model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

            self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=str(self.model_path))
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, cache_dir=str(self.model_path), torch_dtype="auto", device_map="auto"
            )

            self.initialized = True
            print("TinyLlama model loaded successfully")

        except Exception as e:
            print(f"TinyLlama init failed: {e}")
            self.initialized = False

    def generate(self, prompt: str, history: Optional[List[Dict]] = None,
                 max_length: int = 200, temperature: float = 0.7) -> Optional[str]:
        """Generate text using TinyLlama"""
        if not self.initialized:
            return None

        try:
            formatted_prompt = self._format_prompt(prompt, history)
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt")

            outputs = self.model.generate(
                **inputs, max_length=max_length, temperature=temperature,
                do_sample=True, top_p=0.9
            )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response[len(formatted_prompt):].strip()

        except Exception as e:
            print(f"Generation error: {e}")
            return None

    def _format_prompt(self, prompt: str, history: Optional[List[Dict]] = None) -> str:
        """Format prompt with conversation history"""
        system_msg = (
            "You are Jarvis, a helpful cosmetics business assistant. "
            "You help with product recommendations, order management, and customer service. "
            "Respond in Bengali when the user speaks Bengali."
        )

        formatted = f"<|system|>\n{system_msg}\n"

        if history:
            for msg in history[-5:]:
                role = msg.get('role', 'user')
                text = msg.get('text', '')
                formatted += f"<|{role}|>\n{text}\n"

        formatted += f"<|user|>\n{prompt}\n<|assistant|>\n"
        return formatted

    def generate_product_description(self, product_name: str, ingredients: List[str]) -> Optional[str]:
        """Generate product description"""
        prompt = f"Write a short product description for {product_name}.\nIngredients: {', '.join(ingredients)}\nDescription:"
        return self.generate(prompt, max_length=150)

    def generate_customer_reply(self, query: str, context: str = '') -> Optional[str]:
        """Generate customer service reply"""
        prompt = f"Customer query: {query}\nContext: {context}\nProfessional reply:"
        return self.generate(prompt, max_length=200)

    def download_model(self):
        """Download TinyLlama model weights"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer

            model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

            print("Downloading TinyLlama model...")
            AutoTokenizer.from_pretrained(model_name, cache_dir=str(self.model_path))
            AutoModelForCausalLM.from_pretrained(model_name, cache_dir=str(self.model_path))

            print("Model downloaded successfully")
            self._init_model()

        except Exception as e:
            print(f"Download failed: {e}")
