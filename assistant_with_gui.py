import traceback
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
try:
    import skills.findfiles as findfiles
except:
    pass
try:
    import skills.weather as weather
except:
    pass
try:
    import skills.chat as chat
except:
    pass
try:
    import skills.fonts as fonts
except:
    pass
try:
    import skills.sendmail as sendmail
except:
    pass
try:
    import skills.definition as definition
except:
    pass

from assistant_wrapper import AIRA_Interactive_Assistant
from gui import GraphicalUserInterface

class InteractiveAssistantWithGUI(AIRA_Interactive_Assistant):
    def __init__(self, gui_instance):
        super().__init__(name="Aira", mode=1, gui_instance=gui_instance)
        self.app_gui = None  # Initialize app_gui attribute
        """
    def process_command(self, gui_user_input=None):
        if self.mode == 0:
            query = self.take_command().lower()
        else:
            query = gui_user_input.lower()
        super().process_command(gui_user_input=query)
        """
    def gui_process_command(self, query):
        """
        Process a command from the GUI, show user input, and provide appropriate responses based on the query.
        
        Parameters:
            query (str): The command/query received from the GUI input.
        
        Returns:
            None
        """
        query = query.lower()
        # query="tell the time"
        self.assistant_gui_show_user_input(query)
        if "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            response = f"The time is {strTime}"
            self.assistant_output(response)

        elif "exit" in query:
            self.assistant_output("Thanks for giving me your time")
            self.farewell()
        else:
            response = "I don't understand that yet"
            self.assistant_output(response)


    def start_gui(self):
        if self.gui_instance is None:
            # Pass self.gui_process_command as process_command_func
            self.app_gui = GraphicalUserInterface(process_command_func=self.gui_process_command)
            self.app_gui.start_gui()
            return self.app_gui
        else:
            print("GUI instance already provided.")
            return self.gui_instance


if __name__ == "__main__":
    try:
        # Create an instance of AssistantGUI
        assistant_gui_instance = GraphicalUserInterface()

        # Create an instance of AssistantWithGUI with the gui_instance provided
        assistant_with_gui = InteractiveAssistantWithGUI(gui_instance=assistant_gui_instance)

        # Set the process_command_func of the AssistantGUI instance
        assistant_gui_instance.process_command_func = assistant_with_gui.gui_process_command

        # Start the GUI
        assistant_gui_instance.start_gui()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
