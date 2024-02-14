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
import shutil
import random
from bs4 import BeautifulSoup
import json
from plyer import notification
from urllib.parse import quote
import keyboard

# import hugginfaceblenderbot

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
print(voices)
engine.setProperty("voice", voices[1].id)  # Choose female voice
engine.setProperty("volume", 1)
engine.setProperty("rate", 150)

assistant_name = "Aira"  # Customize assistant name


def notify(t, m):
    notification.notify(
        title=t,
        message=m,
        app_icon=None,
        timeout=5,
    )


def mode_select():
    speak(f"Please select an input mode for interacting with {assistant_name}")
    speak("1.Press 't' for Text Input Mode\n2.Press 's' for Speech Input Mode ")

    while True:
        if keyboard.is_pressed("t"):
            speak("You have successfully Selected : Text Input Mode")
            mode_var = 0
            time.sleep(0.6)
            break
        elif keyboard.is_pressed("s"):
            speak("You have successfully Selected : Speech Input Mode")
            mode_var = 1
            time.sleep(0.6)
            break
    return mode_var


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
    speak(greetings.get(hour, "Greetings, user!"))
    speak(f"This is {assistant_name} at your service.")
    notify("Aira", "Assistant woke up")


def mystical_farewell():
    """Bid farewell to the user with a mystical touch."""
    speak("May your journey be filled with wonder and enchantment. Farewell!")


# Function to get word definition from the API


