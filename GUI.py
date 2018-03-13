import tkinter as tk
from tkinter.filedialog import askopenfilename
import Image, ImageTk
import os
import Tomograf
import numpy as np
from pylab import *
def main():

    def buttonWykonaj():
        print("Kliknalem wykonaj")

        alfaAngle=e.get()
        print("kat alfa: " + alfaAngle)
        numDetector = e2.get()
        print("liczba detektorow " + numDetector)
        fiAngle = e3.get()
        print("liczba detektorow " + fiAngle)
        iteration = e4.get()
        print("liczba detektorow " + iteration)

        print("czy uzywac filtru " + str(CheckVar1.get()))



        Tomograf.main(alfaAngle, numDetector ,fiAngle,CheckVar1.get(), iteration)

    def fileNames():

        # otwieranie sciezki
        filename = askopenfilename()
        print(filename)

    #window
    root = tk.Tk()
    root.title("TOMOGRAF")
    root.resizable(width=False, height=False)

    # set the root window's height, width and x,y position
    # x and y are the coordinates of the upper left corner
    w = 300
    h = 200
    x = 50
    y = 50
    # use width x height + x_offset + y_offset (no spaces!)
    root.geometry("%dx%d+%d+%d" % (1200, 700, x, y))
    # use a colorful frame
    frame = tk.Frame(root, bg='grey')
    frame.pack(fill='both', expand='yes')


    # position a label on the frame using place(x, y)
    # place(x=0, y=0) would be the upper left frame corner
    #picture location
    lb = tk.Label(frame, text="Wybierz plik do operacji :" , bg='grey')
    lb.place(x=20, y=30)

    butFile = tk.Button(frame, text=" WYBIERZ PLIK ", bg='yellow', command=fileNames)
    butFile.place(x=20, y=60)

    #Angle Alpha
    lb = tk.Label(frame, text="Podaj kat rotacji alfa :" , bg='grey')
    lb.place(x=20, y=130)
    e = tk.Entry(root)
    e.place(x=20 , y=155)
    e.focus_set()

    #numberOfDetectors
    lb2 = tk.Label(frame, text="Podaj liczbe detektorow  :", bg='grey')
    lb2.place(x=20, y=190)
    e2 = tk.Entry(root)
    e2.place(x=20 , y=215)
    e2.focus_set()

    #Angle FI
    lb3 = tk.Label(frame, text="Podaj kat (fi) :", bg='grey')
    lb3.place(x=20, y=250)
    e3 = tk.Entry(root)
    e3.place(x=20 , y=275)
    e3.focus_set()

    #save (co ile iteracji)
    lb4 = tk.Label(frame, text="Co ile iteracji zapisac  :", bg='grey')
    lb4.place(x=20, y=310)
    e4 = tk.Entry(root)
    e4.place(x=20 , y=335)
    e4.focus_set()

    #use filtering
    CheckVar1 = tk.IntVar()
    C1 = tk.Checkbutton( text = "Filtr", variable = CheckVar1,  onvalue = 1, offvalue = 0, height=2,  width = 5, bg='grey')
    C1.place(x=20,y=370)


    # put the button below the label, change y coordinate
    but = tk.Button(frame, text=" WYKONAJ ", bg='yellow', command=buttonWykonaj)
    but.place(x=20, y=430)

    #button w lewo
    but1 = tk.Button(frame, text="POPRZEDNI", bg='yellow')
    but1.place(x=300, y=30)

    #buttin w prawo
    but2 = tk.Button(frame, text="NASTEPNY", bg='yellow')
    but2.place(x=400, y=30)





    #plik w labelu
    #im = Image.open('./Zdjecia-przyklad/Kwadraty2.jpg').convert2byte()
    #tkimage = ImageTk.PhotoImage(im)
    #tk.Label(frame, image=tkimage).pack()

    #dzialajacy plik w labelu
    #image = Image.open("./Zdjecia-przyklad/Kwadraty2.jpg")
    #photo = ImageTk.PhotoImage(image)
    #label = tk.Label(image=photo)
    #label.image = photo # keep a reference!
    #label.pack()

    root.mainloop()


if __name__ == "__main__":
    main()


