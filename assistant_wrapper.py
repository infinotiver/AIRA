from enum import Enum
import logging
import pyttsx3
from collections import deque
from typing import List, Any, Optional
import datetime
import time
import keyboard
import requests
import importlib.util
import speech_recognition as sr
from plyer import notification


class InterfaceMode(Enum):
    TERMINAL = 0
    GUI = 1


class InputMode(Enum):
    TEXT = 0
    SPEECH = 1


class Wrapper:
    def __init__(
        self,
        name: str,
        interface_mode: InterfaceMode = InterfaceMode.TERMINAL,
        input_mode: InputMode = InputMode.TEXT,
        gui_instance: Optional[Any] = None,
    ) -> None:
        """
        Initialize the Chatbot class.

        Parameters:
            name (str): The name of the chatbot.
            interface_mode (InterfaceMode): The interface mode of the chatbot (InterfaceMode.TERMINAL for terminal mode, InterfaceMode.GUI for GUI mode).
            input_mode (InputMode): The input mode of the chatbot (InputMode.TEXT for text input, InputMode.SPEECH for speech input).
            gui_instance (Any): An optional GUI instance.

        Returns:
            None
        """
        self.name: str = name
        self.interface_mode: InterfaceMode = interface_mode
        self.input_mode: InputMode = input_mode
        self.clients: dict = {}  # Dictionary to store external clients
        self.commands: dict = {}  # Dictionary to store registered commands
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.engine: pyttsx3.Engine = pyttsx3.init("sapi5")
        self.voices: List[pyttsx3.voice.Voice] = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[1].id)  # Choose female voice
        self.engine.setProperty("volume", 0.9)
        self.engine.setProperty("rate", 190)
        self.command_history: deque[str] = deque(maxlen=5) # Stores the last 5 commands
        self.gui_instance = gui_instance  # Reference to the GUI instance

    def update_command_history(self, command):
        """Add a command to the command history."""
        self.command_history.append(command)

    def get_command_history(self) -> List[str]:
        """Return the command history as a list of strings."""
        return list(self.command_history)

    def change_interface_mode(self, mode: InterfaceMode):
        if isinstance(mode, InterfaceMode):
            self.interface_mode = mode
        else:
            raise ValueError(
                "Invalid interface mode. Use InterfaceMode.TERMINAL or InterfaceMode.GUI."
            )

    def change_input_mode(self, mode: InputMode):
        if isinstance(mode, InputMode):
            self.input_mode = mode
        else:
            raise ValueError(
                "Invalid input mode. Use InputMode.TEXT or InputMode.SPEECH."
            )

    def import_skill(self, skill_name):
        """Import a skill module dynamically."""
        try:
            if requests.get("http://www.google.com").status_code == 200:
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
            title=title,
            message=message,
            app_icon=None,
            timeout=5,
        )

    def select_input_mode(self):
        """
        Selects the input mode for interacting with the assistant.

        This function prompts the user to select the input mode for interacting with the assistant. The user can choose between text input mode and speech input mode by pressing 't' or 's' respectively. The function loops until a mode is selected and sets the `self.mode` attribute accordingly.

        Returns:
            int: The selected input mode. 0 for text input mode and 1 for speech input mode.

        """
        self.assistant_output(
            f"Please select an input mode for interacting with {self.name}"
        )
        self.assistant_output(
            "Press 't' for Text Input Mode\nPress 's' for Speech Input Mode"
        )

        mode_var = None

        # Loop until a mode is selected
        while True:
            if keyboard.is_pressed("t"):
                self.input_mode = InputMode.TEXT
                self.assistant_output("You have selected: Text Input Mode")
                break
            elif keyboard.is_pressed("s"):
                self.input_mode = InputMode.SPEECH
                self.assistant_output("You have selected: Speech Input Mode")
                break
            time.sleep(0.2)  

        return self.input_mode

    def assistant_gui_show_user_input(self, user_input: str):
        """
        Show the user input in the assistant GUI.

        Parameters:
            user_input (str): The input provided by the user.

        Raises:
            Exception: If the instance is not in GUI mode.

        Returns:
            None
        """
        if self.interface_mode != InterfaceMode.GUI:
            raise Exception("Not a GUI instance.")
        else:
            self.gui_instance.display_user_input(user_input)

    def assistant_output(self, response):
        """Handle assistant response output."""
        if self.interface_mode == InterfaceMode.TERMINAL:
            print(f"\033[35m{response}\033[0m")
        elif self.interface_mode == InterfaceMode.GUI:
            self.gui_instance.display_output(response)

        self.engine.say(response)
        self.engine.runAndWait()

    def greet(self):
        """Greet the user based on the time of the day."""
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            greetings = "Good Morning"
        elif hour >= 12 and hour < 18:
            greetings = "Good Afternoon"
        else:
            greetings = "Good Evening"

        self.assistant_output(f"{greetings} user")
        self.notify("Aira", "Assistant Initialized")

    def farewell(self):
        """Farewell message."""
        self.assistant_output(
            "May your journey be filled with wonder and enchantment. Farewell!"
        )

    def take_command(self, gui_user_input: Optional[str] = None) -> str
        """Capture user command through text or speech."""
        if self.input_mode == InputMode.SPEECH:
            recognizer = sr.Recognizer()
            print("Speak your wish...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                recognizer.pause_threshold = 1
                recognizer.dynamic_energy_threshold = False
                recognizer.adjust_for_ambient_noise(source, duration=2)
                audio = recognizer.listen(source)
            print("Recognizing voice input...")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"User > {query}\n")
            return query
        else:
            if gui_user_input is not None:
                return gui_user_input
            else:
                raise ValueError("Please pass user input.")
                
    def register_command(self, name: str, handler: callable, description: str = ""):
        """Registers a command manually."""
        self.commands[name] = {"handler": handler, "description": description}

    def dispatch_command(self, command_name: str, *args, **kwargs):
        """Dispatches a command by name."""
        if command_name in self.commands:
            return self.commands[command_name]["handler"](*args, **kwargs)
        else:
            self.assistant_output(f"Command '{command_name}' not found.")

    def command(self, name: str = None, description: str = ""):
        """
        Decorator for registering a command directly with a function.

        Usage:
        @bot.command(name="hello", description="Greet the user")
        def greet():
            print("Hi!")
        """
        def decorator(func):
            cmd_name = name or func.__name__
            self.register_command(cmd_name, func, description)
            return func
        return decorator