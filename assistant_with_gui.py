import tkinter as tk
import customtkinter
from threading import Thread
from time import strftime
from gui import AssistantGUI 
from aira import *
# (import) skills
import skills.openapplications as openapplications
import skills.findfiles as findfiles
import skills.weather as weather
import skills.chat as chat
import skills.fonts as fonts
import skills.sendmail as sendmail
import skills.definition as definition



class AssistantWithGUI(AiraAssistant):
    def __init__(self):
        super().__init__()  # Initialize the Aira class

        self.app_gui = None


    def process_command(self,query):
        query = query.lower()
        #query="tell the time"
        self.app_gui.display_user_input(query)

        if "wikipedia" in query:
            self.speak("Searching wikipedia")
            query = query.replace("wikipedia", "")
            self.search_wikipedia(query)

        elif "open youtube" in query:
            self.speak(openapplications.Open_Applications.youtube())

        elif "youtube" in query:
            search_query = query.replace("youtube", "").strip()
            openapplications.Open_Applications.search_yt(search_query)

        elif "open google" in query:
            self.speak(openapplications.Open_Applications.google())

        elif "search on google" in query:
            search_query = query.replace("search on google", "")
            openapplications.Open_Applications.search_google(search_query)
            self.speak("Opening your browser for desired results")

        elif "open stackoverflow" in query:
            self.speak(openapplications.Open_Applications.stackoverflow())
            webbrowser.open("stackoverflow.com")

        elif "open aisc" in query:
            self.speak(openapplications.Open_Applications.aisc())
            webbrowser.open("aistudent.community")

        elif "open forum" in query or "open aisc forum" in query:
            self.speak(openapplications.Open_Applications.aisc_forum())

        elif "define" in query:
            query = query.replace("define", "")
            try:
                word_data = definition.get_word_definition(query)
                word_data = definition.speak_definition(query, word_data)
                self.speak(word_data)
            except Exception as e:
                self.speak(str(e))

        elif "play music" in query or "play song" in query:
            self.speak("Here you go with music")
            music_dir = r"C:\Users\ADMIN\Desktop\Pranjal Prakarsh\[M] Media\Tunes"
            music_thread = Thread(target=self.play_music, args=(music_dir,))
            music_thread.start()

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            response=f"The time is {strTime}"
            self.app_gui.display_output(response)
            self.speak(response)
            

        elif "exit" in query:
            self.speak("Thanks for giving me your time")
            self.mystical_farewell()
        else:
            response="I don't understand that yet"
            self.app_gui.display_output(response)
            self.speak(response)
            
    def start_gui(self):
        if not self.app_gui:
            self.app_gui = AssistantGUI(process_command_func=self.process_command)
            self.app_gui.start_gui()
        else:
            print("GUI already running.")


if __name__ == "__main__":
    assistant_with_gui = AssistantWithGUI()
    assistant_with_gui.start_gui()