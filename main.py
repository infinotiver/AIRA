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
from geopy.geocoders import Nominatim 
import pywhatkit

# (import) skills
import skills.openapplications as openapplications
import skills.findfiles as findfiles
import skills.weather as weather
import skills.chat as chat
import skills.fonts as fonts
import skills.sendmail as sendmail
import skills.definition as definition
import pygame
# Initialisation
# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Choose female voice
engine.setProperty("volume", 0.9)
engine.setProperty("rate", 190)

assistant_name = "Aira"  # Customize assistant name


# Initialize pygame mixer
pygame.mixer.init()




def play_music(music_dir):
    songs = os.listdir(music_dir)
    for x in songs:
        speak(f"Now playing... {x}")
        pygame.mixer.music.load(os.path.join(music_dir, x))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Adjust the tick value as needed


def notify(t, m):
    notification.notify(
        title=t, message=m, app_icon=None, timeout=5,
    )


def mode_select():
    speak(f"Please select an input mode for interacting with {assistant_name}")
    speak("Press 't' for Text Input Mode\nPress 's' for Speech Input Mode ")

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

def search_wikipedia(query):
 
    try:
        results = wikipedia.summary(query, sentences=5)
    except wikipedia.DisambiguationError as e:
        speak("There are multiple options. Please specify.")
        for i, option in enumerate(e.options[:10], start=1):
            speak(f"{i}. {option}",1)
        choice = int(input("Enter the number of your choice: "))
        engine.setProperty("rate", 200)
        results = wikipedia.summary(e.options[choice - 1], sentences=5)
    except Exception as error:
        print(error)

    speak("According to Wikipedia")
    if results:
        speak(results)
    else:
        speak("No results were there")


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
    notify("Aira", "Assistant woke up")


def mystical_farewell():
    """Bid farewell to the user with a mystical touch."""
    speak("May your journey be filled with wonder and enchantment. Farewell!")



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
    user_preference = takeCommand(mode).lower()
    return user_preference


def get_fun_fact():
    api_url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(api_url)
    data = response.json()
    fun_fact = data["text"]
    speak(f"Here's a fun fact for you: {fun_fact}")


# Search for programming tutorials on YouTube
def search_programming_tutorials():
    speak("What programming topic are you interested in?")
    topic = takeCommand(mode)
    webbrowser.open(
        f"https://www.youtube.com/results?search_query={quote(topic)}+programming+tutorial"
    )
    speak(f"I found some programming tutorials on YouTube for {topic}. Check them out!")


def get_tech_news():
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?category=technology&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "ok" and data["articles"]:
        articles = data["articles"][:5]
        speak("Here are some top technology news headlines:")
        for i, article in enumerate(articles, start=1):
            speak(f"{i}. {article['title']}")
            speak(article["description"])
    else:
        speak("Sorry, I couldn't fetch technology news at the moment.")


def send_whatsapp_message():
    speak("Whom do you want to send a WhatsApp message?")
    contact = takeCommand()
    speak(f"What message would you like to send to {contact}?")
    message = takeCommand()
    speak("Sending the message.")
    pywhatkit.sendwhatmsg(
        contact,
        message,
        datetime.datetime.now().hour,
        datetime.datetime.now().minute + 1,
    )


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


def takeCommand(mode):
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
        # print(e)

        print("Type your command:")

        # Allow text input as backup

        query = input("> ")
    return query





