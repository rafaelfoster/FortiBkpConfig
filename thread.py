#!/usr/bin/python


import threading

def f(id):
    print 'thread function %s\n' %(id)
    return

if __name__ == '__main__':
    for i in range(3):
        t = threading.Thread(target=f, args=(i,))
        t.start()

