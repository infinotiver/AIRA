import tkinter as tk
from threading import Thread
from time import strftime
from gui import AssistantGUI  # Assuming you have the AssistantGUI class in a separate file
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
        super().__init__()

        self.root = tk.Tk()
        self.app_gui = AssistantGUI(self.root, self.process_command)

    def process_command(self):
        mode = 1
        query = self.take_command(mode).lower()
        self.app_gui.display_user_input(self,query)

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
            music_thread = threading.Thread(
                target=assistant.play_music, args=(music_dir,)
            )
            music_thread.start()

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            assistant.speak(f"The time is {strTime}")

        elif "exit" in query:
            assistant.speak("Thanks for giving me your time")
            assistant.mystical_farewell()

    def start_gui(self):
        self.app_gui.start()

if __name__ == "__main__":
    assistant_with_gui = AssistantWithGUI()
    assistant_with_gui.start_gui()
