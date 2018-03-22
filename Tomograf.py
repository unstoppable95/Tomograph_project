import cv2
from skimage import feature, data, color, measure
from skimage.filters.edges import convolve
from pylab import *
import skimage as ski
from skimage import data, io, filters, exposure
import numpy as np
from PIL import Image
import numpy as np
from scipy import ndimage
import skimage.morphology as mp
from skimage.filters.edges import convolve
from skimage import color,measure
import colorsys as cs
from matplotlib import pylab as plt
from skimage import img_as_ubyte
from skimage import data
import os
from math import ceil
from subprocess import call
import dicom
import os
import numpy
from matplotlib import pyplot, cm


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

def line(x0,y0, x1,y1 ,imageX, imageY):
    #print(imageX, imageY)
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



def lineReverse(x0,y0, x1,y1 ,imageX, imageY, image, detValue, sinogramReverse, ii,jj, iterr,name):
    #print(imageX, imageY)

    sum=0.0
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
        # wyn=sinogramReverse
        for i in range(len(sinogramReverse)):
            for j in range(len(sinogramReverse[0])):
                wynTmp.append(sinogramReverse[i][j])
            wyn.append(wynTmp)
            wynTmp = []

        '''
        #normalize and save step
        maxx = -1000000.0
        minn=100000.0
        for i in range(len(wyn)):
            for j in range(len(wyn[0])):
                if (wyn[i][j] > maxx):
                    maxx = wyn[i][j]
                if(wyn[i][j] <minn):
                    minn=wyn[i][j]

        # normalizing
        for i in range(len(wyn)):
            for j in range(len(wyn[0])):
                wyn[i][j] = (wyn[i][j] - minn) / (maxx - minn)

        '''
        wyn=normalize(wyn)
        io.imsave('./STEP/sinogramStep_' + str(ii) +'_'+ str(name)  + '.jpg', wyn)
        print("Zapisalem " , ii)



def countLinePixel(x0,y0, x1,y1,image):
    sum=0.0
    x=0.0

    array=line(x0,y0, x1,y1,len(image[0]),len(image) )

    for i in array:
        #print(int(i[0]),int(i[1]))
        sum=sum+image[int(i[1]),int(i[0])]
        x=x+1.0

    return sum/x


def makeSinogram(detectorsList, emitersList, detectorsNumber, numberOfRotations, image, high, isFilter):
    sinogram=np.zeros((numberOfRotations,detectorsNumber))

    for j in range(0,int(detectorsNumber)-1):
        for i in range(0,int(numberOfRotations)-1):
            temp = countLinePixel(emitersList[i][0], emitersList[i][1], detectorsList[i][j][0], detectorsList[i][j][1], image)
            sinogram[i][j]=temp
    #sinogram2=sinogram
    if(isFilter==1):
        sinogram2 = ramLakFilter(sinogram)
    else:
        sinogram2=sinogram

    '''
    maxx = -100000.0
    minn=100000.0
    for i in range(len(sinogram2)):
        for j in range(len(sinogram2[0])):
            if (sinogram2[i][j] > maxx):
                maxx = sinogram2[i][j]
            if (sinogram2[i][j] < minn):
                minn = sinogram2[i][j]

    # normalizing
    for i in range(len(sinogram2)):
        for j in range(len(sinogram2[0])):
            sinogram2[i][j] = (sinogram2[i][j] -minn)/(maxx - minn)
    '''
    sinogram2=normalize(sinogram2) ############################################
    #io.imsave('./Po_filtrze4.jpg', sinogram2)
    return sinogram2


def convolve(array1, array2):
    wyn=[]
    for i in range(len(array1)):
        wyn.append(0)
        for j in range(len(array2)):
            wyn[i]=wyn[i]+array1[i-j]*array2[j]

    return wyn


