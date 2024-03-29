import tkinter as tk
import customtkinter
from time import strftime
import webbrowser

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


class AssistantGUI:
    root_instance = None

    def __init__(self, process_command_func):
        self.root = customtkinter.CTk()
        self.root.title("Assistant GUI")
        self.root.geometry("810x600")
        self.create_sidebar()
        self.create_main_frame()
        self.process_command_func = process_command_func
        self.update_time()

    def create_sidebar(self):
        side_bar_frame = customtkinter.CTkFrame(self.root, width=140,corner_radius=0,fg_color="gray10")
        side_bar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        side_bar_frame.grid_rowconfigure(4, weight=1)
        logo_label = customtkinter.CTkLabel(
            side_bar_frame,
            text="A.I.R.A.",
            font=("Consolas",20))
        logo_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 10)
                        )
        settings_button = customtkinter.CTkButton(side_bar_frame,text="Settings",font = ("Consolas", 15), command=None)
        settings_button.grid(row=1, column=0, padx=20, pady=10)
        sidebar_button_2 = customtkinter.CTkButton(side_bar_frame,text="About", font = ("Consolas",15), command=self.open_about)
        sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        theme_label = customtkinter.CTkLabel(side_bar_frame, text="Theme (Experimental)", font = ("Consolas",15))
        theme_label.grid(row=5,column=0, padx=20, pady=(10, 10))
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(side_bar_frame, values=["Dark","Light", "System"],command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))




    def create_main_frame(self):
        main_frame = customtkinter.CTkFrame(
            self.root, width=630, height=600, corner_radius=0
        )
        main_frame.grid(row=0, column=1, sticky="nsew")
        self.user_input_entry = customtkinter.CTkEntry(
            main_frame, placeholder_text = "Input Command",height=40,width=350, corner_radius=10,  font =("Consolas", 15)
        )
        self.user_input_entry.place(relx=0.3, rely=0.8, anchor="center")

        self.ok_button = customtkinter.CTkButton(
            main_frame,
            text="Send",
            command=self.handle_ok_click,
            width=100,
            height=40,
            corner_radius=100,
            font=("Consolas", 15),
        )
        self.ok_button.place(relx=0.7, rely=0.8, anchor="center")
        self.user_input_entry.bind("<Return>", self.handle_ok_click)

        self.output_text = customtkinter.CTkLabel(
            main_frame,
            text="",
            font =("Consolas", 15),
            text_color="whitesmoke",
            fg_color="#313338",
            corner_radius=60,
        )
        self.output_text.place(relx=0.01, rely=0.1, anchor="nw")
        self.time_label = customtkinter.CTkLabel(
            main_frame,
            text="",
            font =("Consolas", 12),
            fg_color="#333333",
            text_color="white",
            corner_radius=10,
        )
        self.time_label.place(relx=0.99, rely=0.99, anchor="se")
        self.user_input_label = customtkinter.CTkLabel(
            main_frame,
            text="Press the command button...",
            font =("Consolas", 15),
            text_color="#c5c1c1",
            fg_color="#303136",
            corner_radius=60,
        )
        self.user_input_label.place(relx=0.981, rely=0.01, anchor="ne")

    def update_time(self):
        time_string = strftime("%c")
        self.time_label.configure(text=time_string)
        self.root.after(100, self.update_time)

    def handle_ok_click(self,event=None):
        print("Calling functions")
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

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    def open_about(self):
        about_window = customtkinter.CTkToplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")

        about_label = customtkinter.CTkLabel(
            about_window,
            text="Assistant GUI\nVersion 1.0\nDeveloped by Infinotiver",
            font=("Consolas", 14),
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

# Incase of testing        
def start_gui_alone():
    app_gui = AssistantGUI(process_command_func=None)
    app_gui.start_gui()

#start_gui_alone()