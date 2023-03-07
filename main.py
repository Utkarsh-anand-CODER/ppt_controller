import os
import cv2
import numpy as np
from cvzone.HandTrackingModule import  HandDetector
# variable
width,height =1280,720
folderPath="ppt"
#camera setup
cap=cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
#get the list of presentation images
pathImages=sorted(os.listdir(folderPath))
#print(pathImages)
# variable
imgNumber=2
hs,ws=int(120*1),int(213*1)
gestureThreshold=300
buttonpressed=False
buttoncounter=0
buttondelay=30
annotations=[[]]
annotationnumber=0
annotationstart=False
#hand dector
detector=HandDetector(detectionCon=0.8,maxHands=1)
while True:
    #import  images
    success,img=cap.read()
    img =cv2.flip(img,1)
    pathfullimages=os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent=cv2.imread(pathfullimages)
    hands,img=detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)
    if hands and buttonpressed is False:
        hand=hands[0]
        fingers=detector.fingersUp(hand)
        cx, cy =  hand['center']
        lmList =  hand['lmList']

        #Constrain values for easier drawing

        #indexFinger=lmList[8][0],lmList[8][1]
        xVal=int(np.interp(lmList[8][0],[width//2,w],[0,width]))
        yVal=int(np.interp(lmList[8][1],[150,height-150],[0,height]))
        indexFinger=xVal,yVal
        if cy<=gestureThreshold:#if hand is at the height of the face
            annotationstart = False
            #gesture 1-left
            if fingers ==[1, 0, 0, 0, 0]:
                annotationstart = False
                print("Left")
                if imgNumber>0:
                    buttonpressed = True
                    annotations = [[]]
                    annotationnumber = 0
                  #  annotationstart = False
                    imgNumber-=1
            # gesture 2-right
            if fingers == [0, 0, 0, 0, 1]:
                annotationstart = False
                print("right")
                if imgNumber<len(pathImages)-1:
                   buttonpressed = True
                   annotations = [[]]
                   annotationnumber = 0
                  #annotationstart = False
                   imgNumber+=1
        #gesture 3- Show Pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)
            annotationstart = False
        # gesture 4- Draw Pointer
        if fingers == [0, 1, 0, 0, 0]:
            if annotationstart is False:
                annotationstart=True
                annotationnumber+=1
                annotations.append([])
            cv2.circle(imgCurrent,indexFinger,12,(0, 0, 255),cv2.FILLED)
            annotations[annotationnumber].append(indexFinger)
        else:
            annotationstart=False
        #gesture 5-erase
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                if annotationnumber>=0:
                    annotations.pop(-1)
                    annotationnumber-=1
                    buttonpressed=True
    else:
        annotationstart=False
    #BUTTON PRESSED ITERATION
    if buttonpressed:
        buttoncounter +=1
        if buttoncounter>buttondelay:
            buttoncounter=0
            buttonpressed=False


    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
           if  j!=0:
               cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)
    # adding webcam image on the sildes
    imgSmall=cv2.resize(img,(ws,hs))
    h,w, _ =imgCurrent.shape
    imgCurrent[0:hs,w-ws:w]=imgSmall

    cv2.imshow("Image",img)
    cv2.imshow("Slides", imgCurrent)

    key=cv2.waitKey(1)
    if key ==ord('q'):
        break