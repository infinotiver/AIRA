import tkinter as tk
import customtkinter
from time import strftime
from threading import Timer
import webbrowser
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
customtkinter.set_default_color_theme("blue")

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistant GUI")
        self.root.geometry("800x600")

        self.create_sidebar()
        self.create_main_frame()

        # Start updating time
        self.update_time()

    def create_sidebar(self):
        sidebar_frame = customtkinter.CTkFrame(
            self.root, width=900, height=900, fg_color="#333333",corner_radius=0,
            
        )
        sidebar_frame.grid(row=0, column=0, sticky="ns",ipadx=10)

        settings_button = customtkinter.CTkButton(
            sidebar_frame,
            text="Settings",
            command=self.open_settings,
            width=150,
            height=40,
            corner_radius=20,
        )
        settings_button.pack(pady=(100, 10))

        about_button = customtkinter.CTkButton(
            sidebar_frame,
            text="About",
            command=self.open_about,
            width=150,
            height=40,
            corner_radius=20,
        )
        about_button.pack(pady=10)
        connected_button=customtkinter.CTkButton(
            sidebar_frame,
            text="Not Connected",
            width=150,
            height=40,
            corner_radius=20,
            state="disabled",
            fg_color=("red","darkred"),
            text_color="white",
            text_color_disabled="white"
        )
        connected_button.pack(pady=10)
        

    def create_main_frame(self):
        main_frame = customtkinter.CTkFrame(self.root, width=630, height=600,corner_radius=0)
        main_frame.grid(row=0, column=1, sticky="nsew")
        
        self.record_button = customtkinter.CTkButton(
            main_frame,
            text="Record",
            command=self.start_recording,
            width=150,
            height=40,
            corner_radius=20,
            font=("Arial", 25) 
        )
        self.record_button.place(relx=0.5, rely=0.5, anchor="center")

        self.user_input_label = customtkinter.CTkLabel(
            main_frame, text="", font=("Helvetica", 15), text_color="black", fg_color="#c6c2c2",corner_radius=10
        )
        self.user_input_label.place(relx=0.981, rely=0.01, anchor="ne")

        self.output_text = customtkinter.CTkLabel(
            main_frame, text="", font=("Helvetica", 15), text_color="black", fg_color="#c5c1c1", corner_radius=10
        )
        self.output_text.place(relx=0, rely=0.1, anchor="nw")
        self.time_label = customtkinter.CTkLabel(
            main_frame, text="", font=("Helvetica", 12), fg_color="#333333", text_color="white", corner_radius=10
        )
        self.time_label.place(relx=0.99, rely=0.99, anchor="se")

    def update_time(self):
        # Update the time dynamically
        
        time_string = strftime("%I:%M:%S %p")
        self.time_label.configure(text=time_string)
        self.root.after(1000, self.update_time)

    def start_recording(self):
        # Simulating recording and recognizing user input
        user_input = "This is a sample user input."  # Replace this with the actual recognized input
        self.display_user_input(user_input)

        # Add your logic to convert audio input to text and display the result
        output_text = "This is the recognized text from audio input."  # Replace this with the actual result
        self.display_output(output_text)

        # Schedule to clear the output after 10 seconds
        timer = Timer(10, self.clear_output)
        timer.start()

    def display_user_input(self, input_text):
        self.user_input_label.configure(text=f"User Input: {input_text}")

    def display_output(self, output_text):
        self.output_text.configure(text=f"Output: {output_text}")

    def clear_output(self):
        self.output_text.configure(text="")
        self.user_input_label.configure(text="")

    def open_settings(self):
        # Placeholder for opening settings
        print("Opening settings...")

    def open_about(self):
        # Create an app info window
        about_window = customtkinter.CTkToplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")

        about_label = customtkinter.CTkLabel(about_window, text="Assistant GUI\nVersion 1.0\nDeveloped by Infinotiver (Pranjal Prakarsh)`",font=("Arial",11))
        code_label=customtkinter.CTkLabel(about_window,text="This is a voice / text operated personal assistant ")
        code_button=customtkinter.CTkButton(about_window,text="View Source Code",command=self.open_code,fg_color="black",corner_radius=5)
        about_label.pack(pady=10)
        code_label.pack(pady=5)
        code_button.place(anchor="center",rely=0.6,relx=0.5)

    def open_code(self):
        webbrowser.open_new("https://github.com/infinotiver/Aira-Voice-Assistant")
if __name__ == "__main__":
    root = customtkinter.CTk()

    app = AssistantGUI(root)
    root.mainloop()
