#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Brain - Core AI Engine
Intent Recognition, Context Management, Response Generation
"""

import re
import random
from typing import Dict, List, Optional, Tuple


class JarvisBrain:
    """
    Main intelligence engine for Jarvis Cosmetics AI

    Features:
    - Hybrid Intent Recognition (Regex + Keyword matching)
    - Context-aware responses
    - Product knowledge integration
    - Multi-turn conversation support
    """

    def __init__(self, business_config: Dict):
        self.business = business_config
        self.context = ConversationContext()
        self.intents = self._load_intents()
        self.templates = self._load_templates()
        self.product_brain = None

        # AI model placeholders (optional, wired in from ai_models/)
        self.local_ai = None
        self.online_ai = None

    def _load_intents(self) -> Dict:
        """Load intent recognition patterns"""
        return {
            'check_orders': {
                'patterns': [
                    r'order', r'orders', r'check order', r'new order',
                    r'order check', r'how many orders', r'today order',
                    r'order dekhao', r'notun order'
                ],
                'priority': 10,
            },
            'confirm_order': {
                'patterns': [
                    r'confirm order', r'accept order', r'order confirm',
                    r'order nao', r'order grohon'
                ],
                'priority': 10
            },
            'cancel_order': {
                'patterns': [
                    r'cancel order', r'order cancel', r'bad dao',
                    r'order batil'
                ],
                'priority': 9
            },
            'make_call': {
                'patterns': [
                    r'call', r'phone', r'dial', r'call koro',
                    r'phone koro', r'jogajog'
                ],
                'priority': 10,
                'extract_number': True
            },
            'whatsapp_message': {
                'patterns': [
                    r'whatsapp', r'whats app', r'wa message',
                    r'whatsapp koro', r'message pathao'
                ],
                'priority': 10,
                'extract_number': True
            },
            'product_info': {
                'patterns': [
                    r'product', r'cream', r'serum', r'lotion',
                    r'product info', r'cream dam', r'product dam',
                    r'ki ache', r'ki pabo', r'dam koto'
                ],
                'priority': 9
            },
            'product_recommendation': {
                'patterns': [
                    r'recommend', r'suggest', r'konta valo',
                    r'konta nebo', r'skin er jonno', r'face er jonno'
                ],
                'priority': 9
            },
            'skin_analysis': {
                'patterns': [
                    r'skin', r'face', r'twak', r'mukh',
                    r'skin type', r'twaker dhoron', r'toillakto',
                    r'sushko', r'sensitive'
                ],
                'priority': 8
            },
            'ingredient_query': {
                'patterns': [
                    r'ingredient', r'upadan', r'chemical', r'natural',
                    r'ki diye toiri'
                ],
                'priority': 8
            },
            'daily_report': {
                'patterns': [
                    r'report', r'bikri', r'income', r'revenue',
                    r'ajker bikri', r'koto taka', r'koto order'
                ],
                'priority': 8
            },
            'inventory_check': {
                'patterns': [
                    r'stock', r'inventory', r'koto ache', r'shes',
                    r'furiye geche', r'ar koto ache'
                ],
                'priority': 8
            },
            'set_reminder': {
                'patterns': [
                    r'reminder', r'mone koriye', r'follow up', r'mone rakho'
                ],
                'priority': 7
            },
            'help': {
                'patterns': [
                    r'help', r'ki korte paro', r'sahajjo',
                    r'ki ki paro', r'command'
                ],
                'priority': 5
            },
            'greeting': {
                'patterns': [
                    r'hello', r'hi', r'assalamu', r'salam',
                    r'kemon acho', r'ki khobor'
                ],
                'priority': 5
            },
            'goodbye': {
                'patterns': [
                    r'bye', r'goodbye', r'allah hafez', r'biday',
                    r'bondho koro', r'thamo'
                ],
                'priority': 5
            }
        }

    def _load_templates(self) -> Dict:
        """Load response templates"""
        return {
            'greeting': [
                "Hello {owner}! How are you? How can I help today?",
                "Assalamu Alaikum {owner}! Jarvis ready. What should I do?",
                "Hello! What can I do for {business_name}?"
            ],
            'check_orders': [
                "Checking orders now {owner}...",
                "Opening website to check new orders...",
                "One moment, checking order status..."
            ],
            'confirm_order': [
                "Confirming order...",
                "Order accepted. Notifying customer...",
                "Order confirmed! Should I call the customer?"
            ],
            'help': [
                """I can help you with:

