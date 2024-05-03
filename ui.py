from tkinter import *
from tkinter import filedialog
from main import *
import sys

data_path = ""  # Global variable to store the selected file path
logs_path = ""  # Global variable to store
image_exts = ['jpeg', 'jpg', 'bmp', 'png']

def remove_all_widgets(window):
    # Get a list of all widgets in the window
    widgets = window.winfo_children()
    
    # Destroy each widget in the list
    for widget in widgets:
        widget.destroy()

def openFile(window, type):
    if type == "data":
        global data_path  # Use the global keyword to modify the global variable
        pack = 0
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
                    label = Label(window, text=f"Make sure there are only different folders for different classes in your data directory. Please select again. ❌\n")
                    label.pack()
                    pack = 1
                    break
                else:
                    files = os.listdir(full_path)
                    for file in files:
                        file_path = os.path.join(full_path, file)
                        if os.path.isdir(file_path):
                            subdirectories.append(file)

            if subdirectories:
                if pack == 0:
                    label_subdirs = Label(window, text=f"There exists subfolder(s) in your classes folder. Please select again. ❌\n {subdirectories}")
                    label_subdirs.pack()
            else:
                if pack == 0:
                    label_success = Label(window, text=f"Data Path Selected: {data_path} ✅")
                    label_success.pack()
                    check_box(window, data_path)

        else:
            label = Label(window, text=f"Empty directory. Please select a valid directory. ❌")
            label.pack()
    else:
        global logs_path
        logs_path = filedialog.askdirectory()
        logs_path = logs_path.replace('/', '\\')
        if os.path.isdir(logs_path):
            label = Label(window, text=f"Logs Path Selected: {logs_path} ✅")
            label.pack()
        else:
            label = Label(window, text=f"This is not a valid directory for logs. Please select a valid directory. ❌")
            label.pack()

def ok(window):
    remove_all_widgets(window)

def ofdata(window, type, btn):
    global data_path, logs_path
    change_data_btn = Button(text="Change Data Path",
                             command=lambda: ofdata(window, type, btn))

    okbtn = Button(text="OK",
                   command=lambda: ok(window))
    openFile(window, type)
    if data_path != "":
        btn.pack_forget()
        if not change_data_btn.winfo_ismapped():
            change_data_btn.place(x=100, y=50)
            change_data_btn.pack()
    if data_path != "" and logs_path != "":
        okbtn.place(x=100, y=80)
        okbtn.pack()

def oflogs(window, type, btn):
    global data_path, logs_path
    change_logs_btn = Button(text="Change Logs Path",
                             command=lambda: oflogs(window, type, btn))
    okbtn = Button(text="OK",
                   command=lambda: ok(window))
    openFile(window, type)
    if logs_path != "":
        btn.pack_forget()
        if not change_logs_btn.winfo_ismapped():
            change_logs_btn.place(x=100, y=60)
            change_logs_btn.pack()
        
    if data_path != "" and logs_path != "":
        okbtn.place(x=100, y=80)
        okbtn.pack()
    

def check_memory_limit(var, label):
        if var.get():
            limit()
            label.pack()
        else:
            if label.winfo_ismapped():
                label.pack_forget()

def label_checking(var, canvas): 
    if var.get():
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        if canvas.get_tk_widget().winfo_ismapped():
            canvas.get_tk_widget().pack_forget()

def check_box(window, data_path):
    v = BooleanVar()
    if data_path != '':
        batch = getBatch(data_path)[0]
        figure = checkLabels(batch)
        canvas = FigureCanvasTkAgg(figure, master=window)
        plot_button = Checkbutton(window, text="Check the label of classes", variable=v, command=lambda: label_checking(v, canvas))
        plot_button.pack() 

def a():
    try:
        checkImg(data_path, image_exts)
    except Exception as e: # Catch any exception
        print("Invalid dir: ", data_path)
    batch = getBatch(data_path)[0]
    data = getBatch(data_path)[1]
    scaled_data = scale(data)

    train = splitData(scaled_data)[0]
    val = splitData(scaled_data)[1]
    test = splitData(scaled_data)[2]

    model = createModel()

    hist = trainModel(model, train, val, logs_path)
    evaluate(model, test)
    saveModel(model)

def main():
    global data_path, logs_path, image_exts
    pack = 0

    window = Tk()
    window.geometry("800x600")

    def on_close():
        window.destroy()
        sys.exit()  # Exit the program when the window is closed

    window.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event

    # Create a Text widget
    ins = Label(window, text=f"Please enter your data path\nNote: This should be a directory containing different folders for different classes.")
    ins.pack()

    label = Label(window, text="Memory usage is limited.")

    btn1 = Button(text="Data",
                  command=lambda: ofdata(window, 'data', btn1))
    btn1.place(x=100, y=50)
    btn1.pack()

    btn2 = Button(text="Logs",
                  command=lambda: oflogs(window, 'logs', btn2))
    btn2.place(x=100, y=60)
    btn2.pack()

    var = BooleanVar()
    checkbox = Checkbutton(window, text="Limit memory growth", variable=var, command=lambda: check_memory_limit(var, label))
    checkbox.pack()


    

    window.mainloop()
    
    
if __name__ == "__main__":
    main()