def ramLakFilter(image):
    print("PRZED: ", len(image), " ", len(image[0]))
    #io.imsave('./Przedfiltrem.jpg',image)

    x=2*int(len(image[0])/8)+1 #wiec zawsze nieparzysty
    x=11
    center=int(x/2)
    print("x= ",x,"Center= ",center+1)

    filter=np.zeros(x)


    for i in range(x):
        if(i%2==0):
            filter[i]=0
        if(i%2==1):
            filter[i] = ((-4/(pi*pi))/(i*i))
        if (i == center):
            filter[i] = 1

    #check
    # arr2=np.zeros((len(image),len(image[0])+x-1))

    #uzupelnianie
    # for i in range(len(image)):
    #     for j in range(int(x/2),  len(image[0])+int(x/2)):
    #         arr2[i][j]=image[i][j-int(x/2)]

    '''
    for i in range(len(image)):
        for j in range(len(image[0])+x):
            for k in range(len(filter)):
                arr[i][j] += arr2[i][j - k] * filter[k]
    '''
    # pomm = normalize(arr2)
    # io.imsave('./Pommm.jpg', pomm)

    '''
    for i in range(len(image)):
        for j in range(int(x/2),   len(image[0]) ):
            for k in range(int(x)):
                arr[i][j] = arr[i][j] + (arr2[i][j-k] * filter[k])#+ (arr2[i][j+k] * filter[k])
    '''

    ##KRUSZYNOWY
    arr = np.zeros_like(image)
    #arr = np.zeros((len(image), len(image[0]) + x - 1))
    #out_sinogram =

    #half_filtr_len = len(filter) // 2
    padding = 2 * center + 1
    pad_array = np.zeros(center)
    for counter, element in enumerate(image):
        for i in range(image.shape[1]):
            arr[counter][i] = np.sum(np.concatenate([pad_array, element, pad_array])[i:i + x] * filter)

    #out_con_sin = list()
    #for ind_x, x in enumerate(image):
    #    out_convolve_line = np.convolve(x, filter, mode='same')
    #   out_con_sin.append(out_convolve_line)

    ##KRUSZYNOWY

    #xx=normalize(arr)
    #io.imsave('./Przed_obcinaniem.jpg', xx)

    #arr = arr[:, int(x/2):len(image[0])+int(x/2)]
    arr=normalize(arr)
    #arr=normalize(arr)
    #io.imsave('./Po_filtrze.jpg', arr)

    return arr

def makeSinogramReverse(sinogram, numberOfDet, numberOfRotation, detectorsList, emitersList, image, sinogramReverse, iterr,name):
    x = len(image[0])-2
    y = len(image)-2

    for i in range(numberOfRotation):
        for j in range(numberOfDet):
            lineReverse(emitersList[i][0], emitersList[i][1], detectorsList[i][j][0], detectorsList[i][j][1],x, y,image, sinogram[i][j], sinogramReverse ,i,j, iterr,name)


    #finding max pixel
    # maxx=-10000000.0
    # minn=100000.0
    # for i in range(len(sinogramReverse)):
    #     for j in range (len(sinogramReverse[0])):
    #         if(sinogramReverse[i][j] > maxx):
    #             maxx = sinogramReverse[i][j]
    #         if(sinogramReverse[i][j] < minn):
    #             minn = sinogramReverse[i][j]
    #
    # #normalizing
    # for i in range(len(sinogramReverse)):
    #     for j in range(len(sinogramReverse[0])):
    #         sinogramReverse[i][j] = (sinogramReverse[i][j] - minn) / (maxx - minn)

    sinogramReverse=normalize(sinogramReverse)



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

def meanSquaredError(oryginal, image):
    '''sum=0.0
    x=0
    for i in range(len(oryginal)):
        for j in range (len(oryginal[0])):
            z=oryginal[i][i]-image[i][j]
            sum=sum+(z*z)
            x=x+1

    return sum/x'''
    return np.power(np.subtract(oryginal, image),2).mean() ** 0.5

def main(rotationAngle,numberOfDet,angleFi,usefiltr,freq,file):


    #------ VARIABLES -----
    # casting input parametres
    #systemRotationAngleAlfa1 = float(rotationAngle)
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

    fileNames =file
    err=0
    for i in fileNames:

        image = io.imread(i, flatten=True)

        #size of picture
        x=len(image[0])
        y=len(image)
        print("Rozmiar obrazka " + i + " wynosi : ", x, y)

        pom=i.split("/")

        i=pom[len(pom)-1]

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
        named=i.split(".")
        name=named[0]+'_'+nameFiltr

        #sinogram3=normalize(sinogram)
        io.imsave('./Sinograms/sinogram_'+nameFiltr+i, sinogram)
        print("Sinogram saved : " + i)

        sinogramReverse = np.zeros((y, x))
        makeSinogramReverse(sinogram, numberOfDet, numberOfRotations, arrayOfDetectors, arrayOfEmiter, image, sinogramReverse, freqOfSave,name)

        io.imsave('./Results/sinogramReverse_'+ nameFiltr + i, sinogramReverse)
        print('Sinogram reverse saved ' +i)

        err=meanSquaredError(image, sinogramReverse)
        print("Blad sredniokwadratowy = " , err)
    print("END !!! ")
    return err



def getFileNames():
    file_names = []
    os.chdir('./Zdjecia-przyklad')
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".jpg"):
            name = os.path.join(cwd, file)
            file_names.append(file)
        if file.endswith(".JPG"):
            name = os.path.join(cwd, file)
            file_names.append(file)

    os.chdir('../')
    os.getcwd()
    return file_names



