
import sys
sys.path.insert(1, 'C:\\Users\\gpbla\\Documents\\Goodies')
import Goodies as g
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from Text_Tools import text2phrases


textbin="C:\\Users\\gpbla\\Desktop\\Text_Bin\\"

def secondSplit(phrases,c,size=20):
    finalPhrases=[]
    for p in phrases:
        if(len(p.split(" "))>size):
            finalPhrases.extend(p.split(c))
        else:
            finalPhrases.append(p.replace(c," "))
    return finalPhrases



def render(filename,finalName,sourceLang=""):
    
    TEXT=open(textbin+filename,encoding='utf-8').read()

    phrases=text2phrases(TEXT)
    
    if(sourceLang==""):

        from Text_Tools import get_language

        sourceLang=get_language(TEXT)

    print(filename,sourceLang)
    
    biCOMB=AudioSegment.empty()
    monoCOMB=AudioSegment.empty()
    
    allWords=[]
    
    for i in range(len(phrases)):
        
        for w in phrases[i].lower().split(" "):
            if(w not in allWords):
                allWords.append(w)
        
        print(i/len(phrases))
        if(len(phrases[i])>0):
            
            trans=g.trans(phrases[i],source_lang=sourceLang)
            if(len(trans)>0 and len(phrases[i])>0):
                
                biCOMB+=g.get_tts(trans,lang='en')
                targetAudio=g.get_tts(phrases[i],lang=sourceLang)
                
                biCOMB+=targetAudio 
                monoCOMB+=targetAudio
                
    biCOMB.export(finalName+"_bi.mp3", format="mp3")
    monoCOMB.export(finalName+"_mono.mp3", format="mp3")
    
    make_flashcards(TEXT,sourceLang,filename)
        
    g.move_file(textbin+filename,"C:\\Users\\gpbla\\Desktop\\DesktopJunk\\finished_bilingual_audiobook\\"+filename)
    
    upload_to_lingq(TEXT,sourceLang,filename)

    print("Finished",filename)
    
def make_flashcards(TEXT,sourceLang,filename):
    
    import wordTable as wt
    
    try:
        WT=wt.wordTable(sourceLang)
        try:
            WT.add_to_corpus(TEXT,filename)
        except Exception as e: 
            print(e)
            
            print("could not add",filename,"to corpus")
        U=WT.unknown_words(allWords)
        np.random.shuffle(U)
        U=U[0:50]
        if(len(U)>0):
            render_audio_flashcards(U,sourceLang,filename.split(".")[0])
        else:
            print("There are no unknown words here!")
            
    except Exception as e: 
        print(e)
        print("Error do you have a corpus for",sourceLang)
    
def upload_to_lingq(TEXT,sourceLang,filename):
    
    import lingq
    
    try:
        print(filename.split(".")[0],TEXT,sourceLang,filename.split(".")[0]+"_mono.mp3")
        lingq.upload_to_lingq(filename.split(".")[0],TEXT,sourceLang,audioPath="C:\\Users\\gpbla\\Desktop\\toEmail\\"+filename.split(".")[0]+"_mono.mp3")
        print("Saved lingq!")
    except Exception as e:
        print(e)
        print("Could not upload this to lingq")
    
def render_audio_flashcards(cards,sourceLang,filename,destLang="en", cognateLang="en"):

    flashCOMB=AudioSegment.empty()
    
    string=""
    
    for c in cards:
        string+=c+"\n"
        try:
            
            import Definition_Finder

            trans=Definition_Finder.get_definitions(c,sourceLang)

            #trans=g.trans(c,source_lang=sourceLang)
            if(len(trans)>0):
                flashCOMB+=g.get_tts(trans,lang=destLang)
                flashCOMB+=g.get_tts(c,lang=sourceLang)

                #try to find cognates
                import Cognate_Finder
                flashCOMB+=Cognate_Finder.render_this_Is_Cognate_With(c,sourceLang,cognateLang)

        except Exception as e: 
            print(e)
            print("error",c,trans)
            
            
    '''
    import lingq
    
    try:
        lingq.upload_to_lingq("Daily Words",string,sourceLang)
        print("Saved words to lingq!")
    except Exception as e:
        print(e)
        print("Could not upload this to lingq")
    '''
        
    flashCOMB.export(g.send_folder+filename+"_flashcards.mp3", format="mp3")
    
