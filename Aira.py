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
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen
from gtts import gTTS

# Replace with your personal details and API keys
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[1].id)  # Choose a mystical voice
assistant_name = "Aira"  # Customize assistant name

def speak(audio):
    """Print and speak the given audio message with a mystical touch."""
    print(f"\033[35m{audio}\033[0m")
    engine.say(audio)
    engine.runAndWait()

def mystical_greet():
    """Greet the user with a mystical touch."""
    hour = int(datetime.datetime.now(tz="Asia/Kolkata").hour)
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

        print("Recognizing voice input...")
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

if __name__ == '__main__':
    clear = lambda: os.system('cls')

    # This Function will clean any
    # command before execution of this python file
    clear()

    mystical_greet()

    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=5)
            except wikipedia.DisambiguationError as e:
                choice = random.choice(e.options)
                results = wikipedia.summary(choice, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Here you go to Google\n")
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            speak("Here you go to Stack Over flow.Happy coding")
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query or "play song" in query:
            speak("Here you go with music")

            music_dir = "something"
            songs = os.listdir(music_dir)
            print(songs)
            random_song = os.startfile(os.path.join(music_dir, random.choice(songs)))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f" the time is {strTime}")

        elif 'send a mail' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("whom should I send")
                to = input()
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you,")

        elif 'fine' in query:
            speak("It's good to know that you're fine")

        elif "change my name to" in query:
            query = query.replace("change my name to", "")
            assistant_name = query

        elif "change name" in query:
            speak("What would you like to call me, ")
            assistant_name = takeCommand()
            speak("Thanks for naming me")

        elif "what's your name" in query or "What is your name" in query:
            speak("My friends call me")
            speak(assistant_name)
            print("My friends call me", assistant_name)

        elif 'joke' in query:
            speak("Work In progress")

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            mystical_farewell()

        elif "calculate" in query:
            app_id = "Wolframalpha api id"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is " + answer)

        elif 'search' in query or 'play' in query:
            query = query.replace("search", "")
            query = query.replace("play", "")
            webbrowser.open(query)

        elif 'news' in query:
            try:
                jsonObj = urlopen('''https://newsapi.org / v1 / articles?source = the-times-of-india&sortBy = top&apiKey =\\times of India Api key\\''')
                data = json.load(jsonObj)
                i = 1

                speak('here are some top news from the times of india')
                print('''=============== TIMES OF INDIA ============''' + '\n')

                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                print(str(e))

        elif 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'shutdown system' in query:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call('shutdown / p /f')

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop Aira from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl / maps / place/" + location + "")

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])

        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")

        elif "log off" in query or "sign out" in query:
            speak("Make sure all the applications are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "write a note" in query:
            speak("What should i write,")
            note = takeCommand()
            file = open('Aira.txt', 'w')
            speak("Sir, Should I include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)

        elif "show note" in query:
            speak("Showing Notes")
            file = open("Aira.txt", "r")
            print(file.read())
            speak(file.read(6))

        elif "Aira" in query:
            wishMe()
            speak("Aira 1 Version 0 in your service")
            speak(assistant_name)

        elif "weather" in query:
            api_key = "Api key"
            base_url = "http://api.openweathermap.org / data / 2.5 / weather?"
            speak(" City name ")
            print("City name : ")
            city_name = takeCommand()
            complete_url = base_url + "appid =" + api_key + "&q =" + city_name
