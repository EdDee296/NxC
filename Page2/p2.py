from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Radiobutton, IntVar, StringVar, ttk
import random
import inspect  
import sys
sys.path.append('C:/Users/ASUS/OneDrive/New folder/New folder')
from main import *
import json


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\Downloads\Tkinter-Designer-master\Tkinter-Designer-master\Page2\assets\frame0")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# pos is [x,y]
def increment_pos(pos: list, x: int):
    pos[1] += x
    return pos
def decrement_pos(pos: list, x: int):
    pos[1] -= x
    return pos


# Read data from the file
with open("data.json", "r") as f:
    database = json.load(f)

init_pos = {'button_add_layer': [119.0, 341.0],  
            'add_arg': [240, 341], 
            'button_ok': [330, 380],
            'index': [70.0, 269.0],
            'equal': [180.0, 304.0],
            'layer_combobox': [133.0, 273.0],
            'arg_combobox': [125.0, 304.0],
            'textbox': [250.0, 310.0]}
increase = 70

image_exts = ['jpeg', 'jpg', 'bmp', 'png']

class Layer():
    def __init__(self, window: Tk, canvas: Canvas):
        self.window = window
        self.canvas = canvas
        self.layer = ['Conv2D', 'MaxPooling2D', 'Dense', 'Flatten', '']
        self.args = []
        self.index = 0
        self.last_y = init_pos['layer_combobox'][1]  # Keep track of the y-coordinate of the last widget
        self.images = []
        self.layer_id = []

        self.layer_widgets = []
        self.arg_widgets = []
        self.textbox_widgets = []

        self.layer_names = {}
        self.arg_names = {}
        
        self.layer_widget_keys = {}  # Keeps track of the current keys in self.data
        self.arg_widget_keys = {}  # Keeps track of the current keys in the inner dictionaries

        self.model = None

        self.data = {}
        self.add_layer_btn = self.create_button("button_2.png", init_pos["button_add_layer"], 84.0, 17.0, self.init_layer)
        self.ok_btn = self.create_button("button_1.png", init_pos["button_ok"], 104, 37, self.print_model)  
        self.add_arg_btn = self.create_button("button_4.png", init_pos['add_arg'], 76.0, 13.0, self.add_arg)

    def init_layer(self):
        self.create_layer_name(init_pos['index'], init_pos['layer_combobox'])
        
        self.last_y += increase  # Update the y-coordinate of the last widget
        increment_pos(init_pos['layer_combobox'], increase)
        increment_pos(init_pos['arg_combobox'], increase)
        increment_pos(init_pos['textbox'], increase)
        increment_pos(init_pos['index'], increase)
        increment_pos(init_pos['equal'], increase)
        self.reposition_widgets()

    def create_argument(self, arg_pos: list, equal_pos: list, textbox_pos: list):
        arg_var = StringVar()
        arg_var.trace_add("write", lambda *argu: self.update_name(self.arg_names, arg, arg_var.get()))

        arg = ttk.Combobox(self.window, values=self.args, width=7, textvariable=arg_var, state="readonly")
        self.arg_widgets.append(arg)
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
            bd=1,
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
        
        self.last_y += increase  # Update the y-coordinate of the last widget
        increment_pos(init_pos['layer_combobox'], increase)
        increment_pos(init_pos['arg_combobox'], increase)
        increment_pos(init_pos['textbox'], increase)
        increment_pos(init_pos['index'], increase)
        increment_pos(init_pos['equal'], increase)
        
        return arg, textbox, equal
        
    def add_arg(self):
        arg, textbox, equal = self.create_argument(init_pos['arg_combobox'], init_pos['equal'], init_pos['textbox'])
        self.textbox_widgets.append((self.layer_widgets[-1], arg, textbox))  # Store the layer widget along with the argument widget and textbox
        self.reposition_widgets()

    def save_values(self):
        for layer_widget in self.layer_widgets:
            new_layer_name = layer_widget.get()
            old_layer_name = self.layer_widget_keys.get(layer_widget)

            # If the layer name already exists, add a number to the end
            original_layer_name = new_layer_name
            i = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '|', '\\', ';', ':', "'", '"', ',', '.', '<', '>', '/', '?']

            while new_layer_name in self.data and new_layer_name != old_layer_name:
                if not new_layer_name[len(new_layer_name) - 1] in i:
                    new_layer_name = original_layer_name + random.choice(i)


            if old_layer_name is not None and old_layer_name in self.data:
                self.data[new_layer_name] = self.data.pop(old_layer_name)
            elif new_layer_name not in self.data:
                self.data[new_layer_name] = {}

            for layer_widget_arg, arg_widget, textbox in self.textbox_widgets:
                if layer_widget_arg != layer_widget:  # Skip if the argument doesn't belong to the current layer
                    continue

                new_arg_name = arg_widget.get()
                old_arg_name = self.arg_widget_keys.get(arg_widget)
                textbox_value = textbox.get()

                if textbox_value.strip() == '':
                    continue  # Ignore empty textboxes

                if old_arg_name is not None and old_arg_name in self.data[new_layer_name]:
                    self.data[new_layer_name][new_arg_name] = self.data[new_layer_name].pop(old_arg_name)

                self.data[new_layer_name][new_arg_name] = textbox_value  # Update the value every time

                self.arg_widget_keys[arg_widget] = new_arg_name

            self.layer_widget_keys[layer_widget] = new_layer_name

        print("layers: ", self.data, '\n')
        print_selection()
    
    def get_args(self, layer_name):
        self.args = list(inspect.signature(globals()[layer_name]).parameters.keys())[:-1]
        self.args.append(" ")

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
        layer = ttk.Combobox(self.window, values=self.layer, width=10, textvariable=layer_var, state="readonly")
        layer.bind("<<ComboboxSelected>>", lambda event: self.get_args(layer_var.get()))  # Update the argument list when a layer is selected  # Use after_idle to call get_args
        self.layer_widgets.append(layer)
        self.canvas.create_window(
            layer_pos[0],
            layer_pos[1],
            window=layer
        )
        return layer, index

    def reposition_widgets(self):
        # Reposition all widgets based on the y-coordinate of the last widget
        self.canvas.coords(self.add_layer_btn, init_pos['button_add_layer'][0] + 15, self.last_y)
        self.canvas.coords(self.ok_btn, init_pos["button_ok"][0], self.last_y + 50)
        self.canvas.coords(self.add_arg_btn, init_pos["add_arg"][0], self.last_y)

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

    def update_name(self, dict, widget, name):
        dict[widget.current()] = name
    
    def create_model_from_dict(self, layers):
        model = Sequential()
        for layer_name, args in layers.items():
            # Remove any special characters from the layer name
            clean_layer_name = ''.join(e for e in layer_name if e.isalnum())
            # Get the layer class from globals
            LayerClass = globals()[clean_layer_name]
            # Convert string values in args to actual values
            for arg, value in args.items():
                if value.isdigit():
                    args[arg] = int(value)
                elif value.startswith('(') and value.endswith(')'):
                    args[arg] = tuple(map(int, value[1:-1].split(',')))
            # Add the layer to the model
            model.add(LayerClass(**args))
        model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])
        return model
    
    def print_model(self):
        self.save_values()
        self.model = self.create_model_from_dict(self.data)
        self.model.summary()
        hist = trainModel(a.model, train, val, database['logs_path'])
        evaluate(self.model, test)
        self.model.save(os.path.join('models', database['name']+'.h5'))

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

if lim != 0:
    limit()

try:
    checkImg(database['data_path'], image_exts)
except Exception as e: # Catch any exception
    print("Invalid dir: ", database['data_path'])
batch = getBatch(database['data_path'])[0]
data = getBatch(database['data_path'])[1]
scaled_data = scale(data)

train = splitData(scaled_data)[0]
val = splitData(scaled_data)[1]
test = splitData(scaled_data)[2]

a = Layer(window, canvas)
a.init_layer()


window.resizable(False, False)
window.mainloop()