def make():
    allFiles=g.all_files(textbin)

    for f in allFiles:
        if(".txt" in f):
            try:
                print("Creating a bilingual audiobook for",f)
                name=f.replace(".txt","")
                render(f,g.send_folder+name)
                #render_word_by_word(f,g.send_folder+name)
            except Exception as e: 
                print(e)
                print("error",f)


# In[3]:


def render_audio_flashcards_examples(cards,sourceLang,filename,make_video=False,destLang='en',cognateLang='en'):
    import wordTable as wt
    import text2Image
    import numpy as np
    
    WT=wt.wordTable(sourceLang)

    phrases=WT.load_corpus()
    #print(phrases)
    np.random.shuffle(phrases)
    hereAreSomeExamples=g.get_tts("Here are some examples",lang='en')
    
    if(make_video):
        import os
        if(filename not in os.listdir()):
            os.mkdir(filename)
    
    flashCOMB=AudioSegment.empty()
    
    count=0
    
    from Reverso import get_reverso_examples

    for c in cards:
        try:
            
            import Definition_Finder
            trans=Definition_Finder.get_definitions(c,sourceLang)

            if(len(trans)>0):
                flashCOMB+=g.get_tts(trans,lang='en')
                flashCOMB+=g.get_tts(c,lang=sourceLang)
            examples=[]

            import Cognate_Finder
            flashCOMB+=Cognate_Finder.render_this_Is_Cognate_With(c,sourceLang,cognateLang)

            for p in phrases:

                from Text_Tools import phrase2Words

                phraseWords=phrase2Words(p,lang=sourceLang)

                if(len(phraseWords)<10):
                    if(c in phraseWords and len(examples)<5):
                        if(p not in examples):
                            examples.append(p)


            if(len(examples)<5):
                e,t=get_reverso_examples(c,sourceLang,maxExamples=5-len(examples))
                print("Found",len(e),"Reverso Examples")
                examples.extend(e)
            
            if(len(examples)>0):
                flashCOMB+=hereAreSomeExamples
                N=0
                for e in examples:
                    
                    print(c,e)
                    
                    if(N>0):
                        flashCOMB+=g.get_tts(c,lang=sourceLang)
                    N+=1
                    
                    trans=g.trans(e,source_lang=sourceLang,dest_lang=destLang)
                    
                    temp_audio=g.get_tts(trans,lang=destLang)+g.get_tts(e,lang=sourceLang)
                    
                    if(make_video):
                        count+=1
                        temp_audio.export(filename+"\\temp_"+str(count)+".mp3")
                        image=text2Image.top_bottom(e,trans,size=(800,400))
                        image.save(filename+"\\temp_"+str(count)+".jpg")
                    
                    flashCOMB+=temp_audio

            else:
                print("no example!!",c)
            
        except Exception as e: 
            print(e)
            print("error",c,trans)
    
    if(make_video):
        import movie
        movie.slideshow_from_folder(filename+"\\",filename+".MP4")
    flashCOMB.export(g.send_folder+filename+"_flashcards.mp3", format="mp3")
    
    print("Finished Making",filename)

    
def render_general_examples(cards,sourceLang,filename,make_video=False):
    g.dictionaries=[]

    from General_Language_Study import lang_handler
    import text2Image
    import numpy as np
    
    if(make_video):
        import os
        if(filename not in os.listdir()):
            os.mkdir(filename)
    
    LH=lang_handler(sourceLang)
    
    phrases=LH.getPhrases()
    
    #np.random.shuffle(phrases)
    hereAreSomeExamples=g.get_tts("Here are some examples",lang='en')
    
    count=0
    
    flashCOMB=AudioSegment.empty()
    for c in cards:
        try:
            
            trans=""
            print(c,trans)
            trans=g.trans(c,source_lang=sourceLang)
            if(len(trans)>0):
                flashCOMB+=g.get_tts(trans,lang='en')
            else:
                flashCOMB+=g.get_tts("No Translation",lang='en')
            
            #revert to english
            
            spoken_word=LH.tts(c)
            #spoken_word=g.get_tts(c,lang="en")
            flashCOMB+=spoken_word
            
            examples=[]
            
            for p in phrases:
                if(c in p.lower().split(" ") and len(examples)<5):
                    if(p not in examples):
                        examples.append(p)
            
            examples = sorted(examples, key=len)
            
            if(len(examples)>0):
                flashCOMB+=hereAreSomeExamples
                N=0
                for e in examples:
                    print(c,e)
                    if(N>0):
                        flashCOMB+=spoken_word
                    N+=1
                    trans=LH.findTrans(e)
                    temp_audio=g.get_tts(trans,lang='en')+LH.findAudio(e)
                    flashCOMB+=temp_audio
                    
                    if(make_video):
                        count+=1
                        temp_audio.export(filename+"\\temp_"+str(count)+".mp3")
                        image=text2Image.top_bottom(e,trans,size=(800,400))
                        image.save(filename+"\\temp_"+str(count)+".jpg")
                
                    
            else:
                print("no example!!",c)
            
        except Exception as e: 
            print(e)
            print("error",c,trans)
            
    if(make_video):
        import movie
        movie.slideshow_from_folder(filename+"\\",filename+".MP4")
    flashCOMB.export(g.send_folder+filename+"_flashcards.mp3", format="mp3")
    
    print("Finished Making",filename)

