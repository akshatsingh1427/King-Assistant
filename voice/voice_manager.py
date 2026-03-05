"""
Voice Manager - Speech input and output
"""

import time

class VoiceManager:
    """Manage voice input and output"""
    
    def __init__(self):
        self.engine = None
        self.recognizer = None
        
        # Try to initialize TTS
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 160)
            self.engine.setProperty('volume', 0.9)
            print("  • Text-to-Speech: Ready")
        except ImportError:
            print("  • Text-to-Speech: Install 'pyttsx3' for voice")
        
        # Try to initialize STT
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.mic = sr.Microphone()
            print("  • Speech Recognition: Ready")
        except ImportError:
            print("  • Speech Recognition: Install 'SpeechRecognition' for voice input")
        except:
            print("  • Microphone: Not found")
    
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
        """Listen for voice input"""
        if not self.recognizer:
            return None
        
        try:
            with self.mic as source:
                print("\n🎤 Listening... (speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
            
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            return text.lower()
        except:
            return None