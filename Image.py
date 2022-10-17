#!/usr/bin/env python
# coding: utf-8

# In[1]:


from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFilter
import PIL
import numpy as np
import imageio
import rawpy
import matplotlib.pyplot as plt
import cv2

def load(f,npType=float):

    try:
        return np.asarray(imageio.imread(f)).astype(npType)
    
    except:
        with rawpy.imread(f) as raw:
            rgb = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=16)
            return rgb.astype(npType)
    
def save(rgb,f,bit=8):
    
    if(bit==16):
        imageio.imsave(f, rgb.astype(np.uint16))
    else:
        imageio.imsave(f, rgb.astype(np.uint8))
        
def crop(im,x1,y1,x2,y2):
    
    return im[x1:x2,y1:y2]


def normalize_image(image,const=0.5,MaxValue=255):
    image[:,:,0]=normalize_array(image[:,:,0],const=const,MaxValue=MaxValue)
    image[:,:,1]=normalize_array(image[:,:,1],const=const,MaxValue=MaxValue)
    image[:,:,2]=normalize_array(image[:,:,2],const=const,MaxValue=MaxValue)
    return image


def normalize_array(array,const=0.5,MaxValue=255):
    #print(np.amin(array),np.amax(array))
    #limit=np.amax(array)
    limit=MaxValue
    mean=np.mean(array)
    x=[0,mean,limit]
    y=[0,limit*const,limit]
    function=np.polyfit(x, y, 2)
    newArray=array**2*function[0]+array*function[1]+function[2]
    newArray[newArray < 0] = 0
    newArray[newArray > limit] = limit
    return newArray

# In[2]:

def shrink(im, max_side=500,factor=-1):

    if(factor==-1):
        
        longSide=np.amax(im.shape)
        print(longSide)
        scaleFactor=longSide/max_side
        print(scaleFactor)
        return cv2.resize(im, dsize=(int(im.shape[1]/scaleFactor), int(im.shape[0]/scaleFactor)), interpolation=cv2.INTER_CUBIC),scaleFactor

    else:
        scaleFactor=factor
        return cv2.resize(im, dsize=(int(im.shape[1]/scaleFactor), int(im.shape[0]/scaleFactor)), interpolation=cv2.INTER_CUBIC),scaleFactor





# In[ ]:




