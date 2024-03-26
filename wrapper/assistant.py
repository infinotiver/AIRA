import asyncio
import logging
import speech_recognition as sr
import pyttsx3
import os
import time  # For time-related tasks
import requests  # For making API requests
from geopy.geocoders import Nominatim
from collections import deque 
# Consider using a threading library for concurrency (optional)

# [TODO] Natural Language Understanding (NLU) integration 

class VoiceAssistant:
    def __init__(self, name):
        self.name = name
        self.clients = {}  # Dictionary to store external clients
        self.commands = {}  # Dictionary to store registered commands
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.engine = pyttsx3.init("sapi5")
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[1].id)  # Choose female voice
        self.engine.setProperty("volume", 0.9)
        self.engine.setProperty("rate", 190)
        self.loc = Nominatim(user_agent="GetLoc")
        self.command_history = deque(maxlen=5)  # Stores the last 5 commands

    def add_client(self, client_name, client_instance):
        """Add an external client to the assistant."""
        self.clients[client_name] = client_instance

    def command(self, keyword):
        """Decorator to register a method as a command."""
        def decorator(func):
            self.commands[keyword] = func
            return func
        return decorator
    def update_command_history(self, command):
        """Add a command to the command history."""
        self.command_history.append(command)

    def get_command_history(self):
        """Return the command history as a list of strings."""
        return [str(command) for command in self.command_history]

    async def handle_command(self, command, *args, **kwargs):
        """Handle a recognized command."""
        if command in self.commands:
            func = self.commands[command]
            try:
                result = await func(*args, **kwargs)
                self.update_command_history(command)
                return result
            except Exception as e:
                self.logger.error(f"Error executing command '{command}': {e}")
                return f"An error occurred while executing the command: {e}"
        else:
            return f"Command '{command}' not recognized."
        
    async def listen(self):
        """Listen for user input continuously."""
        while True:
            user_input = input(f"{self.name}> ").lower()
            # Split user input into command and arguments
            command, *args = user_input.split()
            # Execute command asynchronously
            result = await self.handle_command(command, *args)
            print(result)
    def talk(self, text):
        """
        Convert the given text to speech.

        :param text: The text to convert.
        """
        self.engine.say(text)
        self.engine.runAndWait()