import sys
import os
import html
import Text_Tools
import ast
import matplotlib.pyplot as plt
from termcolor import colored
import numpy as np
from IPython.display import clear_output
sys.path.insert(1, 'C:\\Users\\gpbla\\Documents\\Goodies')
import Goodies as g
from os.path import exists
from Text_Tools import similar

import time
import os

root=r"C:\Users\gpbla\Desktop\Code\Language_Learning"+'\\'

def sort(score,inf):
    list1=score
    list2=inf
    zipped_lists = zip(list1, list2)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    list1, list2 = [ list(tuple) for tuple in  tuples]
    return list1, list2

supported_langs=[]

def is_cloud_lang(lang):

    global supported_langs

    if(len(supported_langs)==0):

        import re

        lines=open(root+"supported languages.txt").read().split("\n")

        for l in lines:

            inf=l.split("\t")[1]

            inf=re.sub(r'\(.*?\)', '', inf)
            
            if(" or " in inf):
                
                supported_langs.extend(inf.split(" or "))
                
            else:
                
                supported_langs.append(inf)

        return is_cloud_lang(lang)
    
    else:

        return lang in supported_langs
            


def trans(text,source_lang):

    return g.word_translation(text,source_lang,justDict=True)

    '''

    text = Text_Tools.clean_text( text )

    if(is_cloud_lang(source_lang)):

        return g.trans(text,source_lang=source_lang)
    
    else:

        try:

            import General_Language_Study

            LH = General_Language_Study.lang_handler(source_lang)

            return LH.findTrans(text)

        except:

            return g.trans(text,source_lang=source_lang)

    '''



def logShuffle(U,num):
    
    AskList=[]          
    n=0
    while(len(AskList)<num and n<100000):
        index=int(len(U)*-0.1*np.log(-np.random.random()+1))
        if(index<len(U)):
            if(U[index] not in AskList):
                AskList.append(U[index])
        n+=1
    return AskList



def update_log(entryType,q,response,language):

    information = [ entryType , q , response , time.time() ]

    with open("C:\\Users\\gpbla\\Documents\\Goodies\\log_"+language+".txt", "a",encoding="utf-8") as myfile:

        myfile.write("\n"+str(information))
        




