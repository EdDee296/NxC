from pathlib import Path
from tkinter import filedialog
import sys
sys.path.append('C:/Users/ASUS/OneDrive/New folder/New folder')

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, END
from main import *


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\OneDrive\New folder\New folder\build\assets\frame0")


def save():
    global name, data_path, logs_path
    name = entry_1.get()
    data_path = entry_2.get()
    logs_path = entry_3.get()
    print(name, data_path, logs_path)
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


def openFile(type):
    if type == "data":
        global data_path  # Use the global keyword to modify the global variable
        data_path = filedialog.askdirectory()
        data_path = data_path.replace('/', '\\')
        # Get a list of all entries (files and directories) in the folder
        entries = os.listdir(data_path)
        
        if len(entries) != 0:
            # Check if there are any non-image files or subdirectories
            subdirectories = []

            for entry in entries:
                full_path = os.path.join(data_path, entry)
                if not os.path.isdir(full_path):
                    entry_2.delete(0,END)
                    entry_2.insert(0,"Invalid directory.❌")
                    break
                else:
                    files = os.listdir(full_path)
                    for file in files:
                        file_path = os.path.join(full_path, file)
                        if os.path.isdir(file_path):
                            subdirectories.append(file)

            if subdirectories:
                entry_2.delete(0)
                entry_2.insert(0,"Invalid directory.❌")
            else:
                entry_2.delete(0,END)
                entry_2.insert(0,data_path)
                    

        else:
            entry_2.delete(0,END)
            entry_2.insert(0,"Invalid directory.❌")
    else:
        global logs_path
        logs_path = filedialog.askdirectory()
        logs_path = logs_path.replace('/', '\\')
        if os.path.isdir(logs_path):
            entry_3.delete(0,END)
            entry_3.insert(0,logs_path)
        else:
            entry_3.delete(0,END)
            entry_3.insert(0,"Invalid directory.❌")


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

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    335.0,
    34.0,
    image=image_image_1
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

entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=383.5,
    y=209.0,
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
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
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


image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    395,
    277.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    395,
    193.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    400,
    110.0,
    image=image_image_4
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: save(),
    relief="flat"
)
button_1.place(
    x=450.0,
    y=360.0,
    width=104.0,
    height=37.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: openFile("logs"),
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
    command=lambda: openFile("data"),
    relief="flat"
)
button_3.place(
    x=611.0,
    y=206.0,
    width=33.0,
    height=38.0
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    168.0,
    244.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    163.0,
    346.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    163.0,
    159.0,
    image=image_image_7
)
window.resizable(False, False)
window.mainloop()
