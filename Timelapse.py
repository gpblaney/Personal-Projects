#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scipy.fftpack as fftpack

def high_pass(im,n=300):
    
    if(len(im.shape)==3):
        
        im[:,:,0] = high_pass(im[:,:,0])
        
        im[:,:,1] = high_pass(im[:,:,1])
        
        im[:,:,2] = high_pass(im[:,:,2])
        
        return im
    
    F1 = fftpack.fft2((im).astype(float))
    F2 = fftpack.fftshift(F1)

    (w, h) = im.shape
    half_w, half_h = int(w/2), int(h/2)


    F2[half_w-n:half_w+n+1,half_h-n:half_h+n+1] = 0 # select all but the first 50x50 (low) frequencies

    #F2[100:210,140:240] = 0

    #plt.figure(figsize=(10,10))
    #plt.imshow( (20*np.log10( 0.1 + F2)).astype(int))
    #plt.show()

    im1 = fp.ifft2(fftpack.ifftshift(F2)).real
    
    return im1-np.mean(im1)


# In[2]:


import cv2
import numpy as np
import os
from os.path import isfile, join
import matplotlib.pyplot as plt

def frames_to_video_helper(files,pathOut,fps=30):
    
    frame_array=[]
   
    if("." not in pathOut):
        pathOut+=".mp4"

    for i in range(len(files)):
        
        try:
        
            filename = files[i]

            img = cv2.imread(filename)

            height, width, layers = img.shape

            size = (width,height)

            frame_array.append(img)
            
        except:
            
            print("error",files[i])

        
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'AVC1'), fps, size)
    
    for i in range(len(frame_array)):
        
        #print(np.amax(frame_array[i]),np.amin(frame_array[i]))
        print("writing",i)
        out.write(frame_array[i])
        
    out.release()
    print(pathOut+" file has been written")
    
def concatenate_videos(filepaths,savename,fps=30):
    
    
    import cv2
    cap = cv2.VideoCapture(filepaths[0]) #0 for camera

    if cap.isOpened(): 
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
        fps = int(cap.get(cv2.CAP_PROP_FPS)) # float `fps`
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) # float `total_frame_in_the_video` (should not be applicable for camera)


    size=(width,height)
    
    if("." not in savename):
        savename+=".mp4"

    # Create a new video
    video = cv2.VideoWriter(savename,cv2.VideoWriter_fourcc(*'avc1'), fps, size)

    # Write all the frames sequentially to the new video
    for v in filepaths:
        curr_v = cv2.VideoCapture(v)
        while curr_v.isOpened():
            r, frame = curr_v.read()    # Get return value and curr frame of curr video
            if not r:
                break
            video.write(frame)          # Write the frame

    video.release()    
    
def frames_to_video(files,pathOut="",fps=30,chunkSize=200):
    
    if(pathOut == ""):
        
        string = files[0]
        
        i = len(string)-1
        
        while( string[i] != "\\" ):
            
            
            i = i-1
            
        pathOut=string[ 0 : i + 1 ] + "timelapse.mp4"
    
    if(len(files)<chunkSize):
        
        frames_to_video_helper(files,pathOut,fps=fps)
        
    else:
        
        
        files2Stack=[]
        
        fileChunks=[]
        
        i=0
        while(i<len(files)):
            
            fileChunks.append(files[i:i+chunkSize])
            
            files2Stack.append("Timelapse_Frames_"+str(i)+" - "+str(i+chunkSize)+".mp4")
            
            i+=chunkSize

        for i in range(len(fileChunks)):
            
            print(files2Stack[i])
            
            frames_to_video_helper(fileChunks[i],files2Stack[i],fps=fps)
            
        print("concatenate_videos")

        concatenate_videos(files2Stack,pathOut,fps=fps)
        


# In[ ]:





# In[3]:



def make_timelapse(path,fps=30,pathOut=""):
    import os
    files=[]
    for f in os.listdir(path):
        files.append(path+f)

    print(files)
    frames_to_video(files, fps=fps, pathOut=pathOut)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




