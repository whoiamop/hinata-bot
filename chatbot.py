#!/usr/bin/env python3
"""
🌸 HINATA AI CHATBOT - Friend Style Hinglish
Uses OpenRouter API for AI responses
"""

import random
import re
import aiohttp
from typing import Optional

class HinataAI:
    def __init__(self):
        # OpenRouter API Key
        self.api_key = "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"
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Fallback responses in Hinglish (friend style)
        self.fallback_responses = {
            "greeting": [
                "hey kaisa hai tu",
                "kya haal hai bhai",
                "hello ji kya chal raha",
                "hii kaisi ho",
                "konnichiwa dost",
            ],
            "how_are_you": [
                "main bilkul mast hu tu bata",
                "bas yahi life chal rahi hai",
                "maza aa raha hai baat karke",
                "thik hu bhai tu suna",
            ],
            "who_are_you": [
                "main hinata hu tumhari dost",
                "main ek bot hu jo tumse dosti karne aaya",
                "main hinata group manager hu aur tumhari friend bhi",
            ],
            "what_can_you_do": [
                "main sab kuch kar sakti hu group manage karna spam hatana aur tumse baat karna",
                "mere paas bahut powers hai admin commands anti spam aur mast mast baatein",
            ],
            "love": [
                "aww tu bhi na sharam kar thoda",
                "ye kya bol raha hai pagal",
                "main bhi tumse dosti karti hu",
                "tu sweet hai yaar",
            ],
            "joke": [
                "ek ladka ladki se pucha tumhara naam kya hai ladki boli meri umar hai ladka bola toh main uncle bulau",
                "teacher ne pucha batao pakistan ka capital kya hai student bola india",
                "ek chota bacha bola papa mujhe shaadi karni hai papa ne kaha pehle padhai kar le beta",
            ],
            "sad": [
                "arre kya hua ro mat yaar",
                "sab thik ho jayega tension mat le",
                "main hu na tere saath",
                "koi baat nahi life mein ups downs hote rehte hai",
            ],
            "happy": [
                "wah kya baat hai party de",
                "mujhe bhi khushi hui sunke",
                "bas aise hi khush reh hamesha",
            ],
            "angry": [
                "arre gussa mat kar cool down",
                "kya hua bata mujhe",
                "deep breath le sab thik ho jayega",
            ],
            "bored": [
                "bore ho raha hai chal kuch masti karte hai",
                "koi naya game khelte hai",
                "mere saath baat kar time pass ho jayega",
            ],
            "tired": [
                "thak gaya hai toh rest kar le yaar",
                "so ja thodi der aaram kar",
                "kaam zyada mat kar health ka dhyan rakh",
            ],
            "thanks": [
                "aree koi baat nahi yaar",
                "itna formal mat ho hum dost hai",
                "koi nahi bhai main hu na",
            ],
            "bye": [
                "bye bye yaar milte hai",
                "chal ja raha hai theek hai baad mein baat karte hai",
                "take care dost",
            ],
            "anime": [
                "naruto dekhna mat bhoolna believe it",
                "hinata hyuga meri favourite hai woh kitni strong hai",
                "anime dekhna best stress buster hai",
                "naruto ka will of fire sabse best hai",
            ],
            "default": [
                "hmm bata aur kya chal raha",
                "sahi hai yaar",
                "mujhe bhi bata apne baare mein",
                "kya kar raha hai aajkal",
                "mast hai yaar",
                "samajh gaya main",
                "aur bata kya naya hai",
                "theek hai dost",
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
    
    async def generate_response(self, message: str, user_name: str = "") -> str:
        """Generate friend-style response"""
        if not message:
            return self.get_fallback_response("hello")
        
        # Try AI API first
        ai_response = await self.get_ai_response(message)
        if ai_response:
            return ai_response
        
        # Fallback to local responses
        return self.get_fallback_response(message)
