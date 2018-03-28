from pylab import *
from skimage import  io
import numpy as np
import copy


#funkcja normalizujaca, przesuwa minimalny lub maksumalny element na kolor 0 po czy wszystkie elementy dzieli przez maksymalna wartosc
def normalize(image): 
    maxx = -1000000.0
    minn = 100000.0
    for i in range(len(image)):
        for j in range(len(image[0])):
            if (image[i][j] > maxx):
                maxx = image[i][j]
            if (image[i][j] < minn):
                minn = image[i][j]

    for i in range(len(image)):
        for j in range(len(image[0])):
            image[i][j] = (image[i][j] - minn) / (maxx - minn)

    return image

#funkcja realizujaca algorytm brezenhama, zlicza wartosci pikseli nalinii emiter-detektor
def line(x0,y0, x1,y1 ,imageX, imageY): 
    wyn=[]
    dx = x1-x0
    dy = y1-y0

    def sign(x):
        if x >= 0: return +1
        else:      return -1

    inc_x = sign(dx) # uwzględnienie znaków dx
    inc_y = sign(dy) # i dy

    dx = abs(dx)     # teraz odcinek został "przeniesiony"
    dy = abs(dy)     # do właściwego oktantu

    if dx >= dy:     # dy/dx <= 1 -- odcinek leży w "niebieskim" oktancie

        d       = 2*dy - dx
        delta_A = 2*dy
        delta_B = 2*dy - 2*dx

        x, y = (0, 0)
        for i in range(int(dx+1)):
            if((x0+x)<=imageX and (y0+y)<=imageY):
                wyn.append([x0+x, y0+y])
            if d > 0:
                d += delta_B
                x += inc_x
                y += inc_y
            else:
                d += delta_A
                x += inc_x

    else:            # dy/dx > 1 -- odcinek leży w "czerwonym" oktancie
                     # proszę zwrócić uwagę na wspomnianą zamianę znaczenia zmiennych
        d   = 2*dx - dy
        delta_A = 2*dx
        delta_B = 2*dx - 2*dy

        x, y = (0, 0)
        for i in range(dy+1):
            if ((x0 + x )<= imageX and (y0 + y )<= imageY):
                wyn.append([x0+x, y0+y])
            if d > 0:
                d += delta_B
                x += inc_x
                y += inc_y
            else:
                d += delta_A
                y += inc_y

    return wyn


#funkcja dodajaca do obrazu wynikowego (na podstawie algorytmu brezen-hana) wartosci z sinoogramu odczytane przez poszczegolny detektor
def lineReverse(x0,y0, x1,y1 ,imageX, imageY, detValue, sinogramReverse, ii,jj, iterr,name): 
    dx = x1-x0
    dy = y1-y0
    def sign(x):
        if x >= 0: return +1
        else:      return -1

    inc_x = sign(dx) # uwzględnienie znaków dx
    inc_y = sign(dy) # i dy

    dx = abs(dx)     # teraz odcinek został "przeniesiony"
    dy = abs(dy)     # do właściwego oktantu

    if dx >= dy:     # dy/dx <= 1 -- odcinek leży w "niebieskim" oktancie

        d       = 2*dy - dx
        delta_A = 2*dy
        delta_B = 2*dy - 2*dx

        x, y = (0, 0)
        for i in range(int(dx+1)):
            if((x0+x)<imageX-1 and (y0+y)<imageY-1):
                sinogramReverse[y0 + y,x0 + x ] = (sinogramReverse[y0 + y,x0 + x ] + detValue)

            if d > 0:
                d += delta_B
                x += inc_x
                y += inc_y
            else:
                d += delta_A
                x += inc_x

    else:            # dy/dx > 1 -- odcinek leży w "czerwonym" oktancie
                     # proszę zwrócić uwagę na wspomnianą zamianę znaczenia zmiennych
        d   = 2*dx - dy
        delta_A = 2*dx
        delta_B = 2*dx - 2*dy

        x, y = (0, 0)
        for i in range(dy+1):
            if ((x0 + x )< imageX-1 and (y0 + y )< imageY-1):
                sinogramReverse[y0 + y,x0 + x ] = (sinogramReverse[ y0 + y,x0 + x ] + detValue)

            if d > 0:
                d += delta_B
                x += inc_x
                y += inc_y
            else:
                d += delta_A
                y += inc_y

    if (ii % iterr == 0 and jj == 0):
        wyn = []
        wynTmp = []

        for i in range(len(sinogramReverse)):
            for j in range(len(sinogramReverse[0])):
                wynTmp.append(sinogramReverse[i][j])
            wyn.append(wynTmp)
            wynTmp = []

        wyn=normalize(wyn)
        io.imsave('./STEP/sinogramStep_' + str(ii) +'_'+ str(name)  + '.jpg', wyn)
        print("Zapisalem " , ii)

