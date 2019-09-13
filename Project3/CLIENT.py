import numpy as mypy
import threading
import time
import random
import hmac
import sys
import errno

import socket as mysoc

def client():
    try:
        ctors=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
   
# Define the port on which you want to connect to the server
    port = 35765
    
    #sa_sameas_myaddr = mysoc.gethostbyname(sys.argv[1])
    #mysoc.gethostbyname(mysoc.gethostname())
    host_name = mysoc.gethostname()
    print("[C] host name in client is ", host_name)
    #print("[C] ip address in client is ", sa_sameas_myaddr)
# connect to the server on local machine
# connect to the server on local machine
    #server_binding=(sa_sameas_myaddr,port)
    server_binding=(host_name,port)
    ctors.connect(server_binding)
    
    hostName1 = 'cpp.cs.rutgers.edu'
    hostName2 = 'java.cs.rutgers.edu'
    
    time.sleep(0.01)
    
    try:
        TLDS_connect1=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    
    server_binding001=(hostName1,36655)
    TLDS_connect1.connect(server_binding001)
    
    time.sleep(0.005)
    
    try:
        TLDS_connect2=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    
    server_binding002=(hostName2,43954)
    TLDS_connect2.connect(server_binding002)
    
    msg = 'PROJ3-HNS.txt'
    #ready to write in output file
    f = open('RESOLVED.txt','w')
    
    #i = 0
    with open(msg,'r') as file:
        #start to read request line by line
        for line in file:
            #create a digest for every line and for each line send it to AS and ask for TLDS host name
            #print ("[C] : currently at ->", i, line)
            #i = i + 1
            array003 = line.split()
            challengeString = array003[1]
            keyString = array003[0]
            hostNameFromTable = array003[2]
            
            digestT = hmac.new(keyString.encode(), challengeString.encode("utf-8"))
            stringSend = digestT.hexdigest() + ' ' + challengeString
            ctors.send(stringSend.encode('utf-8'))
                        
            #listen or not?
            stringRecv = ctors.recv(3074).decode('utf-8')
            print ("[C] : stringRecv from AS -> ", stringRecv)
            
            splitString = stringRecv.split()
            hostNameFromTLDS = splitString[0]
            
            if '\n' in hostNameFromTLDS:
                hostNameFromTLDS = hostNameFromTLDS[:-1]
           
            writeOn = ''
           
            if hostNameFromTLDS == hostName1:
                TLDS_connect1.send(hostNameFromTable.encode('utf-8'))
                writeOn = TLDS_connect1.recv(3074).decode('utf-8')
                print ("[C] : recv from TLDS - 1 ->", writeOn)
            elif hostNameFromTLDS == hostName2:
                TLDS_connect2.send(hostNameFromTable.encode('utf-8'))
                writeOn = TLDS_connect2.recv(3074).decode('utf-8')
                print ("[C] : recv from TLDS - 2 ->", writeOn)

            if "\n" in writeOn:
                writeOn = writeOn[:-1]
            f.write(hostNameFromTLDS + ' ' + writeOn)
            f.write('\n')
     
    f.close()
   # file.close()?????
    
# close the cclient socket 
    ctors.close()
    TLDS_connect1.close()
    TLDS_connect2.close()
    exit()
    
t3 = threading.Thread(name='client', target=client)
t3.start()

input("Hit ENTER  to exit\n")

