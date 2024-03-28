import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
import wolframalpha
import os
import subprocess
import ctypes
import time
import requests
from bs4 import BeautifulSoup
from plyer import notification
from urllib.parse import quote
import keyboard
import threading
#
import pygame

# (import) skills
import skills.openapplications as openapplications
import skills.findfiles as findfiles
import skills.weather as weather
import skills.chat as chat
import skills.fonts as fonts
import skills.sendmail as sendmail
import skills.definition as definition

# Initialize pygame mixer
pygame.mixer.init()


class AiraAssistant:
    def __init__(self):
        # Initialize speech engine
        self.engine = pyttsx3.init("sapi5")
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[1].id)  # Choose female voice
        self.engine.setProperty("volume", 0.9)
        self.engine.setProperty("rate", 190)

        self.assistant_name = "Aira"  # Customize assistant name

        # calling the Nominatim tool
        #self.loc = Nominatim(user_agent="GetLoc")

        # Initialize pygame mixer
        pygame.mixer.init()

        # Set appearance mode for fonts
        # fonts.bootup()

    def play_music(self, music_dir):
        songs = os.listdir(music_dir)
        for x in songs:
            self.speak(f"Now playing... {x}")
            pygame.mixer.music.load(os.path.join(music_dir, x))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)  # Adjust the tick value as needed

    def notify(self, title, message):
        notification.notify(
            title=title, message=message, app_icon=None, timeout=5,
        )

    def mode_select(self):
        self.speak(
            f"Please select an input mode for interacting with {self.assistant_name}"
        )
        self.speak("Press 't' for Text Input Mode\nPress 's' for Speech Input Mode ")

        while True:
            if keyboard.is_pressed("t"):
                self.speak("You have successfully selected: Text Input Mode")
                mode_var = 0
                time.sleep(0.6)
                break
            elif keyboard.is_pressed("s"):
                self.speak("You have successfully selected: Speech Input Mode")
                mode_var = 1
                time.sleep(0.6)
                break
        return mode_var

    def search_wikipedia(self, query):

        try:
            results = wikipedia.summary(query, sentences=5)
        except wikipedia.DisambiguationError as e:
            self.speak("There are multiple options. Please specify.")
            for i, option in enumerate(e.options[:10], start=1):
                self.speak(f"{i}. {option}", 1)
            choice = int(input("Enter the number of your choice: "))
            self.engine.setProperty("rate", 200)  # to reduce time wastage
            results = wikipedia.summary(e.options[choice - 1], sentences=5)
        except Exception as error:
            print(error)

        self.speak("According to Wikipedia")
        if results:
            self.speak(results)
        else:
            self.speak("No results were there")

    def speak(self, audio):
        """Print and speak the given audio message with a mystical touch."""
        print(f"\033[35m{audio}\033[0m")
        self.engine.say(audio)
        self.engine.runAndWait()

    def mystical_greet(self):
        """Greet the user with a mystical touch."""
        hour = int(datetime.datetime.now().hour)
        greetings = {
            0: "A mystical morning awakens, beckoning you forth.",
            12: "The midday sun shines brightly, casting its magic upon you.",
            18: "The moon whispers secrets in the evening sky, inviting you to dream.",
        }

        self.speak(greetings.get(hour, "Greetings, user!"))
        self.notify("Aira", "Assistant woke up")

    def mystical_farewell(self):
        """Bid farewell to the user with a mystical touch."""
        self.speak("May your journey be filled with wonder and enchantment. Farewell!")

    def get_user_preference(self):
        self.speak(
            "Sure! What type of news would you like to hear? (world/national/something(enter word))"
        )
        user_preference = self.take_command(mode).lower()
        return user_preference

    def get_news(self, category):
        try:
            newsapi = os.environ.get("NEWSAPI")

            if category.lower() == "national":
                url = (
                    f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
                )
            elif category.lower() == "headlines":
                url = f"https://newsapi.org/v2/top-headlines?apiKey={newsapi}"
            else:
                url = f"https://newsapi.org/v2/everything?q={category}&apiKey={newsapi}"
            try:
                response = requests.get(url)
            except:
                return self.speak("Looks like there is no internet connection")
            data = response.json()

            if data["status"] == "ok":
                articles = data["articles"][:5]  # Display only the top 5 news items
                if articles:
                    self.speak(f"Here are some top {category} news:")
                    print(f"=============== {category.upper()} ===============\n")
                    for i, item in enumerate(articles, start=1):
                        self.speak(f"{i}. {item['title']}\n")
                        self.speak(f"{item['description']}\n")
                else:
                    self.speak(f"Sorry, no {category} news available at the moment.")
            else:
                self.speak(
                    "Sorry, there was an issue fetching news. Please try again later."
                )
        except Exception as e:
            print(str(e))

    def get_fun_fact(self):
        api_url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(api_url)
        data = response.json()
        fun_fact = data["text"]
        self.speak(f"Here's a fun fact for you: {fun_fact}")

    # Search for programming tutorials on YouTube
    def search_programming_tutorials(self):
        self.speak("What programming topic are you interested in?")
        topic = self.takeCommand(mode)
        webbrowser.open(
            f"https://www.youtube.com/results?search_query={quote(topic)}+programming+tutorial"
        )
        self.speak(
            f"I found some programming tutorials on YouTube for {topic}. Check them out!"
        )

    def get_tech_news(self):
        api_key = os.getenv("NEWS_API_KEY")
        url = (
            f"https://newsapi.org/v2/top-headlines?category=technology&apiKey={api_key}"
        )
        response = requests.get(url)
        data = response.json()

        if data["status"] == "ok" and data["articles"]:
            articles = data["articles"][:5]
            self.speak("Here are some top technology news headlines:")
            for i, article in enumerate(articles, start=1):
                self.speak(f"{i}. {article['title']}")
                self.speak(article["description"])
        else:
            self.speak("Sorry, I couldn't fetch technology news at the moment.")

    def send_whatsapp_message(self):
        self.speak("Whom do you want to send a WhatsApp message?")
        contact = self.takeCommand()
        self.speak(f"What message would you like to send to {contact}?")
        message = self.takeCommand()
        self.speak("Sending the message.")
        return "W.I.P"
        """
        pywhatkit.sendwhatmsg(
            contact,
            message,
            datetime.datetime.now().hour,
            datetime.datetime.now().minute + 1,
        )
        """

    def get_joke():
        try:
            api_url = f"https://api.popcat.xyz/joke"
            response = requests.get(api_url)
            data = response.json()
            joke = data["joke"]
        except Exception as e:
            print(e)
            joke = "What do you give a sick lemon? Lemonaid."
        return joke

    def take_command(self, mode):
        if mode == 1:
            """Capture and return a user command, allowing voice and text input."""
            r = sr.Recognizer()

            print("Speak your wish...")
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                r.pause_threshold = 1
                r.dynamic_energy_threshold = False
                r.adjust_for_ambient_noise(source, duration=2)

                audio = r.listen(source)  # Set timeout to 30 seconds
            print("Recognizing voice input...")
            query = r.recognize_google(audio, language="en-in")

            print(f"User > {query}\n")

            return query

        elif mode == 0:
            print("Type your command:")
            query = input("> ")
            return query


