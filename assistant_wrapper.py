from typing import List
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
import os
import time
import requests
from plyer import notification
from urllib.parse import quote
import keyboard
import threading
import logging
from collections import deque 
import importlib.util
import requests

# (import) skills
import skills.openapplications as openapplications
import skills.findfiles as findfiles
import skills.weather as weather
import skills.chat as chat
import skills.fonts as fonts
import skills.sendmail as sendmail
import skills.definition as definition




# [TODO] Natural Language Understanding (NLU) integration 

class AIRA_Interactive_Assistant:
    def __init__(self, name: str, mode: int = 0, gui_instance=None) -> None:
        """
        Initialize the Chatbot class.

        Parameters:
            name (str): The name of the chatbot.
            mode (int): The mode of the chatbot (0 for terminal mode, 1 for GUI mode).
            gui_instance (Any): An optional GUI instance.

        Returns:
            None
        """
        self.name: str = name
        self.mode: int = mode  # 0 represents terminal mode, 1 represents GUI mode
        self.clients: dict = {}  # Dictionary to store external clients
        self.commands: dict = {}  # Dictionary to store registered commands
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.engine: pyttsx3.Engine = pyttsx3.init("sapi5")
        self.voices: List[pyttsx3.voice.Voice] = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[1].id)  # Choose female voice
        self.engine.setProperty("volume", 0.9)
        self.engine.setProperty("rate", 190)
        self.command_history: deque = deque(maxlen=5)  # Stores the last 5 commands
        self.gui_instance = gui_instance  # Reference to the GUI instance

    
    def update_command_history(self, command):
        """Add a command to the command history."""
        self.command_history.append(command)

    def get_command_history(self):
        """Return the command history as a list of strings."""
        return list(self.command_history)


    def change_mode(self,mode:int):
        if mode in (0,1):
            self.mode = mode
        else:
            raise ValueError("Invalid mode. Please enter 0 or 1.")
        
    def import_skill(skill_name):
        """Import a skill module dynamically."""
        try:
            if requests.get("http://www.google.com").status_code == 200:
                # If internet connection is available, import the skill module
                spec = importlib.util.find_spec(f"skills.{skill_name}")
                if spec:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return module
        except requests.ConnectionError:
            print("No internet connection. Skipping import of skill:", skill_name)
        return None
 
    def notify(self, title, message):
        """
        Notifies the user with a given title and message using a desktop notification.

        Parameters:
            title (str): The title of the notification.
            message (str): The message content of the notification.

        Returns:
            None
        """
        notification.notify(
            title=title, message=message, app_icon=None, timeout=5,
        )

    def mode_select(self):
        """
        Selects the input mode for interacting with the assistant.

        This function prompts the user to select the input mode for interacting with the assistant. The user can choose between text input mode and speech input mode by pressing 't' or 's' respectively. The function loops until a mode is selected and sets the `self.mode` attribute accordingly.

        Returns:
            int: The selected input mode. 0 for text input mode and 1 for speech input mode.

        """
        # If the input method is not equal to 1, prompt the user to select the mode using the keyboard
        self.assistant_output(f"Please select an input mode for interacting with {self.name}")
        self.assistant_output("Press 't' for Text Input Mode\nPress 's' for Speech Input Mode ")

        # Initialize the mode variable to None
        mode_var = None
        
        # Loop until a mode is selected
        while mode_var is None:
            # Check if 't' key is pressed
            if keyboard.is_pressed("t"):
                self.assistant_output("You have successfully selected: Text Input Mode")
                mode_var = 0  # Set the mode variable to 0 for text input mode
                time.sleep(0.6)  # Pause for 0.6 seconds
            # Check if 's' key is pressed
            elif keyboard.is_pressed("s"):
                self.assistant_output("You have successfully selected: Speech Input Mode")
                mode_var = 1  # Set the mode variable to 1 for speech input mode
                time.sleep(0.6)  # Pause for 0.6 seconds
        self.mode = mode_var
        return self.mode

    def assistant_gui_show_user_input(self,user_input:str):
        if not self.mode==1:
            raise "Not GUI INSTANCE"
        else:
            self.gui_instance.display_user_input(user_input)
    def assistant_output(self, response):

        """Print and speak the given audio message with a mystical touch."""
        if self.mode == 0:
            print(f"\033[35m{response}\033[0m")
            self.engine.say(response)
            self.engine.runAndWait()
        elif self.mode == 1:
            self.gui_instance.display_output(response) 
            self.engine.say(response)
            self.engine.runAndWait()
            

    def greet(self):
        """Greet the user with a mystical touch."""
        hour = int(datetime.datetime.now().hour)
        if hour> 0 and hour <= 12:
            greetings= "Good Morning"
        elif hour > 12 and hour <= 18:
            greetings= "Good Afternoon"
        else:
            greetings= "Good Evening"

        self.assistant_output(greetings," user ")
        self.notify("Aira", "Assistant Initialised")

    def farewell(self):
        """Bid farewell to the user with a mystical touch."""
        self.assistant_output("May your journey be filled with wonder and enchantment. Farewell!")


    def take_command(self, gui_user_input=None):
        """
        Capture and return a user command, allowing voice and text input.
        """
        if self.mode == 0:
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

        elif self.mode == 1:
            try :
                return gui_user_input
            except:
                raise " Please pass user input "


def process_command(self,gui_user_input=None):
    """
    Processes a command received from the user and performs the corresponding action.

    This function takes no parameters.

    Returns:
        None.

    Raises:
        None.
    """
    assistant = AIRA_Interactive_Assistant()
    if self.mode == 0:
        query = assistant.take_command().lower()
    else:
        query = assistant.take_command(gui_user_input=gui_user_input)


    if "wikipedia" in query:
        assistant.assistant_output("Searching wikipedia")
        query = query.replace("wikipedia", "")
        assistant.search_wikipedia(query)

    elif "open youtube" in query:
        assistant.assistant_output(openapplications.Open_Applications.youtube())

    elif "youtube" in query:
        search_query = query.replace("youtube", "").strip()
        openapplications.Open_Applications.search_yt(search_query)

    elif "open google" in query:
        assistant.assistant_output(openapplications.Open_Applications.google())

    elif "search on google" in query:
        search_query = query.replace("search on google", "")
        openapplications.Open_Applications.search_google(search_query)
        assistant.assistant_output("Opening your browser for desired results")

    elif "open stackoverflow" in query:
        assistant.assistant_output(openapplications.Open_Applications.stackoverflow())
        webbrowser.open("stackoverflow.com")

    elif "open aisc" in query:
        assistant.assistant_output(openapplications.Open_Applications.aisc())
        webbrowser.open("aistudent.community")

    elif "open forum" in query or "open aisc forum" in query:
        assistant.assistant_output(openapplications.Open_Applications.aisc_forum())

    elif "define" in query:
        query = query.replace("define", "")
        try:
            word_data = definition.get_word_definition(query)
            word_data = definition.speak_definition(query, word_data)
            assistant.assistant_output(word_data)
        except Exception as e:
            assistant.assistant_output(str(e))

    elif "play music" in query or "play song" in query:
        assistant.assistant_output("Here you go with music")
        music_dir = r"C:\Users\ADMIN\Desktop\Pranjal Prakarsh\[M] Media\Tunes"
        music_thread = threading.Thread(target=assistant.play_music, args=(music_dir,))
        music_thread.start()

    elif "the time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        assistant.assistant_output(f"The time is {strTime}")

    elif "exit" in query:
        assistant.assistant_output("Thanks for giving me your time")
        assistant.farewell()




    