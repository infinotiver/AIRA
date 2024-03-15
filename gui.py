import tkinter as tk
import customtkinter
from time import strftime
import webbrowser

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class AssistantGUI:
    root_instance = None

    def __init__(self, process_command_func):
        self.root = customtkinter.CTk()
        self.root.title("Assistant GUI")
        self.root.geometry("800x600")
        self.create_sidebar()
        self.create_main_frame()
        self.process_command_func = process_command_func
        self.update_time()

    def create_sidebar(self):
        sidebar_frame = customtkinter.CTkFrame(
            self.root, width=900, height=900, fg_color="#333333", corner_radius=0,
        )
        sidebar_frame.grid(row=0, column=0, sticky="ns", ipadx=10)
        logo = customtkinter.CTkLabel(
            sidebar_frame, text="AIRA", font=("Spy Agency", 30),
        )
        logo.pack(pady=10)
        settings_button = customtkinter.CTkButton(
            sidebar_frame,
            text="Settings",
            command=self.open_settings,
            width=150,
            height=30,
            corner_radius=100,
            border_color="black",
        )
        settings_button.pack(pady=(100, 10))

        about_button = customtkinter.CTkButton(
            sidebar_frame,
            text="About",
            command=self.open_about,
            width=150,
            height=30,
            corner_radius=100,
        )
        about_button.pack(pady=10)
        optionmenu_var = customtkinter.StringVar(value="Voice Input")
        optionmenu = customtkinter.CTkOptionMenu(
            sidebar_frame,
            values=["Voice Input", "Text Input"],
            # command=optionmenu_callback,
            variable=optionmenu_var,
        )
        optionmenu.pack()

    def create_main_frame(self):
        main_frame = customtkinter.CTkFrame(
            self.root, width=630, height=600, corner_radius=0
        )
        main_frame.grid(row=0, column=1, sticky="nsew")

    def create_main_frame(self):
        main_frame = customtkinter.CTkFrame(
            self.root, width=630, height=600, corner_radius=0
        )
        main_frame.grid(row=0, column=1, sticky="nsew")

        self.user_input_entry = customtkinter.CTkEntry(
            main_frame, width=200, height=40, corner_radius=10, font=("Arial", 15),
        )
        self.user_input_entry.place(relx=0.3, rely=0.5, anchor="center")

        self.ok_button = customtkinter.CTkButton(
            main_frame,
            text="OK",
            command=self.handle_ok_click,
            width=100,
            height=40,
            corner_radius=20,
            font=("Arial", 15),
        )
        self.ok_button.place(relx=0.7, rely=0.5, anchor="center")

        self.output_text = customtkinter.CTkLabel(
            main_frame,
            text="",
            font=("Helvetica", 15),
            text_color="whitesmoke",
            fg_color="#313338",
            corner_radius=60,
        )
        self.output_text.place(relx=0.01, rely=0.1, anchor="nw")
        self.time_label = customtkinter.CTkLabel(
            main_frame,
            text="",
            font=("Helvetica", 12),
            fg_color="#333333",
            text_color="white",
            corner_radius=10,
        )
        self.time_label.place(relx=0.99, rely=0.99, anchor="se")
        self.user_input_label = customtkinter.CTkLabel(
            main_frame,
            text="Press the command button...",
            font=("Helvetica", 15),
            text_color="#c5c1c1",
            fg_color="#303136",
            corner_radius=60,
        )
        self.user_input_label.place(relx=0.981, rely=0.01, anchor="ne")

    def update_time(self):
        time_string = strftime("%I:%M %p")
        self.time_label.configure(text=time_string)
        self.root.after(60000, self.update_time)

    def handle_ok_click(self):
        # Get user input from the entry widget
        user_input = self.user_input_entry.get()
        print(user_input)
        self.user_input_entry.delete(0, customtkinter.END)  # Clear the entry after use
        self.process_command_func(query=user_input)

    def display_user_input(self, input_text):
        self.user_input_label.configure(text=f"User Input: {input_text}")

    def display_output(self, output_text):
        self.output_text.configure(text=f"Output: {output_text}")

    def open_settings(self):
        print("Opening settings...")

    def open_about(self):
        about_window = customtkinter.CTkToplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")

        about_label = customtkinter.CTkLabel(
            about_window,
            text="Assistant GUI\nVersion 1.0\nDeveloped by Infinotiver",
            font=("Arial", 14),
        )
        code_label = customtkinter.CTkLabel(
            about_window, text="This is a voice / text operated personal assistant "
        )
        code_button = customtkinter.CTkButton(
            about_window,
            text="View Source Code",
            command=self.open_code,
            fg_color="black",
            corner_radius=100,
        )
        about_label.pack(pady=10)
        code_label.pack(pady=5)
        code_button.place(anchor="center", rely=0.6, relx=0.5)

    def open_code(self):
        webbrowser.open_new("https://github.com/infinotiver/Aira-Voice-Assistant")

    def start_gui(self):
        self.root.mainloop()
