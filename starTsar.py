#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from PIL import Image, ImageFilter
import PIL
import numpy as np
import imageio
import rawpy
import matplotlib.pyplot as plt
import astroalign as aa
import numpy as np
import imageio
import ast

def load_image(f,Print=True):
    if(Print):
        print(f)
    
    try:
        with rawpy.imread(f) as raw:
            rgb = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=16)
            return rgb.astype(float)
    except:
        return np.asarray(imageio.imread(f).astype(float))
    
def save_image(rgb,f,bit=16):
    
    if(len(rgb)>len(rgb[0])):
        rgb=np.rot90(rgb)
    if(bit==16):
        imageio.imsave(f, rgb.astype(np.uint16))
    else:
        imageio.imsave(f, rgb.astype(np.uint8))
        
def show(im):
    im-=np.amin(im)
    plt.imshow(im/np.amax(im))
    plt.show()
    
    
    
def norm(image,c=0.1):
    
    if(len(image.shape)==3):
        
        for c in range(len(image[0][0])):
            
            image[:,:,c]=norm(image[:,:,c])
    else:
        
        limit=np.amax(image)
        mean=np.mean(image)
        x=[0,mean,limit]
        y=[0,limit*c,limit]
        function=np.polyfit(x, y, 2)
        newArray=image**2*function[0]+image*function[1]+function[2]
        newArray[newArray < 0] = 0
        newArray[newArray > limit] = limit
        return newArray
    
    return image

def path2name(path):
    inf=path.split("\\")
    return inf[len(inf)-1].split(".")[0]

def path2folder(path):
    inf=path.split("\\")
    path=""
    for p in inf[0:len(inf)-1]:
        path+=p+"\\"
    return path

import pickle
import numpy as np
from os.path import exists

def get_transformation(f1,f2):
    
    if(type(f1)==str and type(f2)==str):
        
        save_name=path2folder(f1)+path2name(f1)+"_Matched_To_"+path2name(f2)+".txt"

        if(exists(save_name)):

            file=open(save_name,'rb')

            transf = pickle.load(file)

            file.close()

            return transf

        else:
            primaryImage=load_image(f1)
            targetImage=load_image(f2)

            transf, (source_list, target_list) = aa.find_transform(targetImage,primaryImage)

            file=open(bytes(save_name, 'utf-8'),"wb")

            pickle.dump(transf,file)

            file.close()

            return transf
        
    else:
        
        transf, (source_list, target_list) = aa.find_transform(f1,f2)

        return transf
         

def apply_transformation(primary_ARRAY,scr,transf):
    
    aligned_image, footprint = aa.apply_transform(transf, primary_ARRAY, scr)
    
    footprint=np.invert(footprint)
    
    for c in range(3):
        aligned_image[:,:,c]=aligned_image[:,:,c]*footprint
    return aligned_image
    
    
def stack_minimum(fs):
    im=load_image(fs[0])
    
    for f in fs[1:len(fs)]:
        try:
            im=np.minimum(im,load_image(f))
        except Exception as e:
            print("error",f,e)
        
    return im

