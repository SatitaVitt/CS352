import numpy as mypy
import threading
import time
import random

import socket as mysoc

def TSserver():
    try:
        tssd=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        #print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    tssd.bind(('', 50012))
    tssd.listen(1)
    host = mysoc.gethostname()
    #print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    #print("[S]: Server IP address is  ",localhost_ip)
    ctsd,addr=tssd.accept()
    #print ("[S]: Got a connection request from a client at", addr)
    
    while True:
        hnstring = ctsd.recv(3074).decode('utf-8')
        #print("[TTTS] Here we compare with ->", hnstring)
        
        if "\n" in hnstring:
            hnstring = hnstring[:-1]
        
        if hnstring == "":
            break
        else:
            found = False
            
            TS_Table = open('PROJI-DNSTS.txt','r')
            for line in TS_Table:
                if line 
                array002 = line.split()
                print("[TS] compare with hostname: ", array002[0])
                if array002[0] == hnstring:
                    print("we got it!!!: ", array002)
                    entry = line
                    ctsd.send(entry.encode('utf-8'))
                    found = True
                    break

            if found == False:
                entry = hnstring + " - Error:HOST NOT FOUND"
                ctsd.send(entry.encode('utf-8'))

        
    
    # Close the server socket
    tssd.close() 
    exit()

t1 = threading.Thread(name='TSserver', target=TSserver)
t1.start()
time.sleep(random.random()*5)