if __name__ == "__main__":
    clear = lambda: os.system("cls")
    clear()
    fonts.bootup()

    mode = mode_select()
    mystical_greet()

    while True:
        query = takeCommand(mode).lower()

        if "wikipedia" in query:
            
            speak("Searching wikipedia")
            query = query.replace("wikipedia", "")
            search_wikipedia(query)

        elif "open youtube" in query:
            speak(openapplications.Open_Applications.youtube())

        elif "youtube" in query:

            search_query = query.replace("youtube", "").strip()
            url_search = quote(search_query)
            webbrowser.open(
                f"https://www.youtube.com/results?search_query={url_search}"
            )
        elif "open google" in query:
            speak(openapplications.Open_Applications.google())
        elif "search on google" in query:
            search_query = query.replace("search on google", "")
            url_search = quote(search_query)
            webbrowser.open("https://www.google.com/search?q=" + "+".join(url_search))
            speak("Opening your browser for desired results")
        elif "open stackoverflow" in query:
            speak(openapplications.Open_Applications.stackoverflow())
            webbrowser.open("stackoverflow.com")
        elif "open aisc" in query:
            speak(openapplications.Open_Applications.aisc())
            webbrowser.open("aistudent.community")
        elif "open forum" in query or "open aisc forum" in query:
            speak(openapplications.Open_Applications.aisc_forum())

        elif "define" in query:
            query = query.replace("define", "")
            try:
                word_data = definition.get_word_definition(query)
                word_data=definition.speak_definition(query, word_data)
                speak(word_data)
            except Exception as e:
                speak(e)
        elif "play music" in query or "play song" in query:
            speak("Here you go with music")

            music_dir = r"C:\Users\ADMIN\Desktop\Pranjal Prakarsh\[M] Media\Tunes"

            # Create a new thread for playing music
            music_thread = threading.Thread(target=play_music, args=(music_dir,))
            music_thread.start()

        elif "the time" in query:

            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "send a mail" in query:
            try:
                speak("What message I should deliver through the ether?")
                content = takeCommand(mode)
                speak("Whom should I deliver the magical letter? ")
                to = input("Enter recipient's address > ")
                password = input("Enter your email password > ")
                sendmail.sendEmail(to, password, content)
                speak("Message sent through the ether...!")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif "how are you" in query:
            speak("I am fine, how are you")
        elif "fine" in query:
            speak("It's good to know that you're fine")
        elif "change name" in query:
            speak("What would you like to call me, ")
            assistant_name = takeCommand(mode)
            speak("Thanks for naming me")
        elif "change volume" in query or "set volume" in query:
            speak("Please tell the volume level (0.0 to 1.0)")
            volume = float(takeCommand(mode))
            try:
                engine.setProperty(volume=volume)
                speak("Volume set to the desired level")
            except:
                speak(
                    "There was some problem in setting that volume, please recheck values"
                )
                pass
        elif "change mode" in query or "mode" in query:
            mode_select()
        elif "what's your name" in query or "what is your name" in query:
            speak("My friends call me ")
            speak(assistant_name)

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
        elif "news" in query:
            user_preference = get_user_preference()

            if "world" in user_preference:
                get_news("world")
            elif "national" in user_preference:
                get_news(
                    "general"
                )  
            elif "headlines" in user_preference:
                get_news("top-headlines")
            else:
                speak("Sorry, I couldn't understand your preference. Please try again.")
        elif "lock window" in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()
        elif "shutdown system" in query:
            speak("Hold On a Sec ! Your system is on its way to shut down.\nExecuting command in three seconds.")
            subprocess.call("shutdown /s")
        elif "don't listen" in query or "stop listening" in query:
            speak(
                f"For how much time you want to stop {assistant_name} from listening commands (in seconds)?"
            )
            a = int(takeCommand(mode))
            speak("You can also press 'w' key to resume")

            # Add a loop to check if 'w' key is pressed during the sleep
            for _ in range(a * 10):  # Assuming you check every 0.1 seconds
                if keyboard.is_pressed("w"):
                    speak("Resuming...")
                    break

                time.sleep(0.1)

            speak("Master, the wait is over...")
        elif "where is" in query:

            time.sleep(3)
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            try:
                getLoc = loc.geocode(location)
            except Exception as e:
                print(e)
            ind = query.split()
            location = query[ind + 8 :]
            url = "https://www.google.com/maps/place/" + "".join(location)
            webbrowser.open(url)
            if getLoc:
                speak(getLoc.address)
                webbrowser.open(getLoc.address)
            webbrowser.open_new_tab(url)

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
        elif "hibernate" in query:
            speak("Hibernating")
            subprocess.call("shutdown /h")
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
            api_key = os.environ.get("WEATHER")
            print(api_key)  # Replace with your OpenWeatherMap API key
            speak("Please tell me the city name.")
            city_name = takeCommand(mode)
            response = weather.get_weather(api_key, city_name)
            speak(response)
        elif "open gmail" in query:
            webbrowser.open("gmail.com")
            speak("Google Mail opened")

        elif "take snapshot" in query or "screen snip" in query:
            speak("Opening screen snipping tool")
            keyboard.press_and_release("win+shift+s")
        elif "dictate" in query:
            speak("Opening dictation mode")
        elif "fun fact" in query:
            get_fun_fact()
            keyboard.press_and_release("win+H")
        elif "image conversion" in query:
            ima = input("Enter the Path of Image :")
            pywhatkit.image_to_ascii_art(
                img_path=ima, output_file=f"{assistant_name}_asciiart"
            )
            speak("Made your ASCII code and saved it.")
        elif "find a file" in query or "find file " in query:
            query = query.replace("find a file", " ")
            results = findfiles.find_file_in_all_drives(query)
            for x in results:
                speak(x)

        else:

            assistant_reply = chat.get_chat_response(query)
            if assistant_reply:
                speak(assistant_reply)
            else:
            
                text = quote(query)
                botname = quote(assistant_name)
                url = f"https://api.popcat.xyz/chatbot?msg={text}&owner=Pranjal+Prakarsh&botname={botname}"
                try:
                    request = requests.get(url)
                    data = request.json()
                    output = data["response"]
                    speak(output)
                except:
                    speak("Sorry, I don't understand that")
