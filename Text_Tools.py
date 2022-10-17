#!/usr/bin/env python
# coding: utf-8

# In[1]:


import html
import numpy as np
import sys
sys.path.insert(1, 'C:\\Users\\gpbla\\Documents\\Goodies')
import Goodies as g


def clean_text(text):
    text=text.replace("\xa0","")
    text=text.replace("\x92","'")
    text=text.replace("\x9c","œ")
    text=text.replace("\\'","'")
    text=text.replace("\x02"," ")
    text=html.unescape(text)
    text=text.lower()
    
    junk="-[]8615023479 ,+%_.\\:@/!«»=>()?\"&;*\n’'–†„“©_<>#…%@¹²á³⁴*®{}]/$‚‘æ+|=∙·•\t⸂⸃·—-_"
    for j in junk:
        text=text.replace(j," ")
    while("  " in text):
        text=text.replace("  "," ")
    return text

def phrase2Words(text,lang='en'):

    if("zh" in lang):

        import Chinese

        return Chinese.phrase2Words(text)
    
    return text.split(" ")

def secondSplit(phrases,c,size=20):

    finalPhrases=[]

    for p in phrases:        

        if(len(p.split(" "))>size):

            finalPhrases.extend(p.split(c))

        else:

            finalPhrases.append(p.replace(c," "))

    return finalPhrases

def text2phrases(text,chinese=False):


    if(chinese):
        text=text.replace("。",".")
        text=text.replace("，",".")
        text=text.replace("：",".")
        text=text.replace("\"",".")
        text=text.replace("(",".")
        text=text.replace(")",".")
        text=text.replace(",",".")
        text=text.replace("«",".")
        text=text.replace("»",".")
        text=text.replace("!",".")
        text=text.replace("?",".")
        text=text.replace("—",".")
        text=text.replace(":",".")
        text=text.replace("》",".")
        text=text.replace("《",".")
        text=text.replace("；",".")
        text=text.replace("！",".")
        text=text.replace(" ",".")
        return text.split(".")

    else:
        #text=text.replace("\n"," ")
        
        #\x85
        text=text.replace("\x85","\n")
        text=text.replace("\xa0","")
        text=text.replace("\x92","'")
        text=text.replace("\x9c","œ")
        text=text.replace("\'","'")
        text=text.replace("\x02"," ")
        text=text.replace("(",".")
        text=text.replace(")",".")
        text=text.replace(",",".")
        text=text.replace("«",".")
        text=text.replace("»",".")
        text=text.replace("!",".")
        text=text.replace("?",".")
        text=text.replace("—",".")
        text=text.replace(":",".")
        text=text.replace("\t"," ")
        #text=text.replace("\n"," ")
        text=text.replace("⸃","")
        text=text.replace("⸀","")

        phrases=text.split(".")

        phrases=secondSplit(phrases,"\n")

        #phrases=secondSplit(phrases," ")

        return phrases

        '''
        phrases2=[]
        for p in phrases:
            if(p.count(" ")>=2):
                phrases2.append(p)
        return phrases2
        '''

def wordsNfreqs(allwords):

    if(type(allwords)==str):
        newAllWords=[]
        for w in allwords:
            newAllWords.append(w)
        allwords=newAllWords


    allwords=np.sort(allwords)
    words=[]
    words.append(allwords[0])
    ocs=np.zeros(len(allwords))
    n=0
    for i in range(1,len(allwords)):
        if(allwords[i]!=allwords[i-1]):
            words.append(allwords[i])
            n+=1
            ocs[n]=1
        else:
            ocs[n]+=1
    ocs=ocs[0:n+1]
    #print(len(ocs),len(words))
    ocs,words=g.sort(ocs,words,r=True)
    return words,ocs



from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file("C:\\Users\\gpbla\\Documents\\Goodies\\divine-clone-316305-7c81794b2e83.json")

from google.cloud import translate_v2 as translate
translate_client = translate.Client(credentials=credentials)
import html

def get_language(TEXT):
    
    sourceLang=""
    
    try:
        
        sourceLang=translate_client.detect_language(TEXT[0:100])['language']
        if("ي" in TEXT):
            sourceLang='ar'
            
    except Exception as e:
        
        print(e)
        sourceLang=input("What is the lang of this file? "+filename)
        
    return sourceLang


def similar(a, b):

    from difflib import SequenceMatcher

    return SequenceMatcher(None, a, b).ratio()

def convertText(f,sourceEncoding = "iso-8859-1",targetEncoding = "utf-8"):
    
    source = open(f,encoding=sourceEncoding).read()

    target = open(f, "w",encoding=targetEncoding)
    
    target.write(source)
