#!/usr/bin/env python3
"""
🌸 HINATA AI CHATBOT - Friend Style Hinglish
Uses OpenRouter API for AI responses
Advanced Memory System & Auto-Learning
"""

import random
import re
import aiohttp
import json
import os
from typing import Optional, Dict, List

class HinataAI:
    def __init__(self, db_manager=None):
        # OpenRouter API Key (Fixed & Working)
        self.api_key = os.getenv('OPENROUTER_KEY', "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")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.api_available = True
        
        # Database manager for memory system
        self.db = db_manager
        
        # User memory cache
        self.memory_cache = {}
        
        # Learned responses cache
        self.learned_cache = []
        
        # Learned responses cache
        self.learned_cache = []
        
        # Fallback responses in Hinglish (friend style) - REAL GIRL LIKE SHORT RESPONSES
        self.fallback_responses = {
            "greeting": [
                "hey kaisa hai",
                "kya haal",
                "hello",
                "hi there",
                "konnichiwa",
                "sup",
                "yo",
                "kya chal raha",
            ],
            "how_are_you": [
                "mast hu tu bata",
                "bilkul thik hai",
                "sab mast",
                "badhiya",
                "alright alright",
                "all good",
                "tu bata",
            ],
            "who_are_you": [
                "main hinata hu dost",
                "hinata bolte ho mujhe",
                "bot hu main",
                "your friend",
            ],
            "what_can_you_do": [
                "group manage kar sakti hu",
                "spam hatati hu aur chat krti hu",
                "fun games bhi khelte hai",
            ],
            "love": [
                "aww",
                "haan tu sweet hai",
                "bahut cute ho tum",
                "😊",
                "sharam kar",
            ],
            "joke": [
                "hehe ik funny ho gya",
                "lol serious",
                "😂 good one",
                "haan haan suna tha",
            ],
            "sad": [
                "areh kya hua",
                "sab thik ho jayega",
                "main hu na",
                "mat ro bhai",
            ],
            "happy": [
                "woah great",
                "party time",
                "yay",
                "so happy for u",
            ],
            "angry": [
                "chill chill",
                "cool down",
                "relax bhai",
                "sab thik hoga",
            ],
            "bored": [
                "chalo game khelte hai",
                "/truth ya /dare kro",
                "truth or dare wanna play",
                "kuch interesting krte hain",
            ],
            "tired": [
                "go rest bhai",
                "sleep kr aaram kr",
                "health matter krta hai",
                "so ja ab",
            ],
            "thanks": [
                "no problem",
                "anytime yaar",
                "koi baat nahi",
                "welcome",
            ],
            "bye": [
                "bye bye",
                "cya soon",
                "take care",
                "bye dear",
            ],
            "anime": [
                "hinata hyuga best girl",
                "naruto ka will of fire",
                "anime is life",
                "believe it",
            ],
            "flirt": [
                "stop flirting",
                "cute haan",
                "you're smooth",
                "hehe ok ok",
            ],
            "default": [
                "haan",
                "okay",
                "samajh gyi",
                "sahi baat",
                "nice",
                "cool",
                "acha",
                "sure",
                "gotcha",
                "aur kya",
                "batana kya",
            ],
        }
    
    async def get_ai_response(self, message: str) -> Optional[str]:
        """Get response from OpenRouter AI"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://t.me/",
                "X-Title": "Hinata Bot"
            }
            
            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Hinata, a friendly Indian girl who speaks in Hinglish (Roman Hindi + English mix). You chat like a normal friend - casual, warm, and friendly. Use simple words, no special formatting like asterisks or hashtags. Keep responses short and natural like texting a friend. Never use markdown formatting."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.8
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=data, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        if 'choices' in result and len(result['choices']) > 0:
                            ai_response = result['choices'][0]['message']['content']
                            # Clean the response
                            ai_response = self._clean_response(ai_response)
                            return ai_response
                    else:
                        print(f"OpenRouter error: {response.status}")
                        return None
        except Exception as e:
            print(f"AI API error: {e}")
            return None
    
    def _clean_response(self, text: str) -> str:
        """Clean AI response to be friendly"""
        # Remove markdown formatting
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'\*', '', text)
        text = re.sub(r'__', '', text)
        text = re.sub(r'_', '', text)
        text = re.sub(r'`', '', text)
        text = re.sub(r'#', '', text)
        text = re.sub(r'@', '', text)
        text = re.sub(r'&', '', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Make it lowercase friendly style
        text = text.strip()
        
        return text
    
    def get_fallback_response(self, message: str) -> str:
        """Get fallback response when API fails"""
        msg = message.lower().strip()
        msg_clean = re.sub(r'[^\w\s]', '', msg)
        
        # Check keywords
        if any(w in msg_clean for w in ['hello', 'hi', 'hey', 'konnichiwa']):
            return random.choice(self.fallback_responses["greeting"])
        
        if any(w in msg for w in ['how are you', 'kaisa hai', 'kaisi ho', 'kya haal']):
            return random.choice(self.fallback_responses["how_are_you"])
        
        if any(w in msg for w in ['who are you', 'kon ho', 'kaun ho tum']):
            return random.choice(self.fallback_responses["who_are_you"])
        
        if any(w in msg for w in ['what can you do', 'kya kar sakti ho', 'kya kaam hai']):
            return random.choice(self.fallback_responses["what_can_you_do"])
        
        if any(w in msg for w in ['love you', 'i love you', 'pyaar', 'love u']):
            return random.choice(self.fallback_responses["love"])
        
        if any(w in msg for w in ['joke', 'jokes', 'mazak', 'hasao']):
            return random.choice(self.fallback_responses["joke"])
        
        if any(w in msg for w in ['sad', 'dukhi', 'udaas', 'cry', 'rona']):
            return random.choice(self.fallback_responses["sad"])
        
        if any(w in msg for w in ['happy', 'khush', 'maza', 'fun']):
            return random.choice(self.fallback_responses["happy"])
        
        if any(w in msg for w in ['angry', 'gussa', 'naraz']):
            return random.choice(self.fallback_responses["angry"])
        
        if any(w in msg for w in ['bored', 'bore', 'faltu']):
            return random.choice(self.fallback_responses["bored"])
        
        if any(w in msg for w in ['tired', 'thak', 'thaka']):
            return random.choice(self.fallback_responses["tired"])
        
        if any(w in msg for w in ['thank', 'shukriya', 'dhanyawad']):
            return random.choice(self.fallback_responses["thanks"])
        
        if any(w in msg for w in ['bye', 'alvida', 'ja raha']):
            return random.choice(self.fallback_responses["bye"])
        
        if any(w in msg for w in ['naruto', 'anime', 'hinata hyuga', 'manga']):
            return random.choice(self.fallback_responses["anime"])
        
        return random.choice(self.fallback_responses["default"])
    
    async def generate_response(self, message: str, user_id: int = 0, user_name: str = "") -> str:
        """Generate friend-style response with memory integration"""
        if not message:
            return random.choice(self.fallback_responses["greeting"])
        
        # Try learned responses first
        learned = self._check_learned_responses(message)
        if learned:
            if self.db:
                await self._save_conversation(user_id, message, learned)
            return learned
        
        # Try AI API
        ai_response = await self.get_ai_response(message)
        if ai_response:
            if self.db:
                await self._save_conversation(user_id, message, ai_response)
                await self._learn_response(message, ai_response, user_id)
            return ai_response
        
        # Fallback to local responses
        fallback = self.get_fallback_response(message)
        if self.db:
            await self._save_conversation(user_id, message, fallback)
        return fallback
    
    def _check_learned_responses(self, message: str) -> Optional[str]:
        """Check if we have learned responses for this pattern"""
        if not self.db:
            return None
        
        msg_lower = message.lower().strip()
        
        # Get similar responses from database
        try:
            similar = self.db.get_similar_responses(msg_lower, limit=3)
            if similar:
                # Return the most used response
                return similar[0].get('output_text')
        except:
            pass
        
        return None
    
    async def _save_conversation(self, user_id: int, message: str, response: str):
        """Save conversation to memory"""
        if not self.db or user_id == 0:
            return
        
        try:
            # Store in conversation history
            context = self._extract_context(message)
            self.db.add_conversation(user_id, 0, message, response, context)
            
            # Update user profile
            if not self.db.get_user_profile(user_id):
                self.db.save_user_profile(user_id, "", "", "hinglish")
        except Exception as e:
            print(f"Error saving conversation: {e}")
    
    async def _learn_response(self, input_text: str, response: str, user_id: int = 0):
        """Learn from user interactions"""
        if not self.db:
            return
        
        try:
            # Add to dataset
            self.db.add_to_dataset(input_text.lower(), response, "learned")
            
            # Add as learned response with confidence
            self.db.add_learned_response(input_text.lower(), response, user_id)
        except Exception as e:
            print(f"Error learning response: {e}")
    
    def _extract_context(self, message: str) -> str:
        """Extract context from message for memory"""
        context = {
            "length": len(message),
            "has_question": "?" in message,
            "has_exclamation": "!" in message,
            "sentiment": "neutral"
        }
        
        # Simple sentiment detection
        if any(w in message.lower() for w in ["sad", "dukhi", "udaas", "pain", "hurt"]):
            context["sentiment"] = "sad"
        elif any(w in message.lower() for w in ["happy", "khush", "love", "great", "awesome"]):
            context["sentiment"] = "happy"
        elif any(w in message.lower() for w in ["angry", "gussa", "hate", "mad"]):
            context["sentiment"] = "angry"
        
        return json.dumps(context)
