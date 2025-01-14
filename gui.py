import tkinter as tk
import customtkinter
from time import strftime
import webbrowser
import psutil
import platform

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


class GraphicalUserInterface:
    root_instance = None

    def __init__(self, process_command_func=None):
        self.root = customtkinter.CTk(fg_color="#0d0f13")
        self.root.title("Assistant GUI")
        # self.root.geometry("810x600")
        self.create_sidebar()
        self.create_main_frame()
        self.process_command_func = process_command_func
        self.update_time()

    def create_sidebar(self):
        side_bar_frame = customtkinter.CTkFrame(
            self.root, width=140, corner_radius=0, fg_color="#16182d"
        )
        side_bar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        side_bar_frame.grid_rowconfigure(4, weight=1)
        logo_label = customtkinter.CTkLabel(
            side_bar_frame, text="AIRA", font=("Inter ExtraBold", 60)
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        settings_button = customtkinter.CTkButton(
            side_bar_frame,
            text="Settings",
            font=("Arial", 20),
            command=None,
            corner_radius=100,
            fg_color="#fff",
            text_color="#000",
            hover=False,
            border_spacing=5,
        )
        settings_button.grid(row=1, column=0, padx=20, pady=10)
        sidebar_button_2 = customtkinter.CTkButton(
            side_bar_frame,
            text="About",
            font=("Arial", 20),
            command=self.open_about,
            corner_radius=100,
            fg_color="#fff",
            text_color="#000",
            hover=False,
            border_spacing=5,
        )
        sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        theme_label = customtkinter.CTkLabel(
            side_bar_frame, text="Theme", font=("Consolas", 15)
        )
        theme_label.grid(row=5, column=0, padx=20, pady=(10, 10))
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            side_bar_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
            fg_color="#30365c",
            text_color="#fff",
            dropdown_fg_color="#16182d",
            dropdown_text_color="#fff",
            button_color="#30365c",
        )
        appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Create a label to display the message
        label = customtkinter.CTkLabel(side_bar_frame, text="Input Mode:")
        label.grid(row=7, column=0)

        # Create a StringVar object to store the selected mode
        var = customtkinter.StringVar(side_bar_frame)
        var.set("Text")  # Set the default selected mode as 't'
        mode_selection_dropdown = customtkinter.CTkOptionMenu(
            side_bar_frame,
            values=["Text", "Speech"],
            variable=var,
            fg_color="#30365c",
            text_color="#fff",
            dropdown_fg_color="#16182d",
            dropdown_text_color="#fff",
            button_color="#30365c",
        )
        # Create radio buttons for the two modes
        mode_selection_dropdown.grid(row=8, column=0, padx=20, pady=(10, 10))

        # Add a label to display internet connection status
        internet_status_label = customtkinter.CTkLabel(
            side_bar_frame, text="", corner_radius=10
        )
        internet_status_label.grid(row=9, column=0, padx=20, pady=(10, 10), sticky="we")

        def update_internet_status():
            """
            Updates the internet status label with green if connected, red if not.
            """
            import socket

            try:
                # connect to the host "google.com" (does not send any data)
                socket.create_connection(("google.com", 80))
                internet_status_label.configure(
                    text="Internet: Online", fg_color="#40ad4e"
                )
            except OSError:
                internet_status_label.configure(
                    text="Internet: Offline", fg_color="#ad4040"
                )

            # Update the stats every 10 seconds
            side_bar_frame.after(10000, update_internet_status)

        # Call the function initially to update the status
        update_internet_status()

        # Add labels to display computer and network stats
        cpu_label = customtkinter.CTkLabel(
            side_bar_frame,
            corner_radius=5,
            text="CPU: " + psutil.cpu_percent(interval=1).__str__() + "%",
            fg_color="#30365c",
        )
        cpu_label.grid(row=10, column=0, padx=20, pady=(5, 5), sticky="we")

        memory_percent = psutil.virtual_memory().percent
        memory_label = customtkinter.CTkLabel(
            side_bar_frame,
            corner_radius=5,
            text="Memory: " + f"{memory_percent:.0f}%",
            fg_color="#30365c",
        )
        memory_label.grid(row=11, column=0, padx=20, pady=(5, 5), sticky="we")
        platform_label = customtkinter.CTkLabel(
            side_bar_frame,
            corner_radius=5,
            text="System: " + platform.system(),
            fg_color="#30365c",
        )
        platform_label.grid(row=12, column=0, padx=20, pady=(5, 5), sticky="we")

        # Function to handle the selection of the mode from the GUI
        def select_mode():
            """
            Handles the selection of the mode from the GUI.
            """
            global mode_var
            mode_var = var.get()
            print(mode_var)
            pass

    def create_main_frame(self):
        main_frame = customtkinter.CTkFrame(
            self.root, width=630, height=600, corner_radius=0, fg_color="#0c0f12"
        )
        main_frame.grid(row=0, column=1, sticky="nsew")
        self.user_input_entry = customtkinter.CTkEntry(
            main_frame,
            placeholder_text="Input Command",
            height=40,
            width=400,
            corner_radius=10,
            font=("Consolas", 15),
            border_color="#30365c",
            placeholder_text_color="#30365c",
            fg_color="#16182d",
        )

        self.user_input_entry.place(rely=0.8, anchor="center", relx=0.5)

        self.ok_button = customtkinter.CTkButton(
            main_frame,
            text="Send",
            command=self.handle_ok_click,
            width=100,
            height=40,
            corner_radius=20,
            font=("Arial", 20),
            fg_color="#16182d",
        )
        self.ok_button.place(
            rely=0.8,
            anchor="center",
            relx=0.91,
        )
        self.user_input_entry.bind("<Return>", self.handle_ok_click)
        self.output_text = customtkinter.CTkLabel(
            main_frame,
            text="Press the SEND button",
            font=("Consolas", 15),
            text_color="whitesmoke",
            fg_color="#16182d",
            corner_radius=60,
        )
        self.output_text.place(relx=0.01, rely=0.1, anchor="nw")
        self.time_label = customtkinter.CTkLabel(
            main_frame,
            text="...",
            font=("Consolas", 12),
            fg_color="black",
            text_color="white",
            corner_radius=10,
        )
        self.time_label.place(relx=0.99, rely=0.99, anchor="se")
        self.user_input_label = customtkinter.CTkLabel(
            main_frame,
            text="Press the SEND button...",
            font=("Consolas", 15),
            text_color="#c5c1c1",
            fg_color="#16182d",
            corner_radius=60,
        )
        self.user_input_label.place(relx=0.981, rely=0.01, anchor="ne")

    def update_time(self):
        time_string = strftime("%c")
        self.time_label.configure(text=time_string)
        self.root.after(100, self.update_time)

    def handle_ok_click(self, event=None):
        print("Calling functions")
        try:
            # Get user input from the entry widget
            user_input = self.user_input_entry.get()
            print(user_input)
            self.user_input_entry.delete(
                0, customtkinter.END
            )  # Clear the entry after use
            self.process_command_func(query=user_input)
        except Exception as e:
            print(f"{e}")

    def display_user_input(self, input_text):
        self.user_input_label.configure(text=f"> {input_text}")

    def display_output(self, output_text):
        self.output_text.configure(text=f"{output_text}")

    def open_settings(self):
        print("Opening settings...")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def open_about(self):
        about_window = customtkinter.CTkToplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")
        about_window.transient(self.root)
        about_window.grab_set()
        about_window.attributes("-topmost", True)
        about_window.attributes("-topmost", False)

        about_label = customtkinter.CTkLabel(
            about_window,
            text="A.I.R.A\nVersion 1.0GUI\nDeveloped by Infinotiver",
            font=("Consolas", 14),
            anchor="center",
        )
        about_label.pack(pady=(10, 0))

        code_label = customtkinter.CTkLabel(
            about_window,
            text="This is a voice / text operated personal assistant ",
        )
        code_label.pack(pady=(0, 5))

        code_button = customtkinter.CTkButton(
            about_window,
            text="View Source Code",
            command=self.open_code,
            fg_color="black",
            corner_radius=100,
        )
        code_button.place(relx=0.5, rely=0.6, anchor="center")
        code_button.place(anchor="center", rely=0.6, relx=0.5)

    def open_code(self):
        webbrowser.open_new("https://github.com/infinotiver/Aira-Voice-Assistant")

    def start_gui(self):
        self.root.mainloop()


# Incase of testing
def start_gui_alone():
    app_gui = GraphicalUserInterface(process_command_func=None)
    app_gui.start_gui()


# start_gui_alone()
