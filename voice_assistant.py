 
import speech_recognition as sr
import pyttsx3
from config import Config

class VoiceAssistant:
    """
    Manages voice commands (listening) and text-to-speech (speaking).
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)

    def speak(self, text):
        """
        Converts text to speech.
        """
        print(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_for_command(self):
        """
        Listens for a command containing the wake word.
        Returns the command string or None if no valid command is heard.
        """
        with self.microphone as source:
            print(f"Listening for '{Config.WAKE_WORD}'...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=Config.LISTENING_TIMEOUT, phrase_time_limit=5)
                # Use Google's recognizer for higher accuracy
                command = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: '{command}'")

                if Config.WAKE_WORD in command:
                    # Extract the command after the wake word
                    return command.replace(Config.WAKE_WORD, "").strip()
                
            except sr.UnknownValueError:
                # This is common, so we don't need to print an error.
                pass
            except sr.WaitTimeoutError:
                print("Listening timed out.")
            except Exception as e:
                print(f"Could not process audio: {e}")
        
        return None