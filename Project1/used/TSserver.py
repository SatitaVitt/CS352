import numpy as mypy
import threading
import time
import random

import socket as mysoc

def TSserver():
    try:
        tssd=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    tssd.bind(('', 38692))
    tssd.listen(1)
    host = mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    ctsd,addr=tssd.accept()
    print ("[S]: Got a connection request from a client at", addr)
    TS_Table = open('PROJI-DNSTS.txt','r')
    while True:
        hnstring001 = ctsd.recv(3074).decode('utf-8')
        print("[1111] we got: ", hnstring001)

        #if hnstring001[len(hnstring001)] == '\n':
        #need to FIX - what if the string received doesn't have \n in the end, how do we determine
        hnstring = hnstring001[0:len(hnstring001)-1]
        
        print("[000] we got: ", hnstring)
        
        if hnstring == "":
            break
        else:
            entry = "?"
            print("[TS]: Receive a line: ", hnstring)
            for line in TS_Table:
                array002 = line.split()
                if array002[0] == hnstring:
                    print("we got it!!!: ", array002)
                    entry = line
                    ctsd.send(entry.encode('utf-8'))
                    break
                
            if entry == "?":
                entry = hnstring + " - Error:HOST NOT FOUND"
                ctsd.send(entry.encode('utf-8'))
                
            print("-----------------")
    
    # Close the server socket
    #tssd.close() 
    #exit()

t1 = threading.Thread(name='TSserver', target=TSserver)
t1.start()
time.sleep(random.random()*5)







