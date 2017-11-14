import nltk
from nltk.stem.lancaster import LancasterStemmer 
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import operator
import urllib2
import json
from random import shuffle

stopWordList = stopwords.words('english') + ["?","'s","'ll","n't", "'re"]

def getWordList(coreWords, allWords, entries):
    internet = False
    synAnt = getAntSyn(coreWords)
    shuffle(synAnt)
    topWords = getCooccurWords(coreWords, allWords, entries)
    if (internet):
        w2vs = checkWord2Vec(coreWords)
        shuffle(w2vs)
    #DictPi?
    
        wordList = list(set( synAnt[:10] + w2vs[:10] + topWords[:10] ))
    else:
        wordList = list(set( synAnt[:10] + topWords[:10] ))
        
    wordList = [a for a in wordList if a not in coreWords and '_' not in a]
    print allWords
#    print 'start'
#    wordList = [a for a in wordList if a in allWords]
#    print 'end'
    return wordList

#Get all words, and counts from an array of text data
def getCorpus(entries):
    allWords={}
    for entry in entries: 
        for word in nltk.word_tokenize(entry):
            word = word.lower()
            if word not in stopWordList and ":" not in word and "*" not in word:
                if word not in allWords:
                    allWords[word]=1
                else:
                    allWords[word]+=1
    return allWords

#Returns an array with the words most often seen with coreWords list
def getCooccurWords(coreWords, allWords, entries):
    newData=[];
    allWords={}
    for entry in entries:
        if (calculateScore(entry,coreWords) > 0):
            properNouns=[word for word,pos in pos_tag(nltk.word_tokenize(entry)) if pos == 'NNP']
            newData.append(entry)
            for word in nltk.word_tokenize(entry):
                if word.lower() not in stopWordList and word not in properNouns and len(word)>2 and ":" not in word and "*" not in word:
                    lword=word.lower()
                    if lword not in allWords.keys():
                        allWords[lword]=1.0
                    else:
                        allWords[lword]+=1.0
    return [d[0].lower() for d in list(reversed(sorted(allWords.items(), key=operator.itemgetter(1) )))]

#Calculates a relevance score for a sentance given coreWords
def calculateScore(sentance, coreWords, allWords=None):
    score = 0
    st = LancasterStemmer()
    boldWords=set()
    coreWordsStem = [st.stem(word) for word in coreWords]
    for word in nltk.word_tokenize(sentance):
        stword= st.stem( word.lower() )
        if stword in coreWordsStem:
            boldWords.add(word.lower())
            if allWords:
                score+=1.0/allWords[word]
            else: 
                score += 1
    return score, boldWords

#Returns antonyms and synonyms for coreWords, and ensures ant/syn are in allWords
def getAntSyn(coreWords):
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
            if item not in synAnt and '_' not in item:
                synAnt.append(item.lower())
    return synAnt

def checkWord2Vec(coreWords):
    words=[]
    for word in coreWords:
        data = json.load(urllib2.urlopen("https://h2.rare-technologies.com/w2v/most_similar?positive%5B%5D="+word) )
        for pair in data['similars']:
            if pair[0] not in words:
                words.append(pair[0].lower())
    return words

##Old
#Returns an array with the words most often seen with coreWords list
def getTopWords(coreWords, entries):
    newData=[];
    allWords={}
    for entry in entries:
        if (calculateScore(entry,coreWords) > 0):
            properNouns=[word for word,pos in pos_tag(nltk.word_tokenize(entry)) if pos == 'NNP']
            newData.append(entry)
            for word in nltk.word_tokenize(entry):
                if word.lower() not in stopWordList and word not in properNouns and len(word)>2 and ":" not in word and "*" not in word:
                    lword=word.lower()
                    if lword not in allWords.keys():
                        allWords[lword]=1.0
                    else:
                        allWords[lword]+=1.0
    return reversed(sorted(allWords.items(), key=operator.itemgetter(1) ))
#if __name__ == "__main__":
#    print 'go'
#    print checkWord2Vec('friend')
                