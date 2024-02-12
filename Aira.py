import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
import wolframalpha
import os
import smtplib
import subprocess
import ctypes
import time
import requests
import json
import shutil
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pyjokes
from gtts import gTTS

# Replace with your personal details and API keys
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[1].id)  # Choose a mystical voice
assistant_name = "Mystica"  # Customize assistant name

def speak(audio):
    """Print and speak the given audio message with a mystical touch."""
    print(f"\033[35m{audio}\033[0m")
    engine.say(audio)
    engine.runAndWait()

def mystical_greet():
    """Greet the user with a mystical touch."""
    hour = int(datetime.datetime.now().hour)
    greetings = {
        0: "A mystical morning awakens, beckoning you forth.",
        12: "The midday sun shines brightly, casting its magic upon you.",
        18: "The moon whispers secrets in the evening sky, inviting you to dream.",
    }
    speak(greetings.get(hour, "Greetings, traveler!"))

def mystical_farewell():
    """Bid farewell to the user with a mystical touch."""
    speak("May your journey be filled with wonder and enchantment. Farewell!")

def takeCommand():
    """Capture and return a user command, allowing voice and text input."""
    r = sr.Recognizer()

    try:
        # Listen for voice input
        print("Speak your wish...")
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.dynamic_energy_threshold = False
            audio = r.listen(source, timeout=30)  # Set timeout to 30 seconds

        print("Understanding your command...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")

        return query

    except Exception as e:
        print(e)
        print("Speak or type your command:")

        # Allow text input as backup
        query = input("> ")
        return query

def sendEmail(to, content):
    """Send an email using your credentials."""
    # Replace with your email and password
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()
    speak("Your message has been sent through the ether!")