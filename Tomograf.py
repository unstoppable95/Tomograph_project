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

def countLinePixel(x0,y0, x1,y1,image):
    sum=0.0
    x=0.0

    array=line(x0,y0, x1,y1,len(image[0]),len(image) )

    for i in array:
        #print(int(i[0]),int(i[1]))
        sum=sum+image[int(i[1]),int(i[0])]
        x=x+1.0

    return sum/x


def makeSinogram(detectorsList, emitersList, detectorsNumber, numberOfRotations, image, high):
    sinogram=np.zeros((numberOfRotations,detectorsNumber))

    for j in range(0,int(detectorsNumber)-1):
        for i in range(0,int(numberOfRotations)-1):
            temp = countLinePixel(emitersList[i][0], emitersList[i][1], detectorsList[i][j][0], detectorsList[i][j][1], image)
            sinogram[i][j]=temp

    return sinogram

def makeDetectorsArray(numberOfDet, fi, systemRotationAngleAlfa, r,centerX, centerY, numberofRotation):
    array=[]
    arrayTemp=[]
    point = []
    r=r-1
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
    r=r-1
    alfa=radians(0.0)
    for i in range(numberOfRotation):
        point.append( int(r*cos(alfa) + centerX))
        point.append( int(r*sin(alfa)+ centerY))
        array.append(point)
        alfa=alfa+systemRotationAngleAlfa
        point=[]

    return array

def main():

    fileNames=getFileNames()

    for i in fileNames:


        systemRotationAngleAlfa = radians(2.0)  # in degrees
        numberOfDet = 100
        fi = radians(270)  # rozpietosc ukladu
        image = io.imread('./Zdjecia-przyklad/'+i, flatten=True)

        #size of picture
        x=len(image[0])
        y=len(image)
        print("Rozmiar obrazka" + i + " wynosi : ", x, y)

        #center of picture
        centerX=x/2
        centerY=y/2

        #radius
        if(y<=x):
            r=y/2
        else:
            r=x/2

        numberOfRotations = int(radians(360.0)/systemRotationAngleAlfa)
        arrayOfDetectors = makeDetectorsArray(numberOfDet, fi, systemRotationAngleAlfa, r,centerX, centerY, numberOfRotations)


        arrayOfEmiter = makeEmitersArray(numberOfRotations,r,centerX, centerY, systemRotationAngleAlfa)
        high=y
        sinogram = makeSinogram(arrayOfDetectors, arrayOfEmiter, numberOfDet, numberOfRotations, image, high)

        io.imsave('./sinogram_'+i, sinogram)

        print("END : " + i)

def getFileNames():
    file_names = []
    os.chdir('./Zdjecia-przyklad')
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".jpg"):
            name = os.path.join(cwd, file)
            file_names.append(file)


    os.chdir('../')
    os.getcwd()
    return file_names



if __name__ == '__main__':
    main()