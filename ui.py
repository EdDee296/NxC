from tkinter import *
from tkinter import filedialog
from main import *


data_path = ""  # Global variable to store the selected file path
logs_path = ""  # Global variable to store
image_exts = ['jpeg', 'jpg', 'bmp', 'png']

def openFile(window, type, mes_label):
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

def of(window, type, btn, label):
    global data_path, logs_path
    openFile(window, type, label)
    if data_path != "" or logs_path != "":
        def rm(btn1, btn2):
            btn1.pack_forget()
            btn2.pack_forget()
        btn1 = Button(text="OK",
                      command=lambda: rm(btn1, btn))
        btn1.place(x=100, y=80)
        btn1.pack()

def check_memory_limit(var, label):
        if var.get():
            limit()
            label.pack()
        else:
            if label.winfo_ismapped():
                label.pack_forget()

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

    hist = trainModel(model, train, val)
    evaluate(model, test)
    saveModel(model)

def main():
    global data_path, logs_path, image_exts
    window = Tk()
    window.geometry("800x600")
    # Create a Text widget
    ins = Label(window, text=f"Please enter your data path\nNote: This should be a directory containing different folders for different classes.")
    ins.pack()

    label = Label(window, text="Memory usage is limited.")
    mes_label = Label(window, text="Please select a valid directory. ❌")

    btn1 = Button(text="Data",
                  command=lambda: of(window, 'data', btn1, mes_label))
    btn1.place(x=100, y=50)
    btn1.pack()

    btn2 = Button(text="Logs",
                  command=lambda: of(window, 'logs', btn2, mes_label))
    btn2.place(x=100, y=60)
    btn2.pack()

    var = BooleanVar()

    # Create the checkbox
    checkbox = Checkbutton(window, text="Limit memory growth", variable=var, command=lambda: check_memory_limit(var, label))
    checkbox.pack()



    window.mainloop()
    
    
if __name__ == "__main__":
    main()