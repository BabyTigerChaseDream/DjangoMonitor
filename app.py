from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'hello docker  '+socket.gethostbyname(socket.gethostname())

@app.route('/health_check')
def health():
    return 'ok'

def runScheduler():
    bugCommand = 'python bug/scheduler.py >bug/log.txt 2>bug/error.txt &'
    expCommand = 'python experiment/scheduler.py >experiment/log.txt 2>experiment/error.txt &'
    notificationCommand = 'python notification/scheduler.py >notification/log.txt 2>notification/error.txt &'
    os.system(bugCommand)
    os.system(expCommand)
    os.system(notificationCommand)


if __name__ == '__main__':
    #runScheduler()
    app.run(host='0.0.0.0')
