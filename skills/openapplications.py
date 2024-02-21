import webbrowser
from plyer import notification
import keyboard
from urllib.parse import quote

class OpenApplications:
    @staticmethod
    def open_website(url, display_name):
        webbrowser.open(url)
        response = f"Opening {display_name}"
        return response

    @staticmethod
    def youtube():
        return OpenApplications.open_website("https://www.youtube.com", "Youtube")

    @staticmethod
    def google():
        return OpenApplications.open_website("https://www.google.com", "Google")

    @staticmethod
    def stackoverflow():
        return OpenApplications.open_website(
            "https://stackoverflow.com", "Stack Overflow"
        )

    @staticmethod
    def aisc():
        return OpenApplications.open_website("https://aistudent.community", "AISC")

    @staticmethod
    def aisc_forum():
        return OpenApplications.open_website(
            "https://forum.aistudent.community", "AISC Forum"
        )

    @staticmethod
    def open_custom_application(application_name, url):
        return OpenApplications.open_website(url, application_name)
    @staticmethod
    def search_yt(query):
        url_search = quote(query)
        webbrowser.open(
            f"https://www.youtube.com/results?search_query={url_search}"
        )
        return True
    @staticmethod
    def search_google(query):
        url_search = quote(query)
        webbrowser.open("https://www.google.com/search?q=" + "+".join(url_search))
        return True