import tkinter as tk
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
customtkinter.set_default_color_theme("blue")

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistant GUI")
        self.root.geometry("800x600")

        self.create_sidebar()
        self.create_main_frame()

    def create_sidebar(self):
        sidebar_frame = tk.Frame(
            self.root, width=200, height=600, bg="#333333", padx=10, pady=15
        )
        sidebar_frame.grid(row=0, column=0, sticky="ns")

        settings_button = customtkinter.CTkButton(
            sidebar_frame,
            text="Settings",
            command=self.open_settings,
            width=150,
            height=40,
            corner_radius=20,
        )
        settings_button.pack(pady=(100, 10))

        # Add more buttons in the sidebar as needed

    def create_main_frame(self):
        main_frame = tk.Frame(self.root, width=600, height=600, padx=10, pady=15)
        main_frame.grid(row=0, column=1, sticky="nsew")

        record_button = customtkinter.CTkButton(
            main_frame,
            text="Record",
            command=self.start_recording,
            width=150,
            height=40,
            corner_radius=20,
        )
        record_button.place(relx=0.5, rely=0.5, anchor="center")

        # Add main content here, e.g., chat window, results display, etc.

    def start_recording(self):
        # You can implement the recording functionality here
        print("Recording...")

    def open_settings(self):
        # Placeholder for opening settings
        print("Opening settings...")

if __name__ == "__main__":
    root = tk.Tk()

    app = AssistantGUI(root)
    root.mainloop()
