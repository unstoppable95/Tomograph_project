import tkinter as tk




#window
root = tk.Tk()
root.title("TOMOGRAF")
root.resizable(width=False, height=False)

# set the root window's height, width and x,y position
# x and y are the coordinates of the upper left corner
w = 300
h = 200
x = 50
y = 100
# use width x height + x_offset + y_offset (no spaces!)
root.geometry("%dx%d+%d+%d" % (1300, 800, x, y))
# use a colorful frame
frame = tk.Frame(root, bg='grey')
frame.pack(fill='both', expand='yes')
# position a label on the frame using place(x, y)
# place(x=0, y=0) would be the upper left frame corner
label = tk.Label(frame, text="Podaj ilosc katow")
label.place(x=20, y=30)
# put the button below the label, change y coordinate
button = tk.Button(frame, text="Oblicz", bg='yellow')
button.place(x=20, y=60)


e = tk.Entry(root)
e.place(x=50 , y= 300)
e.focus_set()




root.mainloop()


#frame = Frame(root )
#frame.grid()

#f2=Frame(root,width=1300,height=800)
#f2.grid()

#button = Button(frame,text="Haha",background="red")
#button.grid(row=700, column=80, columnspan=2)



#root.mainloop()


