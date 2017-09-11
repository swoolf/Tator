import sqlite3
import xlrd
from flask import g, Blueprint
from flask import current_app as app

dataBase_funcs = Blueprint('dataBase_funcs', __name__,template_folder='templates')

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db(source=None):
    db = get_db()
    with dataBase_funcs.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    addData2DB(db, source)
    
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def addData2DB(db, source=None):
    textLen = 40
    if source=='parachute' or source==None :
        path = "tator/chelsea stuff/SCR wind testing timeline.xlsx"
        sheetNum=5
        colNum=2
        return addDataFormatted(db)
    elif source=='interlace':
        path = "tator/interlace/data.xls"
        sheetNum=0
        colNum=2
    data=[]
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(sheetNum)
    
    for rowidx in range(0,sheet.nrows):
        if sheet.cell_type(rowidx,colNum) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
            text = sheet.cell(rowidx,colNum).value
            textList = text.split()
            for i in range(len(textList)/textLen+1):
                data.append( ' '.join(textList[i*textLen:]) )
                
                db.execute('insert into entries (code, text, IDnum) values (?, ?,?)',
                     [" ", ' '.join(textList[i*textLen:(i+1)*textLen]) , rowidx])
                db.commit()
                
def addDataFormatted(db, source=None):
    textLen=40
    if source=='parachute' or source==None :
        path = "tator/chelsea stuff/all_data_parachute.xlsx"
        sheetNum=5
        colNum=0
    elif source=='interlace':
        path = "tator/interlace/data.xls"
        sheetNum=0
        colNum=2
    data=[]
    
    book = xlrd.open_workbook(path)
    for sheet in book.sheets():
        for rowidx in range(0, sheet.nrows):
            if sheet.cell_type(rowidx,colNum) not in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                text = sheet.cell(rowidx,colNum).value
                textList = text.split()
                for i in range(len(textList)/textLen+1):
                    data.append( ' '.join(textList[i*textLen:]) )

                    db.execute('insert into entries (code, text, IDnum) values (?, ?,?)',
                         [" ", ' '.join(textList[i*textLen:(i+1)*textLen]) , rowidx])
                    db.commit()
                
    