#funkcja realizujace zliczanie sredniej kolorow znajdujacych sie na linii dla danego ukladu emiter-detektor		
def countLinePixel(x0,y0, x1,y1,image): 
    sum=0.0
    x=0.0
    array=line(x0,y0, x1,y1,len(image[0]),len(image) )
    for i in array:
        sum=sum+image[int(i[1]),int(i[0])]
        x=x+1.0

    return sum/x


#na podstawie tablicy detektorow i emiterow tworzy sinogram	
def makeSinogram(detectorsList, emitersList, detectorsNumber, numberOfRotations, image, high, isFilter):
    sinogram=np.zeros((numberOfRotations,detectorsNumber))

    for j in range(0,int(detectorsNumber)-1):
        for i in range(0,int(numberOfRotations)-1):
            temp = countLinePixel(emitersList[i][0], emitersList[i][1], detectorsList[i][j][0], detectorsList[i][j][1], image) #temp jest to zmienna przechowujaca jeden element sinogramu (wartosc jednego piksela) dla jednego detektora
            sinogram[i][j]=temp
    if(isFilter==1): #sprawdzanie czy sinogram ma zostac przefiltrowany czy nie
        sinogram2 = ramLakFilter(sinogram)
    else:
        sinogram2=sinogram

    return sinogram2

#funkcja filtrujaca sinogram, tworzy maske i nastepnie filtruje sinogram i go zwraca	
def ramLakFilter(image): 

    x=2*int(len(image[0])/40)+1 #wiec zawsze nieparzysty, filtr ma dlugosc 1/20 dlugosci sinogramu
    center=int(x/2)
    filter=np.zeros(x)
    con=(-4/(pi*pi)) #constans
    index =0
    for i in range(-center,center+1,1):
        if(i%2==0):
            filter[index]=0
        if(i%2==1):
            filter[index] = (con/(i*i))
        if (i==0):
            filter[index] = 1
        index+=1

    arr = np.zeros_like(image)

    pad_array = np.zeros(center)
    for counter, element in enumerate(image): #realizacja splotu
        for i in range(arr.shape[1]):
            arr[counter][i] = np.sum(np.concatenate([pad_array, element, pad_array])[i:i + x] * filter)

    return arr


#funkcja tworzaca oraz wynikowy
def makeSinogramReverse(sinogram, numberOfDet, numberOfRotation, detectorsList, emitersList, image, sinogramReverse, iterr,name): 
    x = len(image[0])-2
    y = len(image)-2

    for i in range(numberOfRotation):
        for j in range(numberOfDet):
            lineReverse(emitersList[i][0], emitersList[i][1], detectorsList[i][j][0], detectorsList[i][j][1],x, y, sinogram[i][j], sinogramReverse ,i,j, iterr,name)

    sinogramReverse=normalize(sinogramReverse)


#tworzy tablice 2d detektorow. kazdy wiersz tablicy odpowiada detektorom w jednej iteracji programu, po obrocie o kat alfa zapisywany jest kolejny wiersz itd	
def makeDetectorsArray(numberOfDet, fi, systemRotationAngleAlfa, r,centerX, centerY, numberofRotation): 
    array=[]
    arrayTemp=[]
    point = []
    r=r-2
    alfa = radians(0.0)
    for i in range(numberofRotation):
        point.append(int( r* cos(alfa + pi - fi/2)+ centerX)) #x
        point.append(int( r* sin(alfa + pi - fi/2)+ centerY) )#y
        arrayTemp.append(point)
        point=[]

        for i in range(1, numberOfDet):
            point.append (int( r*cos(alfa + pi - fi/2 + i*(fi/(numberOfDet-1)) )+ centerX) )#X
            point.append( int( r*sin(alfa + pi - fi/2 + i*(fi/(numberOfDet-1)) )+ centerY) )#Y
            arrayTemp.append(point)
            point=[]

        point.append(int( r * cos(alfa + pi + fi / 2 )+ centerX))
        point.append(int( r * sin(alfa + pi + fi / 2 )+ centerY))
        arrayTemp.append(point)
        point=[]

        array.append(arrayTemp)
        arrayTemp=[]
        alfa = alfa + systemRotationAngleAlfa

    return array