Order Management
  'Check orders' / 'Show new orders'

Customer Calls
  'Call 01712345678'

WhatsApp Messages
  'WhatsApp 01712345678'

Product Information
  'Facial cream price' / 'What is good for oily skin'

Reports
  'Show today report'

Say 'Jarvis' to call me!"""
            ]
        }

    def process(self, command: str, history: List[Dict]) -> Dict:
        """
        Main processing function

        Args:
            command: User command text
            history: Conversation history

        Returns:
            Dict with text, action, emotion, data
        """
        command = command.strip().lower()
        self.context.add_message('user', command)

        intent, confidence, entities = self._recognize_intent(command)
        context_data = self.context.get_relevant_context(intent)

        if confidence > 0.7:
            response = self._handle_high_confidence(intent, entities, context_data)
        elif confidence > 0.4:
            response = self._handle_medium_confidence(intent, entities, command)
        else:
            response = self._handle_low_confidence(command, history)

        self.context.add_message('bot', response['text'])
        return response

    def _recognize_intent(self, command: str) -> Tuple[str, float, Dict]:
        """Intent recognition with confidence scoring"""
        best_intent = 'unknown'
        best_confidence = 0.0
        entities = {}

        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data['patterns']:
                confidence = 0.0
                if pattern in command:
                    confidence = 1.0
                elif any(word and word in command for word in pattern.split()):
                    confidence = 0.8
                else:
                    try:
                        if re.search(pattern, command):
                            confidence = 0.9
                    except re.error:
                        continue

                if confidence == 0.0:
                    continue

                priority = intent_data.get('priority', 5)
                confidence *= (1 + priority / 20)

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_intent = intent_name

                    if intent_data.get('extract_number'):
                        numbers = re.findall(r'01[3-9]\d{8}', command)
                        if numbers:
                            entities['phone'] = numbers[0]

        best_confidence = min(best_confidence, 1.0)
        return best_intent, best_confidence, entities

    def _handle_high_confidence(self, intent: str, entities: Dict, context: Dict) -> Dict:
        """Handle high confidence intents"""

        if intent == 'greeting':
            return {
                'text': random.choice(self.templates['greeting']).format(
                    owner=self.business.get('owner', 'Sir'),
                    business_name=self.business.get('name', '')
                ),
                'emotion': 'happy'
            }

        elif intent == 'check_orders':
            return {
                'text': random.choice(self.templates['check_orders']).format(
                    owner=self.business.get('owner', 'Sir')
                ),
                'action': {'type': 'check_orders', 'url': self.business.get('website', '')},
                'emotion': 'professional'
            }

        elif intent == 'confirm_order':
            return {
                'text': random.choice(self.templates['confirm_order']),
                'action': {'type': 'confirm_order'},
                'emotion': 'happy'
            }

        elif intent == 'cancel_order':
            return {
                'text': "Which order should I cancel? Please give the order ID.",
                'emotion': 'calm'
            }

        elif intent == 'make_call':
            phone = entities.get('phone', '')
            if phone:
                return {
                    'text': f"Calling {phone}...",
                    'action': {'type': 'call', 'number': phone},
                    'emotion': 'professional'
                }
            return {'text': "Which number should I call? Please say the number.", 'emotion': 'calm'}

        elif intent == 'whatsapp_message':
            phone = entities.get('phone', '')
            if phone:
                return {
                    'text': f"Opening WhatsApp for {phone}...",
                    'action': {'type': 'whatsapp', 'number': phone},
                    'emotion': 'professional'
                }
            return {'text': "Which number for WhatsApp?", 'emotion': 'calm'}

        elif intent == 'product_info':
            return self._handle_product_query(context.get('last_product'))

        elif intent == 'product_recommendation':
            return self._handle_product_recommendation('')

        elif intent == 'skin_analysis':
            return self._handle_skin_analysis('')

        elif intent == 'ingredient_query':
            return {'text': "Which ingredient do you want to know about?", 'emotion': 'calm'}

        elif intent == 'inventory_check':
            return self._handle_inventory_check()

        elif intent == 'set_reminder':
            return {'text': "What should I remind you about, and when?", 'emotion': 'calm'}

        elif intent == 'daily_report':
            return {
                'text': "Generating today's report...",
                'action': {'type': 'generate_report'},
                'emotion': 'professional'
            }

        elif intent == 'help':
            return {'text': self.templates['help'][0], 'emotion': 'happy'}

        elif intent == 'goodbye':
            return {
                'text': f"Allah Hafez {self.business.get('owner', 'Sir')}! Call me anytime.",
                'emotion': 'happy'
            }

        else:
            return {
                'text': "Sorry, I didn't understand. Please say again.",
                'emotion': 'calm'
            }

    def _handle_medium_confidence(self, intent: str, entities: Dict, command: str) -> Dict:
        """Medium confidence - fall back to AI if wired, else clarify"""
        if self.online_ai:
            reply = self.online_ai.generate(command, self.context.get_history())
            if reply:
                return {'text': reply, 'emotion': 'calm'}
        if self.local_ai:
            reply = self.local_ai.generate(command, self.context.get_history())
            if reply:
                return {'text': reply, 'emotion': 'calm'}
        return {
            'text': "I'm not sure about that. Can you say it differently?",
            'emotion': 'calm'
        }

    def _handle_low_confidence(self, command: str, history: List[Dict]) -> Dict:
        """Low confidence - AI fallback"""
        if self.online_ai:
            reply = self.online_ai.generate(command, history)
            if reply:
                return {'text': reply, 'emotion': 'calm'}
        return {
            'text': "Sorry, I didn't understand. Say 'help' to see what I can do.",
            'emotion': 'calm'
        }

    def _handle_product_query(self, product_name: Optional[str]) -> Dict:
        """Handle product queries"""
        if not self.product_brain or not product_name:
            return {
                'text': "Which product do you want to know about? Say the name.",
                'emotion': 'calm'
            }

        product = self.product_brain.get_product(product_name)
        if product:
            return {
                'text': self._format_product_info(product),
                'emotion': 'happy',
                'data': {'product': product}
            }
        return {
            'text': f"{product_name} not found. Should I search with another name?",
            'emotion': 'calm'
        }

    def _handle_product_recommendation(self, command: str) -> Dict:
        """Product recommendation"""
        if not self.product_brain:
            return {'text': "Product database loading... Please try later.", 'emotion': 'calm'}

        skin_type = self._extract_skin_type(command)
        concern = self._extract_concern(command)
        recommendations = self.product_brain.recommend(skin_type, concern)

        if recommendations:
            text = "Recommendations for you:\n\n"
            for i, prod in enumerate(recommendations[:3], 1):
                text += f"{i}. {prod.name} - TK{prod.price}\n"
                text += f"   {prod.description[:60]}\n\n"
            text += "Which one do you want details for?"
            return {'text': text, 'emotion': 'happy', 'data': {'recommendations': recommendations}}

        return {'text': "Sorry, can't suggest anything now. Try different words?", 'emotion': 'calm'}

    def _handle_skin_analysis(self, command: str) -> Dict:
        """Skin analysis"""
        skin_type = self._extract_skin_type(command)
        if skin_type:
            analysis = self._get_skin_analysis(skin_type)
            return {'text': analysis, 'emotion': 'professional'}
        return {'text': "What is your skin type? Oily, dry, combination, or sensitive?", 'emotion': 'calm'}

    def _handle_inventory_check(self) -> Dict:
        """Low-stock inventory check"""
        if not self.product_brain:
            return {'text': "Product database loading... Please try later.", 'emotion': 'calm'}

        low_stock = self.product_brain.get_low_stock()
        if not low_stock:
            return {'text': "All products are well stocked.", 'emotion': 'happy'}

        text = "Low stock items:\n\n"
        for p in low_stock[:5]:
            text += f"- {p.name}: {p.stock} pcs left\n"
        return {'text': text, 'emotion': 'professional'}

    def _extract_skin_type(self, command: str) -> Optional[str]:
        """Extract skin type from command"""
        types = {
            'oily': ['oily', 'toillakto', 'chokchok', 'tel'],
            'dry': ['dry', 'sushko', 'phata', 'rukhsho'],
            'combination': ['combination', 'mishro', 'mazhari'],
            'sensitive': ['sensitive', 'allergy', 'chulkay']
        }
        for skin_type, keywords in types.items():
            if any(kw in command for kw in keywords):
                return skin_type
        return None

    def _extract_concern(self, command: str) -> Optional[str]:
        """Extract skin concern"""
        concerns = {
            'acne': ['acne', 'brone', 'pimple'],
            'dark_spot': ['dark spot', 'kalo', 'pigmentation'],
            'wrinkle': ['wrinkle', 'ringkle', 'boyosher chap'],
            'dark_circle': ['dark circle', 'chokher niche'],
            'oily': ['oil', 'tel', 'chokchok']
        }
        for concern, keywords in concerns.items():
            if any(kw in command for kw in keywords):
                return concern
        return None

    def _format_product_info(self, product) -> str:
        """Format product information"""
        text = f"Product: {product.name}\n\n"
        text += f"Price: TK{product.price}\n"
        text += f"Stock: {product.stock} pcs\n\n"
        text += f"Description:\n{product.description}\n\n"

        if product.ingredients:
            text += f"Ingredients:\n{', '.join(product.ingredients)}\n\n"
        if product.usage:
            text += f"Usage:\n{product.usage}\n\n"
        if product.skin_types:
            text += f"Suitable for: {', '.join(product.skin_types)}\n"
        return text

    def _get_skin_analysis(self, skin_type: str) -> str:
        """Get skin analysis results"""
        analyses = {
            'oily': """Oily Skin Care:

