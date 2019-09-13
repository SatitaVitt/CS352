import numpy as mypy
import threading
import time
import random
import hmac
import errno

import socket as mysoc
#assume that sys.argv[1] = the table, sys.argv[2] = the key file

def TLDS2server():
  
    try:
        AS_connection=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
        
    AS_connection.bind(('', 54778))
    AS_connection.listen(1)
    host = mysoc.gethostname()
    localhost_ip=(mysoc.gethostbyname(host))
    ctsd,addr=AS_connection.accept()
    
    ifconnected = 1
    
    try:
        client_connection=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    server_binding=('',43954)
    client_connection.bind(server_binding)
    client_connection.listen(1)
    host=mysoc.gethostname()
    localhost_ip=(mysoc.gethostbyname(host))
    csockid,addr=client_connection.accept()    
    
    
    while True:
        hnstring = ctsd.recv(3074).decode('utf-8')
        print ("[TLDS2] : challenge string receive from AS ->", hnstring)
        #receive challenge string from AS

        if "\n" in hnstring:
            hnstring = hnstring[:-1]
        #if hnstring == "":
            #print ("[TLDS2] : hnstring == ""\n ")
     
        key_Table = open('PROJ3-KEY2.txt', 'r')
        for line in key_Table:
            if "\n" in line:
                line = line[:-1]
            key2 = line
            digest2 = hmac.new(key2.encode(), hnstring.encode("utf-8"))
                
            ctsd.send((digest2.hexdigest()).encode('utf-8'))
            print ("[TLDS2] : digest got ->", digest2.hexdigest())
            break
        #finish sending digest to AS, now wait for client to connect 
        
        if ifconnected == 0:
            try:
                client_connection=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
                #client_connection.setblocking(0)
            except mysoc.error as err:
                print('{} \n'.format("socket open error ",err))
    
            server_binding=('',43954)
            client_connection.bind(server_binding)
            client_connection.listen(2)
            host=mysoc.gethostname()
            #print("[S]: Server host name is: ",host)
            localhost_ip=(mysoc.gethostbyname(host))
            #print("[S]: Server IP address is  ",localhost_ip)
            #time.sleep(0.01)
    
            #try:
            csockid,addr=client_connection.accept()

        
        if ifconnected == 1:
            csockid.setblocking(0)
            time.sleep(0.01)
            try:
                hnstring = csockid.recv(3074).decode('utf-8')
                #print ("[TLDS2] : recv from client ->", hnstring)
            except:
                #print("did not connect to client")
                continue
        
            if "\n" in hnstring:
                hnstring = hnstring[:-1]
        
            if hnstring == "":
                break
            else:
                found = False
   
                #TS_Table2 = open('PROJ3-TLDS2.txt','r')
                with open('PROJ3-TLDS2.txt', 'r') as file:
                    for line in file:
                        print ("line --- ", line)
                        if line == '' or line == '\n':
                            print("meet eof")
                            break
                        array002 = line.split()
                        print("[TS] compare with hostname: ", hnstring)
                        if array002[2] != 'A':
                            continue
                        if array002[0] == hnstring:
                            entry = line
                            csockid.send(entry.encode('utf-8'))
                            found = True
                            break
                        
                    if found == False:
                        entry = "Error:HOST NOT FOUND."
                        csockid.send(entry.encode('utf-8'))
                

        
    #TS_Table2.close()
    client_connection.close()
    # Close the server socket
    AS_connection.close() 
    exit()

t1 = threading.Thread(name='TLDS2server', target=TLDS2server)
t1.start()
time.sleep(random.random()*5)