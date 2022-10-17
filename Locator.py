#!/usr/bin/env python
# coding: utf-8

# In[2]:


from PIL import Image, ImageFilter
import PIL
import numpy as np
import imageio
import rawpy
import matplotlib.pyplot as plt
from skimage.io import imread
import matplotlib.pyplot as plt
import scipy.fftpack as fp
import numpy as np
from scipy import fftpack


def load_image(f):
    print("Loading",f)
    if(".CR2" in f):
        with rawpy.imread(f) as raw:
            rgb = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=16)
            return rgb.astype(float)
    else:
        return np.asarray(imageio.imread(f)).astype(float)

def save_image(rgb,f,bit=16):
    print("Saving",f)
    if(len(rgb)>len(rgb[0])):
        rgb=np.rot90(rgb)
    if(bit==16):
        imageio.imsave(f, rgb.astype(np.uint16))
    else:
        imageio.imsave(f, rgb.astype(np.uint8))
        
def highpass_filter_kernel(size):
    
    x=np.arange(size)
    
    x=(size-1)/2-np.abs(x-(size-1)/2)
    
    m=np.zeros((size,size))
    
    for i in range(size):
        for j in range(size):
            m[i][j]=x[i]*x[j]*2-1
    
    return m
    
def simple_high_pass(image,size=5):
    
    k=highpass_filter_kernel(size=size)
    
    if(len(image.shape)==3):
        
        result=np.zeros((k.shape[0],k.shape[1],image.shape[2]))
        
        for i in range(result.shape[2]):
            
            result[:,:,i]=k
        
        k=result
    
    return ndimage.convolve(image,k)


# In[22]:


def fft_high_pass(im,n=25,c=0):
    
    if(len(im.shape)==3):
        
        result=np.zeros(im.shape)
        
        for i in range(im.shape[2]):
            
            result[:,:,i]=fft_high_pass(im[:,:,i],n=n)
        
        return result
    
    F1 = fftpack.fft2((im).astype(float))
    F2 = fftpack.fftshift(F1)

    (w, h) = im.shape
    half_w, half_h = int(w/2), int(h/2)

    Fcopy=np.zeros(F2.shape)
    
    #Fcopy[half_w-n:half_w+n+1,half_h-n:half_h+n+1]=F2[half_w-n:half_w+n+1,half_h-n:half_h+n+1]
    
    F2[half_w-n:half_w+n+1,half_h-n:half_h+n+1] *=c # select all but the first 50x50 (low) frequencies

    #F2[100:210,140:240] = 0

    #plt.figure(figsize=(10,10))
    #plt.imshow( (20*np.log10( 0.1 + F2)).astype(int))
    #plt.show()

    im1 = fp.ifft2(fftpack.ifftshift(F2)).real
    
    return im1-np.mean(im1)

from scipy import ndimage

def target_filter(target,size=6):
    
    #k=simple_high_pass(target,size=size)

    k=fft_high_pass(target,n=size,c=0)
    
    k=k/np.amax(k)

    k-=np.mean(k)
    k=np.rot90(k,k=2)
    return k



def downsize(im, max_side=50,scaleFactor=2):

    if(scaleFactor==0):
        
        longSide=np.amax(im.shape)
        print(longSide)
        scaleFactor=longSide/max_side
        print(scaleFactor)
        
    import cv2
    return cv2.resize(im, dsize=(int(im.shape[1]/scaleFactor), int(im.shape[0]/scaleFactor)), interpolation=cv2.INTER_NEAREST)


# In[42]:



def shift_image(X, dx, dy):
    X = np.roll(X, dy, axis=0)
    X = np.roll(X, dx, axis=1)
    if dy>0:
        X[:dy, :] = 0
    elif dy<0:
        X[dy:, :] = 0
    if dx>0:
        X[:, :dx] = 0
    elif dx<0:
        X[:, dx:] = 0
    return X

def locate_image(image,target,scaleFactor=1,size=3,filtered=False,show=False):
    
    image=np.mean(image,axis=2)
    target=np.mean(target,axis=2)
    
    image=downsize(image,scaleFactor=scaleFactor)
    target=downsize(target,scaleFactor=scaleFactor)
    
    
        
    if(not filtered):
        target=target_filter(target,size=size)
        
    if(show):
        
        plt.imshow(target)
        plt.show()
        
        plt.imshow(target)
        plt.show()
    
    bconv=ndimage.convolve(image, target, mode='constant', cval=0.0)
    bconv/=np.amax(bconv)
    
    #bconv=downsize(bconv,scaleFactor=scaleFactor)
    
    
    coords=np.where(bconv==bconv.max())
    
    
    if(show):
        
        plt.imshow(bconv)
        plt.show()
        
        plt.imshow(bconv[coords[0][0]-20:coords[0][0]+20,coords[1][0]-20:coords[1][0]+20])
        plt.show()
        
    x=(coords[0][0])*scaleFactor
    y=(coords[1][0])*scaleFactor
    
    return x,y
    


def show(im):
    plt.imshow(im/np.amax(im))
    plt.show()

