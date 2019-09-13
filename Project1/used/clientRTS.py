import numpy as mypy
import threading
import time
import random

import socket as mysoc

def client():
    try:
        ctors=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    try:
        ctots=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
        
  
# Define the port on which you want to connect to the server
    port = 48732
    sa_sameas_myaddr =mysoc.gethostbyname(mysoc.gethostname())
    host_name = mysoc.gethostname()
    print("[C] host name in client is ", host_name)
    print("[C] ip address in client is ", sa_sameas_myaddr)
# connect to the server on local machine
    server_binding=(sa_sameas_myaddr,port)
    ctors.connect(server_binding) 
    
    msg='PROJI-HNS.txt'
    
    f = open('RESOLVED.txt','w')
    with open(msg,'r') as file:
        for line in file:
            print ("what we got from proji-hns.txt: ", line)
            ctors.send(line.encode('utf-8'))
            
            r = ctors.recv(3074).decode('utf-8')
            print("[C] write: ", r)
            array001 = r.split()
            print ("[ClientRTS]: ", array001)
            
            if array001[2]=="A":
                f.write(r)
                f.write('\n')
            else:
                #connect to TS
                port=38692
                print ("hostname got from RS server: ", array001[0])
                server_binding=(array001[0],port)
                ctots.connect(server_binding)
                ctots.send(line.encode('utf-8'))
                s = ctots.recv(3074).decode('utf-8')
                print("receive from TS: ", s)
                f.write(s)
                f.write('\n')
                
            
    #f.write('\n')
    #f.write(s)
    ctots.close()        
    file.close()
    
    
    
    #f.write(s)
    f.close()
    
# close the cclient socket 
    ctors.close() 
    exit() #??
    
t3 = threading.Thread(name='client', target=client)
t3.start()

input("Hit ENTER  to exit")

exit()