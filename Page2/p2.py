from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Radiobutton, IntVar, StringVar, ttk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\Downloads\Tkinter-Designer-master\Tkinter-Designer-master\Page2\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# pos is [x,y]

def increment_pos(pos: list, x: int):
    pos[1] += x
    return pos

init_pos = {'button_add_layer': [119.0, 341.0], 
            'btn_rm': [220.0, 273.0], 
            'add_arg': [335, 310], 
            'button_ok': [330, 380],
            'index': [70.0, 269.0],
            'equal': [180.0, 304.0],
            'layer_combobox': [133.0, 273.0],
            'arg_combobox': [125.0, 304.0],
            'textbox': [250.0, 310.0]}

increase = 100

class Layer():
    def __init__(self, window: Tk, canvas: Canvas, layer: list, args: list):
        self.window = window
        self.canvas = canvas
        self.layer = layer
        self.args = args
        self.index = 0
        self.layer_names = {}
        self.arg_names = {}
        self.images = []
        self.add_layer_btn = self.create_button("button_2.png", init_pos["button_add_layer"], 84.0, 17.0, self.init_layer)
        self.ok_btn = self.create_button("button_1.png", init_pos["button_ok"], 104, 37, lambda: print("layers: ", self.layer_names," args: ", self.arg_names))
        
    def init_layer(self):
        self.create_layer_name(init_pos['index'], init_pos['layer_combobox'])
        self.create_argument(init_pos['arg_combobox'], init_pos['equal'], init_pos['textbox'])
        self.create_button("button_3.png", init_pos["btn_rm"], 76.0, 13.0, lambda: print('layer removed'))
        self.create_button("button_4.png", init_pos["add_arg"], 77, 11, lambda: print('add arg'))

        increment_pos(init_pos["btn_rm"], increase)
        increment_pos(init_pos["add_arg"], increase)
        increment_pos(init_pos["arg_combobox"], increase)
        increment_pos(init_pos["equal"], increase)
        increment_pos(init_pos["textbox"], increase)
        increment_pos(init_pos['index'], increase)
        increment_pos(init_pos['layer_combobox'], increase)
        self.canvas.coords(self.add_layer_btn,init_pos['button_add_layer'])
        increment_pos(init_pos["button_add_layer"], increase)
        self.canvas.coords(self.ok_btn,init_pos["button_ok"])
        increment_pos(init_pos['button_ok'], increase)

    def add_name(self, dict, name):
        dict[self.index]=name
        
    def create_layer_name(self, index_pos: list, layer_pos: list):
        index = self.canvas.create_text( 
            index_pos[0],
            index_pos[1],
            anchor="nw",
            text=str(self.index+1)+'.',
            fill="#000000",
            font=("Inter", 12 * -1)
        )
        self.index +=1

        layer_var = StringVar()
        layer_var.trace_add("write", lambda *arg: self.add_name(self.layer_names, layer_var.get()))

        layer = ttk.Combobox(self.window, values=self.layer, width=10, textvariable=layer_var, state="readonly")
        self.canvas.create_window(
            layer_pos[0],
            layer_pos[1],
            window=layer
        )

        return layer, index

    def create_argument(self, arg_pos: list, equal_pos: list, textbox_pos: list):
        arg_var = StringVar()
        arg_var.trace_add("write", lambda *arg: self.add_name(self.arg_names, arg_var.get()))
        arg = ttk.Combobox(self.window, values=self.args, width=7, textvariable=arg_var, state="readonly")
        self.canvas.create_window(
            arg_pos[0],
            arg_pos[1],
            window=arg
        )

        equal = self.canvas.create_text( 
            equal_pos[0],
            equal_pos[1],
            anchor="nw",
            text="=",
            fill="#000000",
            font=("Inter", 12 * -1)
        )

        textbox = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.canvas.create_window(
            textbox_pos[0],
            textbox_pos[1],
            width=80.0,
            height=16.0,
            window=textbox
        )
        
        return arg, textbox, equal
    
    def create_button(self, img_name, button_pos: list, width, height, command):
        img = PhotoImage(
            file=relative_to_assets(img_name))
        self.images.append(img)  # Add the image to the list of images
        button = Button(
            image=img,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        button_id = self.canvas.create_window(
            button_pos[0],
            button_pos[1],
            width=int(width),
            height=int(height),
            window=button
        )
        
        return button_id

    def remove_argument(self, arg, textbox, equal):
        self.delete(arg, textbox, equal)

    def remove_layer(self, layer, index):
        self.delete(layer, index)


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
    relief = "ridge",
    scrollregion = (0,0,2000,5000)
)
canvas.place(x = 0, y = 0)

# # mousewheel scrolling 
canvas.bind('<MouseWheel>', lambda event: canvas.yview_scroll(-int(event.delta / 60), "units"))
# scrollbar 
scrollbar = ttk.Scrollbar(window, orient = 'vertical', command = canvas.yview)
canvas.configure(yscrollcommand = scrollbar.set)
scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
app_name = canvas.create_image(
    335.0,
    34.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
gpu_lim = canvas.create_image(
    330.70001220703125,
    96.51399993896484,
    image=image_image_2
)

# Add radio buttons
radio_var = IntVar()
radio_button_1 = Radiobutton(
    window,
    text="Yes",
    variable=radio_var,
    value=True,
    bg="#FFFFFF",
    selectcolor="#FFFFFF",
    font=("Arial", 8)
)
canvas.create_window(
    280,
    120,
    window=radio_button_1
)
radio_button_2 = Radiobutton(
    window,
    text="No",
    variable=radio_var,
    value=False,
    bg="#FFFFFF",
    selectcolor="#FFFFFF",
    font=("Arial", 8)
)
canvas.create_window(
    380,
    120,
    window=radio_button_2
)
lim = 0
def print_selection():
    global lim
    lim = radio_var.get()
    print(lim)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
md_config = canvas.create_image(
    333.9100036621094,
    141.5,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
md_label = canvas.create_image(
    112.91000366210938,
    172.51400756835938,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
md_type = canvas.create_image(
    335.0,
    174.0,
    image=image_image_5
)

layer = ['a', 'b', 'c', 'd', 'e', 'f']
args = ['1', '2', '3', '4', '5']

a = Layer(window, canvas, layer, args)
a.init_layer()

window.resizable(False, False)
window.mainloop()
