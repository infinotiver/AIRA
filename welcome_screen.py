from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import customtkinter

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(
    r"C:\Users\ADMIN\Desktop\Pranjal Prakarsh\[S] Programming\AIRA_GUI_TktDesigner\build\assets\frame0"
)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = customtkinter.CTk()

window.geometry("1300x700")
window.configure(bg="#0D0F13")


canvas = customtkinter.CTkCanvas(
    window,
    bg="#0D0F13",
    height=700,
    width=1300,
    highlightthickness=0,
    bd=0,
    relief="ridge",
)

canvas.place(x=0, y=0)


button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = customtkinter.CTkButton(
    window,
    # image=button_image_1,
    command=lambda: print("button_1 clicked"),
    fg_color="#0D0F13",
    text="None",
    hover_color="#0D0F13",
    width=363.0,
    height=79.0,
    border_color="#0D0F13",
)
button_1.place(x=705.0, y=524.0)


button_2 = customtkinter.CTkButton(
    None,
    command=lambda: print("button_2 clicked"),
    text="Know More",
    fg_color="#b9b7c6",
    text_color="#000",
    bg_color="transparent",
    width=370.0,
    corner_radius=60,
    height=80.0,
)
button_2.place(
    x=216.0,
    y=524.0,
)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = customtkinter.CTkButton(
    window,
    image=button_image_3,
    width=205.0,
    height=46.0,
    fg_color="#16182d",
    command=lambda: print("button_3 clicked"),
)
button_3.place(
    x=1068.0,
    y=29.0,
)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = customtkinter.CTkButton(
    window,
    image=button_image_4,
    width=266.0,
    height=43.0,
    command=lambda: print("button_4 clicked"),
)
button_4.place(
    x=1007.0,
    y=88.0,
)
window.resizable(False, False)
window.mainloop()
