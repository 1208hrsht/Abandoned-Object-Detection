import numpy as np
import cv2
from collections import Counter, defaultdict
 
firstframe_path =r'Input Path of first frame'

firstframe = cv2.imread(firstframe_path)
firstframe_gray = cv2.cvtColor(firstframe, cv2.COLOR_BGR2GRAY)
firstframe_blur = cv2.GaussianBlur(firstframe_gray,(21,21),0)

cv2.namedWindow('CannyEdgeDet',cv2.WINDOW_NORMAL)
cv2.namedWindow('Abandoned Object Detection',cv2.WINDOW_NORMAL)
cv2.namedWindow('Morph_CLOSE',cv2.WINDOW_NORMAL)

file_path =r'Input Path of surveillance video'
cap = cv2.VideoCapture(file_path)

consecutiveframe=20

track_temp=[]
track_master=[]
track_temp2=[]

top_contour_dict = defaultdict(int)
obj_detected_dict = defaultdict(int)

frameno = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('main',frame)
    
    if ret==0:
        break
    
    frameno = frameno + 1
    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray,(21,21),0)
     
    frame_diff = cv2.absdiff(firstframe, frame)
  
    #Canny Edge Detection
    edged = cv2.Canny(frame_diff,10,200)
    cv2.imshow('CannyEdgeDet',edged)
    kernel2 = np.ones((5,5),np.uint8)
    thresh2 = cv2.morphologyEx(edged,cv2.MORPH_CLOSE, kernel2,iterations=2)
    cv2.imshow('Morph_Close', thresh2)
       
    (cnts, _)= cv2.findContours(thresh2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    mycnts =[] 
    for c in cnts:

        M = cv2.moments(c)
        if M['m00'] == 0: 
            pass
        else:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            if cv2.contourArea(c) < 200 or cv2.contourArea(c)>20000:
                pass
            else:
                mycnts.append(c)
                (x, y, w, h) = cv2.boundingRect(c)
                sumcxcy=cx+cy
                track_temp.append([cx+cy,frameno])
                
                track_master.append([cx+cy,frameno])
                countuniqueframe = set(j for i, j in track_master)
                
                if len(countuniqueframe)>consecutiveframe or False: 
                    minframeno=min(j for i, j in track_master)
                    for i, j in track_master:
                        if j != minframeno:
                            track_temp2.append([i,j])
                
                    track_master=list(track_temp2)
                    track_temp2=[]
               
                countcxcy = Counter(i for i, j in track_master)

                for i,j in countcxcy.items(): 
                    if j>=consecutiveframe:
                        top_contour_dict[i] += 1
  
                
                if sumcxcy in top_contour_dict:
                    if top_contour_dict[sumcxcy]>100:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
                        cv2.putText(frame,'%s'%('CheckObject'), (cx,cy),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
                        print ('Detected : ', sumcxcy,frameno, obj_detected_dict)
                        obj_detected_dict[sumcxcy]=frameno

    for i, j in obj_detected_dict.items():
        if frameno - obj_detected_dict[i]>200:
            print ('PopBefore',i, obj_detected_dict[i],frameno,obj_detected_dict)
            print ('PopBefore : top_contour :',top_contour_dict)
            obj_detected_dict.pop(i)

            top_contour_dict[i]=0
            print ('PopAfter',i, obj_detected_dict[i],frameno,obj_detected_dict)
            print ('PopAfter : top_contour :',top_contour_dict)
    
    cv2.imshow('Abandoned Object Detection',frame)
         
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