def get_word_definition(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


# Function to format and speak the definition


def speak_definition(word, definition_data):
    if not definition_data:
        speak(f"Sorry, I couldn't find the definition for {word}.")
        return
    word_info = definition_data[0]

    # Word and phonetic pronunciation

    speak(f"The word {word} is pronounced as {word_info['phonetic']}.")

    # Meanings and definitions

    for meaning in word_info["meanings"]:
        part_of_speech = meaning["partOfSpeech"]
        speak(f"As a {part_of_speech}, it can mean:")

        for idx, definition in enumerate(meaning["definitions"], start=1):
            speak(f"{idx}. {definition['definition']}")
    # Synonyms and antonyms

    synonyms = word_info.get("synonyms", [])
    antonyms = word_info.get("antonyms", [])

    if synonyms:
        speak(f"Synonyms for {word} include: {', '.join(synonyms)}.")
    if antonyms:
        speak(f"Antonyms for {word} include: {', '.join(antonyms)}.")


def hugginfacechat():
    print("The bot is ready to talk!! (Type 'quit' to exit)")
    tokenizer, model = hugginfacechat.load_tokenizer_and_model()
    chat_round = 1
    chat_history_ids = None
    while True:
        inp = input("\nYou: ")

        if inp.lower() == "quit":
            break
        elif inp.lower() == "let's start":
            speak("Great! Let's start the chat.")
            chat_round = 1
            chat_history_ids = None
        elif inp.lower() == "exit":
            speak("Ending the chat. Goodbye!")
            break
        else:
            chat_history_ids = hugginfacechat.generate_response(
                tokenizer, model, chat_round, chat_history_ids
            )
            chat_round += 1


def get_news(category):
    try:
        newsapi = os.environ.get("NEWSAPI")

        if category.lower() == "national":
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        elif category.lower() == "headlines":
            url = f"https://newsapi.org/v2/top-headlines?apiKey={newsapi}"
        else:
            url = f"https://newsapi.org/v2/everything?q={category}&apiKey={newsapi}"
        try:
            response = requests.get(url)
        except:
            return speak("Looks like there is no internet connection")
        data = response.json()

        if data["status"] == "ok":
            articles = data["articles"][:5]  # Display only the top 5 news items
            if articles:
                speak(f"Here are some top {category} news:")
                print(f"=============== {category.upper()} ===============\n")
                for i, item in enumerate(articles, start=1):
                    speak(f"{i}. {item['title']}\n")
                    speak(f"{item['description']}\n")
            else:
                speak(f"Sorry, no {category} news available at the moment.")
        else:
            speak("Sorry, there was an issue fetching news. Please try again later.")
    except Exception as e:
        print(str(e))


def get_user_preference():
    speak(
        "Sure! What type of news would you like to hear? (world/national/something(enter word))"
    )
    user_preference = takeCommand().lower()
    return user_preference


def get_joke():
    try:
        api_url = f"https://api.popcat.xyz/joke"
        response = requests.get(api_url)
        data = response.json()
        joke = response["joke"]
    except Exception as e:
        print(e)
        joke = "What do you give a sick lemon? Lemonaid."
    return joke


def takeCommand():
    """Capture and return a user command, allowing voice and text input."""
    r = sr.Recognizer()

    try:
        # Listen for voice input

        print("Speak your wish...")
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.dynamic_energy_threshold = False
            audio = r.listen(source, timeout=15)  # Set timeout to 30 seconds
        print("Recognizing voice input...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User > {query}\n")

        return query
    except Exception as e:
        # print(e)

        print("Type your command:")

        # Allow text input as backup

        query = input("> ")
        return query


def sendEmail(to, password, content):
    """Send an email using your credentials."""
    # Replace with your email and password

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    email_id = os.environ.get("EMAIL_ID")
    email_password = password
    server.login(email_id, email_password)
    server.sendmail(email_id, to, content)
    server.close()
    speak("Your message has been sent through the ether!")


if __name__ == "__main__":
    clear = lambda: os.system("cls")

    # This Function will clean any
    # command before the execution of this python file

    clear()

    mystical_greet()

    while True:
        query = takeCommand().lower()

        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=5)
            except wikipedia.DisambiguationError as e:
                speak("There are multiple options. Please specify.")
                for i, option in enumerate(e.options, start=1):
                    speak(f"{i}. {option}")
                choice = int(input("Enter the number of your choice: "))
                results = wikipedia.summary(e.options[choice - 1], sentences=5)
            except Exception as error:
                pass
            speak("According to Wikipedia")
            speak(results)
        elif "open youtube" in query:
            speak("Here you go to Youtube")
            webbrowser.open("https://www.youtube.com")
        elif "youtube" in query:
            search_query = query.replace("youtube", "").strip()
            url_search = quote(search_query)
            webbrowser.open(
                f"https://www.youtube.com/results?search_query={url_search}"
            )
        elif "open google" in query:
            speak("Here you go to Google\n")
            webbrowser.open("google.com")
        elif "open stackoverflow" in query:
            speak("Here you go to Stack Over flow.Happy coding")
            webbrowser.open("stackoverflow.com")
        elif "open aisc" in query:
            speak("Here you go to AI student Community")
            webbrowser.open("aistudent.community")
        elif "open forum" in query or "open aisc forum" in query:
            speak("Here you go to AISC Forum")
            webbrowser.open("forum.aistudent.community")
        elif "define" in query:
            query = query.replace("define", "")
            try:
                word_data = get_word_definition(query)
                speak_definition(query, word_data)
            except Exception as e:
                speak(e)
        elif "play music" in query or "play song" in query:
            speak("Here you go with music")

            music_dir = "something"
            songs = os.listdir(music_dir)
            print(songs)
            random_song = os.startfile(os.path.join(music_dir, random.choice(songs)))
        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif "send a mail" in query:
            try:
                speak("What message I should deliver through the ether?")
                content = takeCommand()
                speak("Whom should I deliver the magical letter? ")
                to = input("Enter recipient's address > ")
                password = input("Enter your email password > ")
                sendEmail(to, password, content)
                speak("Message sent through the ether...!")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")
        elif "how are you" in query:
            speak("I am fine, Thank you")
            speak("How are you ?")
        elif "fine" in query:
            speak("It's good to know that you're fine")
        elif "change name" in query:
            speak("What would you like to call me, ")
            assistant_name = takeCommand()
            speak("Thanks for naming me")
        elif "change volume" in query or "set volume" in query:
            speak("Please tell the volume level (0.0 to 1.0)")
            volume = float(takeCommand())
            try:
                engine.setProperty(volume=volume)
                speak("Volume set to the desired level")
            except:
                speak(
                    "There was some problem in setting that volume, please recheck values"
                )
                pass
        elif "what's your name" in query or "what is your name" in query:
            speak("My friends call me")
            speak(assistant_name)
            print("My friends call me", assistant_name)
        elif "joke" in query:
            joke = get_joke()
            speak(joke)
        elif "exit" in query:
            speak("Thanks for giving me your time")
            mystical_farewell()
            # break()
        elif "calculate" in query:
            app_id = "Wolframalpha api id"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index("calculate")
            query = query.split()[indx + 1 :]
            res = client.query(" ".join(query))
            answer = next(res.results).text
            speak("The answer is " + answer)
        elif "search" in query or "play" in query:
            query = query.replace("search", "")
            query = query.replace("play", "")
            webbrowser.open(query)
        if "news" in query:
            user_preference = get_user_preference()

            if "world" in user_preference:
                get_news("world")
            elif "national" in user_preference:
                get_news(
                    "general"
                )  # You can customize this to a specific category for Indian news
            elif "headlines" in user_preference:
                get_news("top-headlines")
            else:
                speak("Sorry, I couldn't understand your preference. Please try again.")
        elif "lock window" in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()
        elif "shutdown system" in query:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call("shutdown /s")
        elif "don't listen" in query or "stop listening" in query:
            speak(
                f"For how much time you want to stop {assistant_name} from listening commands (in seconds)?"
            )
            a = int(takeCommand())
            time.sleep(a)
            speak("Master, the wait is over...")
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
            speak("What should I write?")
            note = takeCommand()
            file = open("Aira.txt", "w")
            speak("Sir, Should I include date and time")
            snfm = takeCommand()
            if "yes" in snfm or "sure" in snfm:
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
        elif assistant_name in query:
            speak("Model - Aira 1 Version 0 at your service")
            speak(assistant_name)
        elif "weather" in query:
            api_key = "Api key"
            base_url = "http://api.openweathermap.org / data / 2.5 / weather?"
            speak(" City name ")
            print("City name : ")
            city_name = takeCommand()
            complete_url = base_url + "appid =" + api_key + "&q =" + city_name
            pass
        else:
            speak("Sorry I don't understand that yet")
