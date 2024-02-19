import tkinter as tk
import customtkinter
from time import strftime

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
customtkinter.set_default_color_theme("blue")

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistant GUI")
        self.root.geometry("800x600")

        self.create_sidebar()
        self.create_main_frame()

        self.update_time()

    def create_sidebar(self):
        self.sidebar_frame = tk.Frame(
            self.root, bg="#333333", padx=10, pady=15
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.create_navbar_buttons()

    def create_navbar_buttons(self):
        self.settings_button = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Settings",
            command=self.open_settings,
            width=150,
            height=40,
            corner_radius=20,
        )
        self.settings_button.pack(pady=(100, 10))

        self.menu_button = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Menu",
            command=self.toggle_navbar,
            width=150,
            height=40,
            corner_radius=20,
        )
        self.menu_button.pack(pady=10)

    def toggle_navbar(self):
        # Toggle between expanding and collapsing the navbar
        if self.settings_button.winfo_ismapped():
            self.settings_button.pack_forget()
        else:
            self.settings_button.pack(pady=(100, 10))

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, width=600, height=600, padx=10, pady=15)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.aira_label = tk.Label(
            self.main_frame, text="Aira", font=("Helvetica", 24)
        )
        self.aira_label.place(relx=0.5, rely=0.4, anchor="center")

        self.record_button = customtkinter.CTkButton(
            self.main_frame,
            text="Record",
            command=self.start_recording,
            width=150,
            height=40,
            corner_radius=20,
        )
        self.record_button.place(relx=0.5, rely=0.6, anchor="center")

        self.time_label = tk.Label(
            self.main_frame, text="", font=("Helvetica", 12), anchor="e"
        )
        self.time_label.pack(side="bottom", anchor="e", pady=(0, 10), padx=(0, 10))

    def update_time(self):
        # Update the time dynamically
        time_string = strftime("%H:%M:%S %p")
        self.time_label.config(text=time_string)
        self.root.after(1000, self.update_time)

    def start_recording(self):
        # Hide Aira text and display alternative text
        self.aira_label.place_forget()
        self.record_button.place_forget()

        recording_label = tk.Label(
            self.main_frame, text="Recording...", font=("Helvetica", 24)
        )
        recording_label.place(relx=0.5, rely=0.5, anchor="center")

        # You can implement the recording functionality here

    def open_settings(self):
        # Placeholder for opening settings
        print("Opening settings...")

if __name__ == "__main__":
    root = tk.Tk()

    app = AssistantGUI(root)
    root.mainloop()
