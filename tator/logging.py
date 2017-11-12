from datetime import datetime

def logThis(String):
    file = open("log.txt","a") 
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file.write(ts + ' ' + String + "\n") 
    file.close() 