def render_general_flashcards(cards,sourceLang,filename,make_video=False):
    g.dictionaries=[]

    from General_Language_Study import lang_handler
    import text2Image
    import numpy as np
    
    if(make_video):
        import os
        if(filename not in os.listdir()):
            os.mkdir(filename)
    
    LH=lang_handler(sourceLang)
    
    phrases=LH.getPhrases()
    
    #np.random.shuffle(phrases)
    hereAreSomeExamples=g.get_tts("Here are some examples",lang='en')
    
    count=0
    
    flashCOMB=AudioSegment.empty()
    for c in cards:
        try:
            
            trans=""
            print(c,trans)
            trans=g.trans(c,source_lang=sourceLang)
            if(len(trans)>0):
                flashCOMB+=g.get_tts(trans,lang='en')
            else:
                flashCOMB+=g.get_tts("No Translation",lang='en')
            
            #revert to english
            
            spoken_word=LH.tts(c)
            #spoken_word=g.get_tts(c,lang="en")
            flashCOMB+=spoken_word
            
        except Exception as e: 
            print(e)
            print("error",c,trans)
            
    if(make_video):
        import movie
        movie.slideshow_from_folder(filename+"\\",filename+".MP4")
    flashCOMB.export(g.send_folder+filename+"_flashcards.mp3", format="mp3")
    
    print("Finished Making",filename)

def render_word_by_word(filename,finalName,sourceLang=""):
    
    TEXT=open(textbin+filename,encoding='utf-8').read()

    phrases=text2phrases(TEXT,chinese=("zh" in sourceLang))
    
    print(phrases)
    
    if(sourceLang==""):

        from Text_Tools import get_language

        sourceLang=get_language(TEXT)

    print(filename,sourceLang)
    
    import wordTable
    WT=wordTable.wordTable(sourceLang)
    U=WT.unknown_words()
    
    biCOMB=AudioSegment.empty()
    monoCOMB=AudioSegment.empty()
    
    allWords=[]
    
    n=0
    
    percent=10
    
    for p in phrases:
        
        monoCOMB+=g.get_tts(p,lang=sourceLang)
        
        if(100*n/len(phrases)>=percent):
            print(str(percent)+"% done with "+finalName)
            
            percent+=10
        
        n+=1
        
        chunks=[]
        
        currentString=""
        
        unknown_words=[]
        
        phraseWords=[]

        if("zh" in sourceLang):
            
            phraseWords=p

        else:

            phraseWords=p.split(" ")

        for w in phraseWords:
            
            unknownWord=False
            
            if(w.lower() in U or w.lower() not in WT.words):
                if(wordTable.similar(w.lower(),g.trans(w,source_lang=sourceLang).lower())<0.7):
                
                    currentString+=w+" "

                    chunks.append(currentString)
                    chunks.append(w)
                    
                    if(w not in unknown_words):
                        
                        unknown_words.append(w)
                        
                    currentString=w+" "
                    
                    unknownWord=True

            if("'" in w):
                unknownWord=False
            
            if(not unknownWord):
                currentString+=w+" "
    
        if(len(currentString)>0):
            chunks.append(currentString)
            
        for i in range(len(chunks)):
            if(i%2==0):
                print(chunks[i])
                biCOMB+=g.get_tts(chunks[i],lang=sourceLang)
            else:
                trans=g.trans(chunks[i],source_lang=sourceLang)
                
                print(trans)
                
                biCOMB+=g.get_tts(trans)
        
    biCOMB.export(finalName+"_wbw.mp3", format="mp3")
    monoCOMB.export(finalName+"_mono.mp3", format="mp3")
    g.move_file(textbin+filename,"C:\\Users\\gpbla\\Desktop\\DesktopJunk\\finished_bilingual_audiobook"+"\\"+filename)

    '''
    np.random.shuffle(unknown_words)
    
    CARDS=AudioSegment.empty()
    for w in unknown_words:

        try:

            CARDS+=g.get_tts(g.trans(w,source_lang=sourceLang))
            CARDS+=g.get_tts(w,lang=sourceLang)

        except:

            None

    CARDS.export(finalName+"_words.mp3", format="mp3")
    
    '''
        
    print("Finished",filename)
    
                


