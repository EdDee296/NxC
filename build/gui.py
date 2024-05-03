


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\Downloads\Tkinter-Designer-master\Tkinter-Designer-master\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("670x423")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 423,
    width = 670,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    670.0,
    68.0,
    fill="#080707",
    outline="")

canvas.create_text(
    275.0,
    0.0,
    anchor="nw",
    text="Nx-C",
    fill="#FFFFFF",
    font=("Italiana Regular", 48 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    489.0,
    138.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=383.5,
    y=122.0,
    width=211.0,
    height=31.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    489.0,
    312.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=383.5,
    y=296.0,
    width=211.0,
    height=31.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    489.0,
    225.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=383.5,
    y=209.0,
    width=211.0,
    height=31.0
)

canvas.create_text(
    367.0,
    99.0,
    anchor="nw",
    text="Model’s name ",
    fill="#000000",
    font=("Rubik Regular", 12 * -1)
)

canvas.create_text(
    367.0,
    182.0,
    anchor="nw",
    text="Data Path",
    fill="#000000",
    font=("Arial", 12 * -1)
)

canvas.create_text(
    367.0,
    266.0,
    anchor="nw",
    text="Logs Path",
    fill="#000000",
    font=("Italiana Regular", 12 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=611.0,
    y=206.0,
    width=33.0,
    height=38.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=611.0,
    y=293.0,
    width=33.0,
    height=38.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=450.0,
    y=360.0,
    width=104.0,
    height=37.0
)

canvas.create_rectangle(
    0.0,
    66.0,
    336.0,
    423.0,
    fill="#404040",
    outline="")

canvas.create_text(
    11.0,
    77.0,
    anchor="nw",
    text="INSTRUCTION:\nName your image classification model.\nChoose a path in which you store your data.\nThis should be a folder, with different sub-folders\n for different classes.\nIn each sub-folder should be all of your data\n(in this case they are all the images\nto be used to train the model).\nChoose a path to store the logs when training your data.\nAfter you have entered everything,\npress OK to move to next step.",
    fill="#FFFFFF",
    font=("Inter", 12 * -1)
)

canvas.create_text(
    11.0,
    296.0,
    anchor="nw",
    text="Made by EdDee\nContact information:\nGithub: EdDee296\nLinkedin: David Pham\nDiscord: eddee296\nEmail: dav1dph869@gmail.com",
    fill="#FFFFFF",
    font=("Rubik Regular", 12 * -1)
)
window.resizable(False, False)
window.mainloop()