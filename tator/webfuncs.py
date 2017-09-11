from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, make_response, Blueprint
from flask import current_app as app
from dataBase import *
import nltk
import textTools
import StringIO
import csv 
import re
    
web_funcs = Blueprint('web_funcs', __name__,template_folder='templates')

newWords=[]
coreWords=[]
codeName='code'
wordCount=0
#allWords={}

#Download current DB into a csv
@web_funcs.route('/download')
def post():
    db=get_db()
    cur = db.execute('select text, code from entries order by id')
    entries=[]
    csvList=[["this"],'is','a','test']
    si = StringIO.StringIO()
    cw = csv.writer(si)
    for entry in cur.fetchall():
        entries.append([entry[0]])
        print [entry]
        try:
            cw.writerows( [entry] )
        except:
            txt= re.sub(u"\u2014", "-", entry[0] )
            txt = re.sub(u"\u2019", "'", txt )
            cw.writerows( [ [txt], [entry[1]] ] )
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=tator_data.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    
#Pointer to a generate a new code
@web_funcs.route('/newCode')
def newCodePage():
    return render_template('newCode.html')

#Given a few key words, generate list of new words to present to user
@web_funcs.route('/test', methods=['GET', 'POST'])
def getWordList():
    global newWords, coreWords, codeName, wordCount#, allWords
    wordCount=0
    codeName=request.form['data2']
    coreWords = nltk.word_tokenize(request.form['data1'])
    db=get_db()
    cur = db.execute('select text from entries order by id')
    entries=[]
    for entry in cur.fetchall():
        entries.append(entry[0])
    #Get 15 most common words
    allWords = textTools.getCorpus(entries)
    newWords = textTools.getAntSyn(coreWords, allWords)
    for d in textTools.getTopWords(coreWords, entries):
        if d[0] not in newWords and d[0] not in coreWords:
            newWords.append(d[0])
    newWords=newWords[:15]+['3nd']#########
    print newWords
    return nextWord()

#Present next word to user [Need to do in JS!]
@web_funcs.route('/nextWord', methods=['GET', 'POST'])
def nextWord():
    global coreWords, newWords, wordCount
    if request.method == 'POST' and request.form['data1'] == "yes":
        coreWords.append(newWords[wordCount-1])
    print coreWords
    wordCount+=1
    if newWords[wordCount-1] == "3nd":
        #Code Doc and Return to Main
        codeDoc()
    return newWords[wordCount-1]

#Show entries to user
@web_funcs.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select code, text, IDnum from entries order by id')
    entries = cur.fetchall()
    cur = db.execute('SELECT code, words from codes')
    codes = cur.fetchall()
    return render_template('show_entries.html', entries=entries, codes=codes)

#Page for user to choose data and upload their own data
@web_funcs.route('/chooseData')
def chooseData():
    db = get_db()
    cur = db.execute('select code, text, IDnum from entries order by id')
    entries = cur.fetchall()
    cur = db.execute('SELECT code, words from codes')
    codes = cur.fetchall()
    return render_template('chooseData.html', add=False)

#Initialize database
@web_funcs.route('/initData', methods=['POST'])
def initData():
    if request.form['data']=='add':
        return render_template('chooseData.html', add=True)
    init_db(source=request.form['data'])
    return redirect(url_for('web_funcs.show_entries'))
    
#Given coreWords, code document. 
def codeDoc():
    global coreWords, codeName#, allWords
    db=get_db()
    db.execute('INSERT into codes (code, words) values (?,?)',[codeName,' '.join(coreWords)])
    db.commit()
    cur = db.execute('select code, text, id from entries')
    rows=cur.fetchall()
    
    cur = db.execute('select text from entries order by id')
    entries=[]
    for entry in cur.fetchall():
        entries.append(entry[0])
    allWords = textTools.getCorpus(entries)
    
    for row in rows:
        score = textTools.calculateScore(row[1], coreWords, allWords)
        if score > 0: 
            db.execute('UPDATE entries SET code = ? WHERE id = ?', [codeName,row[2]])
            db.commit()
    flash('New Code Entered')

#Clear codes from document
@web_funcs.route('/clearCodes', methods=['POST'])
def clearCodes():
    db=get_db()
    db.execute('UPDATE entries SET code=?',[' ']) 
    db.execute('DELETE FROM codes')
    db.commit()
    print("Clear Codes")
    return redirect(url_for('web_funcs.show_entries'))

#Show only sentances for a specific code [update in JS!]
@web_funcs.route('/sortByCode', methods=['POST'])
def sortByCode():
    print "Sort By Code"
#    return redirect(url_for('show_entries'))
    db = get_db()
    if request.form['choice'] != 'none':
        cur = db.execute('select code, text, IDnum from entries where code = ?', [request.form['choice']] )
        entries = cur.fetchall()
    else:
        cur = db.execute('select code, text, IDnum from entries order by id')
        entries = cur.fetchall()
    cur = db.execute('SELECT code, words from codes')
    codes = cur.fetchall()
    return render_template('show_entries.html', entries=entries, codes=codes)

#User Login
@web_funcs.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('web_funcs.show_entries'))
    return render_template('login.html', error=error)

#User Logout
@web_funcs.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('web_funcs.show_entries')) 

######################################
#???Old implementation, I think
#@web_funcs.route('/add', methods=['POST'])
#def newCode_entry():
#    print 'add'
#    db=get_db()
#    wordBank=[]
#    for word in nltk.word_tokenize(request.form['Words']):
#        wordBank.append(word)
#    cur = db.execute('select code, text, id from entries')
#    rows=cur.fetchall()
#    for row in rows:
#        for word in nltk.word_tokenize(row[1]):
#            if word in wordBank:
#                db.execute('UPDATE entries SET code = ? WHERE id = ?', [request.form['codeID'],row[2]])
#                db.commit()
#                break
#    print(wordBank)
#    db.execute('INSERT into codes (code, words) values (?,?)',[request.form['codeID'],' '.join(wordBank)])
#    db.commit()
#    cur = db.execute('select code, words, id from codes')
#    rows=cur.fetchall()
#    print rows
#    flash('New Code Entered')
#    return redirect(url_for('show_entries'))