def render_hints(filename,finalName,sourceLang="",maxHints=1):
    #TEXT=open(textbin+filename,encoding='utf-8').read()
    TEXT=open(textbin+filename,encoding='utf-8').read()
    
    phrases=text2phrases(TEXT)
    
    if(sourceLang==""):
        from Text_Tools import get_language

        sourceLang=get_language(TEXT)
            
    print(filename,sourceLang)
    
    hintCOMB=AudioSegment.empty()
    monoCOMB=AudioSegment.empty()
    
    
    allWords=[]
    
    for i in range(len(phrases)):
        
        for w in phrases[i].lower().split(" "):
            if(w not in allWords):
                allWords.append(w)
                
    import wordTable as wt
    WT=wt.wordTable(sourceLang)
    Unknown=WT.unknown_words(new_words=allWords)
    #print(Unknown)
    
    hint_matrix=np.zeros((len(phrases),len(Unknown)))
    for i in range(len(phrases)):
        p=phrases[i]
        tempWords=p.lower().split(" ")
        for j in range(len(Unknown)):
            if(Unknown[j] in tempWords):
                hint_matrix[i][j]=1
                
    for j in range(len(Unknown)):
        sum=1
        for i in range(len(phrases)):
            if(hint_matrix[i][j]==1):
                hint_matrix[i][j]=sum
                sum+=1
            
    #plt.figure(figsize=(10,10))
    #plt.imshow(np.log(hint_matrix+1))
    #plt.show()
        
    
    for i in range(len(phrases)):
    #for i in range(10):
        print(i/len(phrases))
        
        if(len(phrases[i])>0):
            
            hintWords=[]
            
            for j in range(len(Unknown)):
                if(len(hintWords)<=maxHints):
                    if(hint_matrix[i][j]>0):
                        hintWords.append(Unknown[j])
                
            if(len(hintWords)>=maxHints):
                trans=g.trans(phrases[i],source_lang=sourceLang)
                if(len(trans)>0 and len(phrases[i])>0):
                    hintCOMB+=g.get_tts(trans,lang='en')
            
            else:
                for hint in hintWords:
                    #make hint
                    try:                    
                        trans=g.trans(hint,source_lang=sourceLang)
                        hintCOMB+=g.get_tts(trans,lang='en')
                        hintCOMB+=g.get_tts(hint,lang=sourceLang)
                    except Exception as e: 
                        print(e)
                        print("could not translate",hint)

            
                
            targetAudio=g.get_tts(phrases[i],lang=sourceLang)
                
            hintCOMB+=targetAudio 
            monoCOMB+=targetAudio
                
    hintCOMB.export(finalName+"_hint.mp3", format="mp3")
    monoCOMB.export(finalName+"_mono.mp3", format="mp3")
    
    make_flashcards(TEXT,sourceLang,filename)
        
    g.move_file(textbin+filename,"C:\\Users\\gpbla\\Desktop\\DesktopJunk\\finished_bilingual_audiobook\\"+filename)
    
    upload_to_lingq(TEXT,sourceLang,filename)

    print("Finished",filename)