def process_command():
    assistant = AiraAssistant()
    mode = 1
    query = assistant.take_command(mode).lower()

    # Add your if-elif conditions for different functionalities within the class

    if "wikipedia" in query:
        assistant.speak("Searching wikipedia")
        query = query.replace("wikipedia", "")
        assistant.search_wikipedia(query)

    elif "open youtube" in query:
        assistant.speak(openapplications.Open_Applications.youtube())

    elif "youtube" in query:
        search_query = query.replace("youtube", "").strip()
        openapplications.Open_Applications.search_yt(search_query)

    elif "open google" in query:
        assistant.speak(openapplications.Open_Applications.google())

    elif "search on google" in query:
        search_query = query.replace("search on google", "")
        openapplications.Open_Applications.search_google(search_query)
        assistant.speak("Opening your browser for desired results")

    elif "open stackoverflow" in query:
        assistant.speak(openapplications.Open_Applications.stackoverflow())
        webbrowser.open("stackoverflow.com")

    elif "open aisc" in query:
        assistant.speak(openapplications.Open_Applications.aisc())
        webbrowser.open("aistudent.community")

    elif "open forum" in query or "open aisc forum" in query:
        assistant.speak(openapplications.Open_Applications.aisc_forum())

    elif "define" in query:
        query = query.replace("define", "")
        try:
            word_data = definition.get_word_definition(query)
            word_data = definition.speak_definition(query, word_data)
            assistant.speak(word_data)
        except Exception as e:
            assistant.speak(str(e))

    elif "play music" in query or "play song" in query:
        assistant.speak("Here you go with music")
        music_dir = r"C:\Users\ADMIN\Desktop\Pranjal Prakarsh\[M] Media\Tunes"
        music_thread = threading.Thread(target=assistant.play_music, args=(music_dir,))
        music_thread.start()

    elif "the time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        assistant.speak(f"The time is {strTime}")

    elif "exit" in query:
        assistant.speak("Thanks for giving me your time")
        assistant.mystical_farewell()


if __name__ == "__main__":
    process_command()

    