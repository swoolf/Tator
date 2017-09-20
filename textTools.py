import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import operator

stopWordList = stopwords.words('english') + ["?","'s","'ll","n't", "'re"]

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

#Calculates a relevance score for a sentance given coreWords
def calculateScore(sentance, coreWords, allWords=None):
    score = 0
    for word in nltk.word_tokenize(sentance):
        word= word.lower()
        if word in coreWords:
            if allWords:
                score+=1.0/allWords[word]
            else: 
                score += 1
    return score

#Returns antonyms and synonyms for coreWords, and ensures ant/syn are in allWords
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
            if item in allWords and '_' not in item and item not in synAnt and item not in coreWords:
                synAnt.append(item)
    return synAnt
            
                