def video_examples(cards,sourceLang,filename):
    
    import text2Image
    import PIL
    
    import wordTable as wt
    import numpy as np
    
    WT=wt.wordTable(sourceLang)
    phrases=WT.load_corpus()
    #print(phrases)
    np.random.shuffle(phrases)
    hereAreSomeExamples=g.get_tts("Here are some examples",lang='en')
    
    flashCOMB=AudioSegment.empty()
    
    from Reverso import reverso_get_translations
    from Reverso import get_reverso_examples

    for c in cards:
        try:
            
            trans=""
            for t in reverso_get_translations(c,sourceLang)[0:5]:
                trans+=t+", "
                
            if(len(trans)==0):
                trans=g.trans(c,source_lang=sourceLang)

            print(c,trans)
            #trans=g.trans(c,source_lang=sourceLang)
            if(len(trans)>0):
                flashCOMB+=g.get_tts(trans,lang='en')
                flashCOMB+=g.get_tts(c,lang=sourceLang)
            examples=[]
            for p in phrases:
                if(c in p.lower().split(" ") and len(examples)<5):
                    if(p not in examples):
                        examples.append(p)
            
            if(len(examples)<5):
                e,t=get_reverso_examples(c,sourceLang,maxExamples=5-len(examples))
                examples.extend(e)
            
            if(len(examples)>0):
                flashCOMB+=hereAreSomeExamples
                N=0
                for e in examples:
                    print(c,e)
                    if(N>0):
                        flashCOMB+=g.get_tts(c,lang=sourceLang)
                    N+=1
                    trans=g.trans(e,source_lang=sourceLang)
                    image=text2Image.top_bottom(e,trans,size=(800,400))
                    
                    plt.imshow(image)
                    plt.show()
                    image.save("Video_slideshow_temp\\TEMP"+str(N)+".jpg")
                    
                    tempAudio=g.get_tts(trans,lang='en')+g.get_tts(e,lang=sourceLang)
                    tempAudio.export("Video_slideshow_temp\\TEMP"+str(N)+".mp3")

                    flashCOMB+=tempAudio
                    
            else:
                print("no example!!",c)
            
        except Exception as e: 
            print(e)
            print("error",c,trans)
            
    print("1")

    flashCOMB.export(g.send_folder+filename+"_flashcards.mp3", format="mp3")
    
def render_verbs(verb,lang):
    from pydub import AudioSegment
    
    biCOMB=AudioSegment.empty()
    monoCOMB=AudioSegment.empty()
    
    conjugations_examples=all_verb_conjugations(verb,lang)
    
    matrix=phrase_matcher(conjugations_examples)
    
    plt.imshow(matrix)
    plt.show()
    
    
    #mylist = [mylist[i] for i in myorder]
    
    perm=sortArray(matrix).astype(int)
    conjugations_examples=[conjugations_examples[i] for i in perm]
    
    for example in conjugations_examples:
        print(example)
        t=g.trans(example,source_lang=lang)
        biCOMB+=g.get_tts(t,lang='en')
        
        target=g.get_tts(example,lang=lang)
        biCOMB+=target
        monoCOMB+=target
        
    biCOMB.export(r"C:\Users\gpbla\Desktop\toEmail\\"+verb+"_examples_bi.mp3", format="mp3")
    monoCOMB.export(r"C:\Users\gpbla\Desktop\toEmail\\"+verb+"_examples_mono.mp3", format="mp3")

def render_verb_examples(verb,lang):
    
    from pydub import AudioSegment
    
    biCOMB=AudioSegment.empty()
    
    conjugations_examples=all_verb_conjugations(verb,lang)
    
    for example in conjugations_examples:
        t=g.trans(example,source_lang=lang)
        biCOMB+=g.get_tts(t,lang='en')
        biCOMB+=g.get_tts(example,lang=lang)

    from Reverso import get_reverso_examples
    
    for example in conjugations_examples:
        
        target,trans=get_reverso_examples(example,lang)
        
        if(len(target)>0):
                
            print(trans,target)
            
            t=g.trans(example,source_lang=lang)
            biCOMB+=g.get_tts(t,lang='en')
            biCOMB+=g.get_tts(example,lang=lang)
            
            target=target[0]
            trans=trans[0]
            
            biCOMB+=g.get_tts(trans,lang='en')
            biCOMB+=g.get_tts(target,lang=lang)
        
    biCOMB.export(r"C:\Users\gpbla\Desktop\toEmail\\"+verb+"_examples.mp3", format="mp3")