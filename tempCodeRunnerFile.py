# exercise: 
# create a horizontal scrollbar at the bottom and use it to scroll the canvas left and right
scrollbar_bottom = ttk.Scrollbar(window, orient = 'horizontal', command = canvas.xview)
canvas.configure(xscrollcommand = scrollbar_bottom.set)
scrollbar_bottom.place(relx = 0, rely = 1, relwidth = 1, anchor = 'sw')
# also add an event to scroll left / right on Ctrl + mousewheel 
canvas.bind('<Control MouseWheel>', lambda event: canvas.xview_scroll(-int(event.delta / 60), "units"))