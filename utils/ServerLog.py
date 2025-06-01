from datetime import datetime


def printInfoLog(line):
    now = datetime.now()
    print("[%s] [INFO    ] " % now.strftime('%Y-%m-%d %H:%M:%S'), end='')
    print(line)


def printErrorLog(line):
    now = datetime.now()
    print("[%s] [ERROR   ] " % now.strftime('%Y-%m-%d %H:%M:%S'), end='')
    print(line)
