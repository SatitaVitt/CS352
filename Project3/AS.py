import  numpy as mypy
import threading
import time
import random

import socket as mysoc

def server():
    
    TLDS1host = "cpp.cs.rutgers.edu"
    TLDS2host = "java.cs.rutgers.edu"
    
    try:
        rssd=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        #print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
        
    server_binding=('',35765)
    rssd.bind(server_binding)
    rssd.listen(1)
    host=mysoc.gethostname()
    localhost_ip=(mysoc.gethostbyname(host))
    csockid,addr=rssd.accept()
    
    try:
        TLDS1_connection=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    
    server_binding001=(TLDS1host,43667)
    TLDS1_connection.connect(server_binding001)
    
    try:
        TLDS2_connection=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    
    server_binding002=(TLDS2host,54778)
    TLDS2_connection.connect(server_binding002)
    
    while True:
        print ("start over")
        # receive a string contain digest and challenge string from the client
        D_C = csockid.recv(3074).decode('utf-8')
        print("receive a line from client: ",D_C)
        
        if D_C == "":
            break;
        else:
            #RS send only the Challenge string to 2 TLDS server
            array001 = D_C.split()
            digestFromClient = array001[0]
            
            TLDS1_connection.send(array001[1].encode('utf-8'))
            digest1 = TLDS1_connection.recv(3074).decode('utf-8')
            
            TLDS2_connection.send(array001[1].encode('utf-8'))
            digest2 = TLDS2_connection.recv(3074).decode('utf-8')
            
            print("digest got from TLDS1", digest1)
            print("digest got from TLDS2", digest2)
            
            if digest1 == digestFromClient:
                csockid.send(TLDS1host.encode('utf-8'))
                print ("[AS] : Here is a Match from TLDS1")
            elif digest2 == digestFromClient:
                csockid.send(TLDS2host.encode('utf-8'))
                print ("[AS] : Here is a Match from TLDS2")
            else:
                print ("[AS] : No Digest Match")
                csockid.send("No host - No Digest Match".encode('utf-8'))
                
                
    rssd.close()
    TLDS1_connection.close()
    TLDS2_connection.close()
    exit()

t2 = threading.Thread(name='server', target=server)
t2.start()
time.sleep(random.random()*5)