from tkinter import *
from tkinter import filedialog
from main import *

data_path = ""  # Global variable to store the selected file path
logs_path = ""  # Global variable to store
image_exts = ['jpeg', 'jpg', 'bmp', 'png']

'''btn2 = Button(text="Open your logs path",
                command=lambda: openFile(window, 'logs'))
    btn2.place(x=200, y=100)
    btn2.pack()'''

def openFile(window, type):
    if type == "data":
        global data_path  # Use the global keyword to modify the global variable
        data_path = filedialog.askdirectory()
        data_path = data_path.replace('/', '\\')
        label = Label(window, text=f"Selected Data Path: {data_path}")
        label.pack()
    else:
        global logs_path
        logs_path = filedialog.askdirectory()
        logs_path = logs_path.replace('/', '\\')
        label = Label(window, text=f"Selected Logs Path: {logs_path}")
        label.pack()


def of(window, type, btn):
    global data_path, logs_path
    openFile(window, type)
    if data_path != "" or logs_path != "":
        def rm(btn1, btn2):
            btn1.pack_forget()
            btn2.pack_forget()
        btn1 = Button(text="OK",
                      command=lambda: rm(btn1, btn))
        btn1.place(x=100, y=80)
        btn1.pack()

def main():
    global data_path, logs_path, image_exts
    window = Tk()
    window.geometry("800x600")
    # Create a Text widget
    ins = Label(window, text=f"Please enter your data path\nNote: This should be a directory containing different folders for different classes.")
    ins.pack()

    photo = PhotoImage("i.png") 
    photoimage = photo.subsample(1, 1)
    btn1 = Button(text="Data",
                  image = photoimage, 
                  compound=LEFT,
                  command=lambda: of(window, 'data', btn1))
    btn1.place(x=100, y=50)
    btn1.pack(side=TOP)


    window.mainloop()
    limit()
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
    
if __name__ == "__main__":
    main()