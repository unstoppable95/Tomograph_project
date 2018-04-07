import tkinter as tk
from tkinter.filedialog import askopenfilename
import Image, ImageTk
import Tomograf
from pylab import *
import os

def main():

    # file to proceed
    fileName= ""

    # files to display ( steps )
    fileNamesDisp = []

    # main left - right
    idx = 0

    def printError(error):
        # Label5
        lb5 = tk.Label(frame, text=error, bg='grey')
        lb5.place(x=0.01*width, y=0.49*height)
        #
        lb5 = tk.Label(frame, text='Blad sredniokwadratowy: ', bg='grey')
        lb5.place(x=0.01*width, y=0.47*height)

    def setPhotoSinogramReverse(fileName):
        reverseName=fileName.split("_")
        path=[]
        if (CheckVar1.get()):
            nameFiltr = 'FILTR_'
        else:
            nameFiltr = 'BEZ_FILTRA_'

        findName='Reverse_'+nameFiltr+reverseName[0]
        for file in os.listdir('./Results/'):
            if findName in file:
                path.append(file)



        img2 = ImageTk.PhotoImage(Image.open('./Results/'+path[0]))
        label8.configure(image=img2)
        label8.image = img2

    def buttonWykonaj():


        alfaAngle=e.get()
        print("Kat alfa: " + alfaAngle)
        numDetector = e2.get()
        print("Liczba detektorow: " + numDetector)
        fiAngle = e3.get()
        print("Kat fi: " + fiAngle)
        iteration = e4.get()
        print("Co ile iteracji zapisac przebieg : " + iteration)
        print("Czy uzywac filtru: " + str(CheckVar1.get()))

        #image proceed
        pom1=Tomograf.main(alfaAngle, numDetector ,fiAngle,CheckVar1.get(), iteration,fileName)
        error= str(pom1)
        shortName=createShortcut()
        findFilesInto(shortName,int(iteration),alfaAngle)
        printError(error)
        setPhotoSinogramReverse(shortName)

        #zapis parametrow do pliku
        #nazwa_pliku  czyFiltr   ilosc_detektorow   kat_alfa   kat_fi   blad_sredniokwadratowy
        plik = open('./dane.txt', 'a+')
        plik.write(shortName+"\t"+numDetector+"\t"+alfaAngle+"\t"+fiAngle+"\t"+error+"\t"+str(CheckVar1.get())+"\n")
        plik.close()

    def createShortcut():
        # use shortcut for search
        if (CheckVar1.get()):
            nameFiltr = 'FILTR_'
        else:
            nameFiltr = 'BEZ_FILTRA_'

        toSplit = fileName.split("/")
        readyName = toSplit[len(toSplit) - 1]
        readyName1 = readyName.split(".")
        ready = readyName1[0]
        shortcut = ready + '_' + nameFiltr
        return shortcut

    def findFilesInto(name1,iterator1,x):
        i =0
        iterator = int(iterator1)
        z= int(int(360.0 /float( x))/iterator)
        for i in range (0,z*iterator,iterator):
            #print(i)
            name ='_'+ str(i) + '_' + name1
            for file in os.listdir('./STEP'):
                    if name in file:
                        fileNamesDisp.append(file)

    def fileNames():

        # otwieranie sciezki
        filename = askopenfilename()
        nonlocal fileName
        fileName=filename

    def callbackLEFT():
        nonlocal idx
        if(idx>0):
            idx-=1
        else:
            idx=0
        img2 = ImageTk.PhotoImage(Image.open("./STEP/"+ fileNamesDisp[idx]))
        label8.configure(image=img2)
        label8.image = img2

    def callbackRIGHT():
        nonlocal idx
        if (idx < len(fileNamesDisp)-1):
            idx += 1
        else:
            idx = len(fileNamesDisp)-1

        img2 = ImageTk.PhotoImage(Image.open("./STEP/"+fileNamesDisp[idx]))
        label8.configure(image=img2)
        label8.image = img2

    def callback():

        filename1 = askopenfilename()
        img2 = ImageTk.PhotoImage(Image.open(filename1))
        label8.configure(image=img2)
        label8.image = img2


    #window
    root = tk.Tk()
    root.title("TOMOGRAF")
    root.resizable(width=False, height=False)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

     #offset
    x = 20
    y = 20
    root.geometry("%dx%d+%d+%d" % (0.71*width, 0.81*height, x, y))
    frame = tk.Frame(root, bg='grey')
    frame.pack(fill='both', expand='yes')


    #labels , buttons
    #picture location
    lb = tk.Label(frame, text="Wybierz plik do operacji:" , bg='grey')
    lb.place(x=0.01*width, y=0.02*height)

    butFile = tk.Button(frame, text=" WYBIERZ PLIK ", bg='yellow', command=fileNames)
    butFile.place(x=0.01*width, y=0.05*height)

    #Angle Alpha
    lb = tk.Label(frame, text="Podaj kat rotacji alfa:" , bg='grey')
    lb.place(x=0.01*width, y=0.1*height)
    e = tk.Entry(root)
    e.place(x=0.01*width , y=0.13*height)
    e.focus_set()

    #numberOfDetectors
    lb2 = tk.Label(frame, text="Podaj liczbe detektorow:", bg='grey')
    lb2.place(x=0.01*width, y=0.16*height)
    e2 = tk.Entry(root)
    e2.place(x=0.01*width , y=0.19*height)
    e2.focus_set()

    #Angle FI
    lb3 = tk.Label(frame, text="Podaj kat (fi):", bg='grey')
    lb3.place(x=0.01*width, y=0.22*height)
    e3 = tk.Entry(root)
    e3.place(x=0.01*width , y=0.25*height)
    e3.focus_set()

    #save (co ile iteracji)
    lb4 = tk.Label(frame, text="Co ile iteracji zapisac:", bg='grey')
    lb4.place(x=0.01*width, y=0.28*height)
    e4 = tk.Entry(root)
    e4.place(x=0.01*width , y=0.31*height)
    e4.focus_set()

    #use filtering
    CheckVar1 = tk.IntVar()
    C1 = tk.Checkbutton( text = "Filtr", variable = CheckVar1,  onvalue = 1, offvalue = 0, height=2,  width = 5, bg='grey')
    C1.place(x=0.01*width,y=0.35*height)


    # put the button below the label, change y coordinate
    but = tk.Button(frame, text=" PRZETWORZ ", bg='yellow', command=buttonWykonaj)
    but.place(x=0.01*width, y=0.41*height)

    #button w lewo
    but1 = tk.Button(frame, text=" POPRZEDNIE", bg='yellow' , width=10 , height=2, command=callbackLEFT)
    but1.place(x=0.3*width, y=0.75*height)

    #buttin w prawo
    but2 = tk.Button(frame, text=" NASTEPNE", bg='yellow', width=10 , height=2 , command=callbackRIGHT)
    but2.place(x=0.45*width, y=0.75*height)

    #dowolny obrazek do wyswielenia
    lb5 = tk.Label(frame, text="Obrazek do wyświetlenia:", bg='grey')
    lb5.place(x=0.01*width, y=0.62*height)

    # buttion dowolny plik
    but3 = tk.Button(frame, text=" WYBIERZ OBRAZEK", bg='yellow', width=15, height=2, command=callback)
    but3.place(x=0.01*width, y=0.65*height)

    #wyswietlanie obrazu
    photo = ImageTk.PhotoImage(Image.open("./Zdjecia-przyklad/START.jpg"))
    label8 = tk.Label(image=photo , width=0.58*width , height=0.72*height , bg='black')
    label8.place(x=0.12*width, y=0.01*height)

    root.mainloop()


if __name__ == "__main__":
    main()


