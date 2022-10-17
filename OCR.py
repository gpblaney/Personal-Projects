#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def toText(filepath):
    
    if(type(filepath)==list):
        
        string=""
        
        for p in filepath:
            
            string+=toText(p)
            
        return string
    
    try:
        return pytesseract.image_to_string(filepath)
    
    except Exception as e:
        
        print(e)
        return ""


# In[7]:





# In[ ]:




