#!/usr/bin/env python3
"""
KING ASSISTANT - HUMAN-LIKE CHAT + WIKIPEDIA KNOWLEDGE
Responds to greetings AND gives factual answers
"""

import os
import sys
import json
import time
import re
import html
import random
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

class WikipediaAPI:
    """Wikipedia knowledge engine"""
    
    def __init__(self):
        self.cache_file = Path('data/cache.json')
        self.cache = self.load_cache()
        self.headers = {
            'User-Agent': 'KingAssistant/3.0 (Educational Project)'
        }
        
    def load_cache(self):
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        self.cache_file.parent.mkdir(exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def clean_text(self, text):
        """Clean up Wikipedia text"""
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = html.unescape(text)
        return text.strip()
    
    def search_wikipedia(self, query):
        """Search Wikipedia for the query"""
        try:
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query,
                'srlimit': 1,
                'utf8': 1
            }
            
            search_url = f"https://en.wikipedia.org/w/api.php?{urllib.parse.urlencode(search_params)}"
            req = urllib.request.Request(search_url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                search_results = data.get('query', {}).get('search', [])
                
                if search_results:
                    return search_results[0].get('title', '')
            return None
        except:
            return None
    
    def get_page_content(self, title):
        """Get full page content"""
        try:
            content_params = {
                'action': 'query',
                'format': 'json',
                'prop': 'extracts',
                'exintro': False,
                'explaintext': True,
                'titles': title,
                'redirects': 1
            }
            
            content_url = f"https://en.wikipedia.org/w/api.php?{urllib.parse.urlencode(content_params)}"
            req = urllib.request.Request(content_url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=8) as response:
                data = json.loads(response.read().decode('utf-8'))
                pages = data.get('query', {}).get('pages', {})
                
                for page_id, page in pages.items():
                    if page_id != '-1':
                        return page.get('extract', '')
            return None
        except:
            return None
    
    def get_detailed_answer(self, query: str) -> str:
        """Get detailed answer for factual questions"""
        cache_key = query.lower().strip()
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        print(f"\n🔍 Searching Wikipedia for: '{query}'")
        
        title = self.search_wikipedia(query)
        if not title:
            title = self.search_wikipedia(query.title())
        
        if not title:
            return None
        
        content = self.get_page_content(title)
        if not content:
            return None
        
        content = self.clean_text(content)
        paragraphs = content.split('\n\n')
        answer_paragraphs = []
        
        for para in paragraphs[:3]:
            if len(para) > 50:
                answer_paragraphs.append(para)
                if len(answer_paragraphs) >= 2:
                    break
        
        if answer_paragraphs:
            answer = '\n\n'.join(answer_paragraphs)
            self.cache[cache_key] = answer
            self.save_cache()
            return answer
        
        return None

class VoiceManager:
    """Voice manager"""
    
    def __init__(self):
        self.engine = None
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 160)
        except:
            pass
    
    def speak(self, text: str):
        """Speak text"""
        print(f"\n👑: {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
    
    def listen(self) -> str:
        """Listen for command"""
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("\n🎤 Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            return text.lower()
        except:
            return None

class KingAssistant:
    """Main assistant - HUMAN-LIKE + KNOWLEDGE"""
    
    def __init__(self):
        self.name = "King"
        self.wake_word = "king"
        self.running = True
        
        print("\n" + "="*60)
        print(f"       👑 {self.name} ASSISTANT")
        print("     Human-like Chat + Wikipedia Knowledge")
        print("="*60)
        
        print("\n📚 Loading Wikipedia...")
        self.wikipedia = WikipediaAPI()
        
        print("\n🔊 Initializing Voice...")
        self.voice = VoiceManager()
        
        self.user_name = self.load_user_name()
        
        print("\n" + "="*60)
        print(f"👑 Ready! Say '{self.wake_word}' + your question")
        print("💡 I can chat like a human AND give you knowledge!")
        print("   • 'king hello' → I'll greet you")
        print("   • 'king how are you' → I'll respond casually")
        print("   • 'king who is Einstein' → I'll give facts")
        print("="*60)
    
    def load_user_name(self):
        try:
            with open('data/settings.json', 'r') as f:
                return json.load(f).get('user_name', 'User')
        except:
            return 'User'
    
    def human_response(self, command: str) -> str:
        """Handle human-like conversations"""
        cmd = command.lower()
        
      
        if any(word in cmd for word in ['hello', 'hi', 'hey', 'hlo', 'helo']):
            responses = [
                f"Hello {self.user_name}! How can I help you today?",
                f"Hi there! What would you like to know?",
                f"Hey! I'm here to answer your questions.",
                f"Hello! Ready to share some knowledge with you!"
            ]
            return random.choice(responses)
        
    
        elif any(phrase in cmd for phrase in ['how are you', 'how r u', 'how do you do']):
            responses = [
                "I'm doing great, thanks for asking! Ready to help you learn something new.",
                "I'm excellent! Just waiting for your next question about science, history, or anything!",
                "All systems operational! How can I assist you today?",
                "I'm fantastic! Full of knowledge and ready to share!"
            ]
            return random.choice(responses)
        

        elif any(phrase in cmd for phrase in ['what are you doing', 'what r u doing', 'whats up']):
            responses = [
                "I'm here, ready to answer your questions about any topic on Wikipedia!",
                "Just waiting for you to ask me about Einstein, quantum physics, or whatever interests you!",
                "I'm scanning Wikipedia, preparing to give you the best answers possible!",
                "I'm doing great! Just hanging out, ready to help you learn!"
            ]
            return random.choice(responses)
        

        elif any(word in cmd for word in ['thank', 'thanks', 'thank you']):
            responses = [
                "You're welcome! Happy to help!",
                "My pleasure! Ask me anything else!",
                "Anytime! That's what I'm here for!",
                "Glad I could help! What else would you like to know?"
            ]
            return random.choice(responses)
        
     
        elif any(word in cmd for word in ['bye', 'goodbye', 'see you', 'exit', 'quit']):
            self.running = False
            responses = [
                f"Goodbye {self.user_name}! Come back anytime!",
                f"See you later! Feel free to ask more questions!",
                f"Bye! It was nice talking with you!"
            ]
            return random.choice(responses)
        

        elif any(phrase in cmd for phrase in ['how old are you', 'your age', 'who made you']):
            responses = [
                "I'm an AI assistant created to help people learn from Wikipedia! I'm always learning new things.",
                "I don't have an age - I'm a program designed to share knowledge with you!",
                "I was created to be your knowledge companion. I'm here whenever you need information!"
            ]
            return random.choice(responses)

        elif any(phrase in cmd for phrase in ['what can you do', 'your capabilities', 'help']):
            return self.show_help()
        
        elif any(phrase in cmd for phrase in ['time', 'what time']):
            return f"The current time is {datetime.now().strftime('%I:%M %p')}"
        
        # Date
        elif any(phrase in cmd for phrase in ['date', 'what day']):
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}"
        
        # Set name
        elif cmd.startswith('my name is '):
            name = cmd.replace('my name is', '').strip()
            if name:
                self.user_name = name
                self.save_user_name(name)
                return f"Nice to meet you, {name}! How can I help you today?"
        
        return None  # Not a human query, try Wikipedia
    
    def save_user_name(self, name):
        """Save user name"""
        settings_file = Path('data/settings.json')
        settings_file.parent.mkdir(exist_ok=True)
        with open(settings_file, 'w') as f:
            json.dump({'user_name': name}, f)
    
    def show_help(self):
        """Show help"""
        help_text = f"""
👑 **{self.name} ASSISTANT - COMMANDS**

Say "{self.wake_word}" followed by:

💬 **CASUAL CHAT:**
  • "king hello" → I'll greet you
  • "king how are you" → Casual response
  • "king what are you doing" → Friendly chat
  • "king thanks" → You're welcome!
  • "king bye" → Goodbye

📚 **KNOWLEDGE QUESTIONS:**
  • "king who is Albert Einstein"
  • "king what is quantum physics"
  • "king history of Rome"
  • "king who is Donald Trump"
  • "king explain black holes"

⏰ **SYSTEM:**
  • "king time" - Current time
  • "king date" - Today's date
  • "king my name is [name]" - Set your name
  • "king help" - Show this menu
"""
        print(help_text)
        return "Help menu displayed. I can chat like a human AND give you Wikipedia knowledge!"
    
    def get_answer(self, command: str) -> str:
        """Get answer - either human chat or Wikipedia"""
        
        # First try human-like response
        human_reply = self.human_response(command)
        if human_reply:
            return human_reply
        
        # If not human query, try Wikipedia
        print(f"\n🔍 Searching for information about: '{command}'")
        answer = self.wikipedia.get_detailed_answer(command)
        
        if answer:
            return answer
        else:
            return f"I couldn't find information about '{command}'. Try asking about a different topic, or just chat with me!"
    
    def run(self):
        """Main loop"""
        self.voice.speak(f"Hello {self.user_name}! I'm {self.name} Assistant. I can chat with you AND answer questions. Try saying 'king hello' or 'king who is Einstein'")
        
        while self.running:
            try:
                # Try voice first
                command = self.voice.listen()
                
                # If no voice, try text
                if not command:
                    command = input("\n📝 You: ").strip().lower()
                
                if command:
                    # Remove wake word if present
                    if command.startswith(self.wake_word):
                        command = command[len(self.wake_word):].strip()
                    
                    if command:
                        response = self.get_answer(command)
                        self.voice.speak(response)
                        
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.voice.speak(f"Goodbye {self.user_name}! Come back anytime!")
                break
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(1)

def main():
    """Main function"""
    try:
        Path('data').mkdir(exist_ok=True)
        assistant = KingAssistant()
        assistant.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()



