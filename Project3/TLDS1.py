import numpy as mypy
import threading
import time
import random
import hmac
import errno

import socket as mysoc
#assume that sys.argv[1] = the table, sys.argv[2] = the key file

def TLDS1server():
  
    try:
        AS_connection=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
        
    AS_connection.bind(('', 43667))
    AS_connection.listen(1)
    host = mysoc.gethostname()
    localhost_ip=(mysoc.gethostbyname(host))
    ctsd,addr=AS_connection.accept()
    
    try:
        client_connection=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    server_binding=('',36655)
    client_connection.bind(server_binding)
    client_connection.listen(1)
    host=mysoc.gethostname()
    localhost_ip=(mysoc.gethostbyname(host))
    csockid,addr=client_connection.accept()
    
    ifconnected = 1
    
    
    
    while True:
        hnstring = ctsd.recv(3074).decode('utf-8')
        #print ("[TLDS1] : challenge string receive from AS ->", hnstring)
        #receive challenge string from AS

        if "\n" in hnstring:
            hnstring = hnstring[:-1]
        #if hnstring == "":
            #print ("[TLDS1] : hnstring == ""\n ")
        
        key_Table = open('PROJ3-KEY1.txt', 'r')
        for line in key_Table:
            if "\n" in line:
                line = line[:-1]
            key2 = line
            digest2 = hmac.new(key2.encode(), hnstring.encode("utf-8"))
            ctsd.send(digest2.hexdigest().encode('utf-8'))
            #print ("[TLDS1] : digest got ->", digest2.hexdigest())
            break
        #finish sending digest to AS, now wait for client to connect 
    
        if ifconnected == 1:
            csockid.setblocking(0)
            time.sleep(0.01)
            try:
                hnstring = csockid.recv(3074).decode('utf-8')
                #print ("[TLDS1] : recv from client ->", hnstring)
            except: 
                #print("did not connect to client")  
                continue

            if "\n" in hnstring:
                hnstring = hnstring[:-1]
        
            if hnstring == "":
                break
            else:
                found = False
   
                #TS_Table1 = open('PROJ3-TLDS1.txt','r')
                with open ('PROJ3-TLDS1.txt','r') as file:
                    for line in file:
                        array002 = line.split()
                        #print("[TS] compare with hostname: ", array002[0])
                        if array002[2] != 'A':
                            continue
                        if array002[0] == hnstring:
                            #print("we got it!!!: ", array002)
                            entry = line
                            csockid.send(entry.encode('utf-8'))
                            found = True
                            break

                    if found == False:
                        entry = "Error:HOST NOT FOUND."
                        csockid.send(entry.encode('utf-8'))
                            
    #TS_Table1.close()
    client_connection.close()
    # Close the server socket
    AS_connection.close() 
    exit()

t1 = threading.Thread(name='TLDS1server', target=TLDS1server)
t1.start()
time.sleep(random.random()*5)