class wordTable:
    
    def __init__(self,lang,dir_path="C:\\Users\\gpbla\\Documents\\Goodies\\"):
        self.language=lang
        self.dir_path=dir_path
        try:
            self.load_stats()
        except: 
            #could not find stats for this language
            self.calculate_stats()

    def isChinese(self):
        return "zh" in self.language
            
    def load_stats(self):
        
        inf=open(self.dir_path+"stats_"+self.language+".txt", "r",encoding="utf-8").read().split("\n") 
        self.words=ast.literal_eval(inf[0])
        #print(self.words)
        self.ocs=ast.literal_eval(inf[1])
        self.wordConfidence=ast.literal_eval(inf[2])
        #self.trans=ast.literal_eval(inf[3])
        
    def save_stats(self):
        with open(self.dir_path+"stats_"+self.language+".txt", "w",encoding="utf-8") as myfile: 
            myfile.write(str(self.words)+"\n")
            myfile.write(str(self.ocs)+"\n")
            myfile.write(str(list(self.wordConfidence))+"\n")
            #myfile.write(str(self.trans)+"\n")
            
    def check_duolingo(self):
        
        #TODO
            
    def load_corpus(self):
        
        #A corpus folder is here is for all language materials to track progress and to create statistics
        corpus_path=self.dir_path+"corpus_"+self.language

        #Check that there is a corpus, if there is none create a corpus folder
        if not os.path.exists(corpus_path):
            os.makedirs(corpus_path)

        #This is a list of all the materials in the target language
        files=os.listdir(corpus_path)
        
        #load all of them into a single string
        all_text=""

        for f in files:
            if(".txt" in f):
                try:
                    all_text+=g.load_text(corpus_path+"\\"+f)+" "
                except Exception as e: 
                    print(e)
                    from Text_Tools import convertText
                    convertText(corpus_path+"\\"+f)
                    all_text+=g.load_text(corpus_path+"\\"+f)+" "
                    
        return Text_Tools.text2phrases(all_text,chinese = self.isChinese())
            
    
    def calculate_stats(self,save=True):
    
        self.check_duolingo()
     
        #A corpus folder is here is for all language materials to track progress and to create statistics
        corpus_path=self.dir_path+"corpus_"+self.language
        
        #Check that there is a corpus, if there is none create a corpus folder
        if not os.path.exists(corpus_path):
            os.makedirs(corpus_path)
        
        #This is a list of all the materials in the target language
        files=os.listdir(corpus_path)
        
        
        #load all of them into a single string
        all_text=""
        
        for f in files:
            if(".txt" in f):
                try:
                    all_text+=g.load_text(corpus_path+"\\"+f)+" "
                except Exception as e: 
                    print(e)
                    from Text_Tools import convertText
                    convertText(corpus_path+"\\"+f)
                    all_text+=g.load_text(corpus_path+"\\"+f)+" "
                    
        #normalize text
        all_text=Text_Tools.clean_text(all_text)
        
        #get a formatted list of words from most to least common with a corresponding list of occurences

        allwords=all_text
        from Text_Tools import phrase2Words
        allwords=phrase2Words(all_text,lang=self.language)

        self.words,self.ocs=Text_Tools.wordsNfreqs(allwords)
        
        #import the log to track progress and update known words
        log=[]
        try:
            log=open(self.dir_path+"log_"+self.language+".txt",encoding="utf-8").read().split("\n")
        except:
            try:
                #if the text file in the corpus cannot be opened by utf-8 then convert it
                from Text_Tools import convertText
                convertText(self.dir_path+"log_"+self.language+".txt")
                log=open(self.dir_path+"log_"+self.language+".txt",encoding="utf-8").read().split("\n")
            except:
                #if no long exists create an empty one
                log=open(self.dir_path+"log_"+self.language+".txt",'w',encoding="utf-8")
                
        
        #get a list of all known words from the activity log
        
        duolingo_words=[]
        duolingo_scores=[]
        
        known_words=[]
        recognised_words=[]
        for l in log:
            if(len(l)>0):
                x=ast.literal_eval(l)
                if(x[0]=="duolingo"):
                    duolingo_words.append(x[1])
                    duolingo_scores.append(float(x[2]))
                if(x[0]=="inquiry" or x[0]=="implied"):
                    if(x[2]):
                        if(x[1] in self.words):
                            known_words.append(x[1])
                if(x[0]=="recognised"):
                    if(x[2]):
                        if(x[1] in self.words):
                            recognised_words.append(x[1])
                        
        # wordConfidence is an array of confidence for each word between 0 - 1
        self.wordConfidence=np.zeros(len(self.words))

        # set confidence for already known words
        for i in range(len(self.words)):
            if(self.words[i] in known_words):
                self.wordConfidence[i]=1
            elif(self.words[i] in recognised_words):
                if(self.wordConfidence[i]<0.9):
                    self.wordConfidence[i]=0.9
                
            if(self.words[i] in duolingo_words):
                score=duolingo_scores[duolingo_words.index(self.words[i])]
                if(score>self.wordConfidence[i]):
                    self.wordConfidence[i]=score

        #save the stats so that they can be loaded quickly in the future
        self.save_stats()

    def text2Words(self,filename):

        text=open(filename,encoding="utf-8").read()

        text=Text_Tools.clean_text(text)
        
        new_words=[]

        from Text_Tools import phrase2Words

        return phrase2Words(text,lang=self.language)

    def confidence_string(self,filename):
        words = self.text2Words(filename)
        confs=[]
        for w in words:
            confs.append(self.confidence(w))
        return words,confs

            
    def text_vocab(self,text):
        
        text=Text_Tools.clean_text(text)
        
        new_words=[]

        from Text_Tools import phrase2Words

        all_new_words=phrase2Words(text,lang=self.language)

        new_ocs=[]

        for w in all_new_words:
            if(w not in new_words):
                new_words.append(w)
                new_ocs.append(-1*all_new_words.count(w))
        return sort(new_ocs,new_words)
            
    def confidence(self,word):
        if(word not in self.words):
            return 0
        return self.wordConfidence[self.words.index(word)]
            
    def unknown_words(self,new_words=-1,cutoff=.9):
        
        unknown=[]
        
        if(new_words==-1):
            for i in range(len(self.wordConfidence)):
                if(self.wordConfidence[i]<cutoff):
                    unknown.append(self.words[i])
        else:
            for w in new_words:
                add=True
                if(w in self.words):
                    if(self.wordConfidence[self.words.index(w)]>cutoff):
                        add=False
                
                '''
                if(add):
                    simularity=similar(w,g.word_translation(w,self.language))
                    if(simularity>0.7):
                        add=False
                        update_log_implied(w,True,self.language)
                '''
                
                if(add):
                    unknown.append(w)
        return unknown
        
    def print_options(self):
        print("1: Add a youtube video to the corpus.")
        print("2: Add a youtube video to the textbin.")
        print("3: Rate video comprehensibility.")
        print("4: Mark Known Words")
        print("5: Load text")
        print("6: Calculate Stats")
        print("7: Show Progress")
        print("8: Print Unknown Words")
        print("9: Input Known Words")
        
        
    def open_dialogue(self):
        print("Hello! Welcome to your new word table for",self.language)
        
        while(True):
            self.print_options()
            text=input(":")
            if(text=="clear"):
                clear_output(wait=True)
                
            if(text=="1"):
                ID=" "
                while(ID!="" and ID!="q"):
                    if(ID!=" "):
                        try:
                            self.add_youtube_video_to_corpus(ID)
                        except Exception as e: 
                            print(e)
                            print("Could not add this video to the corpus")
                    ID=input("What would you like to add?")
                    
            if(text=="2"):
                ID=" "
                while(ID!="" and ID!="q"):
                    if(ID!=" "):
                        try:
                            self.add_youtube_video_to_textbin(ID)
                        except Exception as e: 
                            print(e)
                            print("Could not add this video to the corpus")
                    ID=input("What would you like to add?")
                    
            if(text=="3"):
                ID=" "
                while(ID!="" and ID!="q"):
                    if(ID!=" "):
                        try:
                            score=self.rate_video_comprehensibility(ID)
                            print("This video is about "+str(score*100)+" % comprehensible")
                        except Exception as e: 
                            print(e)
                            print("Could not rate this video to the corpus")
                    ID=input("What would you like to rate?")
                    
            if(text=="4"):
                U=self.unknown_words()
                
                AskList=logShuffle(U,50)
                print("AskList",len(AskList))
                
                self.mark_known_words(AskList)
                    
            if(text=="5"):
                self.load_text()
                
            if(text=="6"):
                self.calculate_stats()
                
            if(text=="7"):
                self.show_progress()
                
            if(text=="8"):
                self.print_unknown_words()
                
            if(text=="9"):
                self.input_known_words()
                
            if(text=="q"):
                return
            
    def input_known_words(self):
        while(True):
            I=input(":")
            if(I=="q"):
                return
            if(I!=""):
                update_log("inquiry",I,True,self.language)
            
    def print_unknown_words(self):
        num=0
        for i in range(len(self.words)):
            if(num<1000):
                if(self.wordConfidence[i]<0.6):
                    print(self.words[i])
                    num+=1
                    
    def show_progress(self):
        
        x=[]
        for i in range(len(self.words)):
            if(self.wordConfidence[i]>0.6):
                x.append(i)
        plt.hist(x,bins=100)
        plt.show()
        x=np.arange(len(self.words))
        x+=1
        y=[]
        sum=0
        for i in self.wordConfidence:
            sum+=i
            y.append(sum)
        plt.plot(y/x)
        plt.show()
        g.plot_square_stats(self.ocs,self.wordConfidence)
                
    def mark_known_words(self,words):
        toCheck=words
        np.random.shuffle(toCheck)
        for w in toCheck:
            if(True):
                ans=input("Do you know this word? "+w+" :")
                if(ans=="q"):
                    return
                if(ans=="y"):
                    update_log("inquiry",w,True,self.language)
                else:
                    print("That's okay just so you know "+w+" = "+g.word_translation(w,self.language))
                    input_2=input("Do you recognise it? :")
                    update_log("inquiry",w,False,self.language)
                    if(input_2=="y"):
                        update_log("recognised",w,True,self.language)
                    else:
                        update_log("recognised",w,False,self.language)
                    
    def text2Vocab(self, filename):
        text=open(filename,encoding="utf-8").read()
        O,W=self.text_vocab(text)
        return O,W

    def load_text(self):
        filepath=g.choose_file(self.dir_path+"corpus_"+self.language+"\\")
        N=filepath.split("\\")
        name=""
        for n in N:
            if(len(n)>0):
                name=n
                
        text=g.load_text(filepath)
        O,W=self.text_vocab(text)
        if(filepath==""):
            return
        
        while(True):
            print("1. Rate text comprehensibility")
            print("2. List unknown words")
            print("3. Make audio flashcards")
            print("4. Make audio study examples")
            print("5. Mark known words")
            I=input("::")
            if(I=="1"):
                rating=self.rate_comprehensibility(O,W)
                print(rating)
                
            if(I=="2"):
                U=self.unknown_words(W)
                for u in U:
                    print(u)
                I2=input("Would you like to mark any of these words as known?")
                if(I2=="y"):
                    self.mark_known_words(U)
                    
            if(I=="3"):
                import audiobook_maker
                Words=self.unknown_words(W)
                lim=50
                try:
                    lim=int(input("How many?:"))
                except Exception as e: 
                    print(e)
                    x=0
                audiobook_maker.render_audio_flashcards(Words[0:lim],self.language,name.split(".")[0])
                    
            if(I=="4"):
                import audiobook_maker
                Words=self.unknown_words(W)
                lim=50
                try:
                    lim=int(input("How many?:"))
                except Exception as e: 
                    print(e)
                    x=0
                audiobook_maker.render_audio_flashcards_examples(Words[0:lim],self.language,name.split(".")[0]+"_examples")

            if(I=="5"):

                Words=self.unknown_words(W)
                self.mark_known_words(Words)
            
            if(I==""):
                self.load_text()
                return
            if(I=="q"):
                return
        
    def rate_text_comprehensibility(self,filepath):
        text=g.load_text(filepath)
        text=Text_Tools.clean_text(text)
        return self.rate_comprehensibility(text)
    
    def rate_video_comprehensibility(self,ID):
        x=g.youtube_transcript(ID,self.language)
        text=""
        for i in x:
            text+=i['text']+" "
        text=Text_Tools.clean_text(text)
        return self.rate_comprehensibility(text)
        
    def rate_comprehensibility(self,new_ocs,new_words):
        score=0
        for i in range(len(new_words)):
            score+=self.confidence(new_words[i])
        return score/len(new_words)
    
    def add_to_corpus(self,text,name):
        if(".txt" not in name):
            name+=".txt"
        if(not exists(self.dir_path+"corpus_"+self.language)):
            os.mkdir(self.dir_path+"corpus_"+self.language)
        g.save_text(text,self.dir_path+"corpus_"+self.language+"\\"+name)
        
    def add_youtube_video_to_textbin(self,ID):
        if("=" in ID):
            ID=ID.split("=")[1]
        text=get_youtube_text(ID,self.language)
        g.save_text(text,"C:\\Users\\gpbla\\Desktop\\Text_Bin\\"+ID+".txt")

    def add_youtube_video_to_corpus(self,ID):
        if("=" in ID):
            ID=ID.split("=")[1]
        text=get_youtube_text(ID,self.language)
        self.add_to_corpus(text,ID)
  

        
        
def get_youtube_text(ID,language):
    text=""
    x=g.youtube_transcript(ID,language)
    for s in x:
        text+=s['text'].lower()+"\n"
    return text


import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import reverse_cuthill_mckee

def sortArray(arr):
    graph = csr_matrix(arr)
    perm = reverse_cuthill_mckee(graph)
    reord_arr = csr_matrix.toarray(graph[perm])
    return perm



def delete_inside(text,a,b):
    text=str(text)
    string=""
    add=True
    for c in text:
        
        if(c==b):
            add=True
        if(add):
            string+=c
        if(a==c):
            add=False
        
    return string

def matcher_helper(p1,p2,chinese=False):

    if(not chinese):

        w1=p1.lower().split(" ")
        w2=p2.lower().split(" ")

    score=0

    for a in w1:
        for b in w2:
            if(a==b):
                score+=1

    return score

def phrase_matcher(phrases,chinese=False):
    
    matrix=np.zeros((len(phrases),len(phrases)))
    #print(sortArray(matrix))
    for i in range(len(phrases)):
        for j in range(i):
            v=matcher_helper(phrases[i],phrases[j],chinese=chinese)
            matrix[i][j]=v
            matrix[j][i]=v
            
    return matrix
            