#podobnie jak w przypadku funkcjitworzacej tablice detektorow, ta funkcja tworzy tablice emiterow	
def makeEmitersArray(numberOfRotation,r,centerX, centerY, systemRotationAngleAlfa): 
    array = []
    point = []
    r=r-2
    alfa=radians(0.0)
    for i in range(numberOfRotation):
        point.append( int(r*cos(alfa) + centerX))
        point.append( int(r*sin(alfa)+ centerY))
        array.append(point)
        alfa=alfa+systemRotationAngleAlfa
        point=[]

    return array


#liczy blad sredniokwadratowy pomiedzy dwoma obrazkami. Liczy go tylko w obsarze wewnatrz kola tworzonegoprzez detektory
def meanSquaredError(oryginal, image, r): 
    image = np.array(image)
    oryginal = np.array(oryginal)
    x = len(image[0])
    y = len(image)
    print("X: ", x, "Y: ", y)
    delX = int((x - r * sqrt(2)) / 2)
    delY = int((y - r * sqrt(2)) / 2)
    delPomX = int(r * sqrt(2))
    image = image[:, delX:]
    image = image[:, :delPomX]
    image = image[delY:, :]
    image = image[:delPomX, :]

    oryginal = oryginal[:, delX:]
    oryginal = oryginal[:, :delPomX]
    oryginal = oryginal[delY:, :]
    oryginal = oryginal[:delPomX, :]

    print("X: ", len(image[0]), "Y: ", len(oryginal))



    return np.power(np.subtract(oryginal, image),2).mean() ** 0.5

def main(rotationAngle,numberOfDet,angleFi,usefiltr,freq,file):

    #------ VARIABLES -----
    # casting input parametres
    systemRotationAngleAlfa = radians(float(rotationAngle))  # in degrees
    numberOfDet = int(numberOfDet)
    fi1 = int(angleFi)
    fi = radians(fi1)  # rozpietosc ukladu
    isFilter = int(usefiltr)
    freqOfSave = int(freq)
    if (isFilter):
        nameFiltr='FILTR_'
    else:
        nameFiltr ='BEZ_FILTRA_'

    image = io.imread(file, flatten=True)

    #size of picture
    x=len(image[0])
    y=len(image)
    print("Rozmiar obrazka " + file + " wynosi : ", x, y)

    pom=file.split("/")
    file=pom[len(pom)-1]

    #center of picture
    centerX=x/2
    centerY=y/2
    #radius
    if(y<=x):
        r=y/2
    else:
        r=x/2

    r=r-2
    numberOfRotations = int(radians(360.0)/systemRotationAngleAlfa)
    arrayOfDetectors = makeDetectorsArray(numberOfDet, fi, systemRotationAngleAlfa, r,centerX, centerY, numberOfRotations)
    arrayOfEmiter = makeEmitersArray(numberOfRotations,r,centerX, centerY, systemRotationAngleAlfa)
    high=y
    sinogram = makeSinogram(arrayOfDetectors, arrayOfEmiter, numberOfDet, numberOfRotations, image, high,isFilter )

    #file name to make sinogram reverse step by step
    named=file.split(".")
    name=named[0]+'_'+nameFiltr

    newSinogram = copy.copy(sinogram)
    sinogramSave = normalize(newSinogram)
    io.imsave('./Sinograms/sinogram_'+nameFiltr+file, sinogramSave)
    print("Sinogram saved : " + file)

    sinogramReverse = np.zeros((y, x))
    makeSinogramReverse(sinogram, numberOfDet, numberOfRotations, arrayOfDetectors, arrayOfEmiter, image, sinogramReverse, freqOfSave,name)
    io.imsave('./Results/sinogramReverse_'+ nameFiltr + file, sinogramReverse)
    print('Sinogram reverse saved ' +file)

    err=meanSquaredError(image, sinogramReverse,r)
    print("Blad sredniokwadratowy = " , err)
    print("END !!! ")
    return err