Morning: Oil-free cleanser -> Toner -> Lightweight moisturizer -> Gel sunscreen
Night: Double cleanse -> Niacinamide serum -> Oil-free night cream

Tips:
- Wash face 2-3 times daily
- Use oil-free products
- Clay mask once a week

Want to see recommended products?""",

            'dry': """Dry Skin Care:

Morning: Cream cleanser -> Hydrating toner -> Rich moisturizer -> SPF 50
Night: Oil cleanser -> Hyaluronic acid -> Thick night cream

Tips:
- Don't wash with hot water
- Use humidifier
- Exfoliate twice a week

Want to see recommended products?""",

            'combination': """Combination Skin Care:

Morning: Gentle cleanser -> Balancing toner -> Zone-specific moisturizer
Night: Deep cleanse -> Serum (T-zone: Niacinamide, Cheeks: Hyaluronic)

Tips:
- Different care for T-zone and cheeks
- Try multi-masking

Want to see recommended products?""",

            'sensitive': """Sensitive Skin Care:

Morning: Micellar water -> Soothing toner -> Fragrance-free moisturizer -> Mineral SPF
Night: Gentle cleanse -> Centella serum -> Barrier repair cream

Tips:
- Choose fragrance-free products
- Patch test new products
- Use one product for 2 weeks

Want to see recommended products?"""
        }
        return analyses.get(skin_type, "Sorry, no information for this skin type.")


class ConversationContext:
    """Conversation context manager"""

    def __init__(self, max_history: int = 10):
        from datetime import datetime
        self._datetime = datetime
        self.history = []
        self.max_history = max_history
        self.current_intent = None
        self.pending_action = None

    def add_message(self, role: str, text: str):
        self.history.append({
            'role': role,
            'text': text,
            'timestamp': self._datetime.now().isoformat()
        })
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self) -> List[Dict]:
        return self.history

    def get_relevant_context(self, intent: str) -> Dict:
        return {
            'last_intent': self.current_intent,
            'last_product': self._extract_last_product(),
            'pending_action': self.pending_action
        }

    def _extract_last_product(self) -> Optional[str]:
        for msg in reversed(self.history):
            if msg['role'] == 'user':
                words = msg['text'].split()
                for word in words:
                    if len(word) > 3:
                        return word
        return None

    def set_pending(self, action: Dict):
        self.pending_action = action

    def clear_pending(self):
        self.pending_action = None
