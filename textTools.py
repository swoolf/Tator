import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import operator

#Get all words, and counts from an array of text data
def getCorpus(entries):
    allWords={}
    for entry in entries: 
        for word in nltk.word_tokenize(entry):
            if word not in ["?","'s"]:
                word.lower()
                if word not in allWords:
                    allWords[word]=1
                else:
                    allWords[word]+=1
    return allWords

def getTopWords(coreWords, entries):
    newData=[];
    allWords={}
#    cur = db.execute('select code, text from entries order by id')
#    entries = cur.fetchall()
    for entry in entries:
        if (calculateScore(entry,coreWords)):
            properNouns=[word for word,pos in pos_tag(nltk.word_tokenize(entry)) if pos == 'NNP']
            newData.append(entry)
            for word in nltk.word_tokenize(entry):
                if word not in stopwords.words('english') and word not in ["?","'s"] and word not in properNouns and len(word)>1:
                    lword=word.lower()
                    if lword not in allWords.keys():
                        allWords[lword]=1.0
                    else:
                        allWords[lword]+=1.0
    return reversed(sorted(allWords.items(), key=operator.itemgetter(1) ))
        
def calculateScore(sentance, coreWords):
    score = 0
    for word in nltk.word_tokenize(sentance):
        word.lower()
        if word in coreWords:
            score+=1
    return score
            
def getAntSyn(coreWords, allWords):
    print coreWords
    synAnt = []
    for word in coreWords:
        synonyms = []
        antonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name() )
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name() )
        for item in synonyms + antonyms:
            if item in allWords and item not in synAnt:
                synAnt.append(item)
    return synAnt
            
                