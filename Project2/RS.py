import  numpy as mypy
import threading
import time
import random
import sys

import socket as mysoc

def server():
    try:
        rsconnect=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        #print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',54667)
    rsconnect.bind(server_binding)
    rsconnect.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=rsconnect.accept()
    print ("[S]: Got a connection request from a client at", addr)
    
    #connect to the 2 other server
    comIPaddr = sys.argv[1]
    eduIPaddr = sys.argv[2]
    RS_DNStable = sys.argv[3]
    
    try:
        comConnect=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    try:
        eduConnect=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
           
# connect to the other two server
    server_binding01=(comIPaddr,50015)#com
    comConnect.connect(server_binding) 
    
    server_binding02=(eduIPaddr,50012)#edu
    eduConnect.connect(server_binding02)
    
    while True:
        
        # receive a string contain hostname from the client
        hostNameStr = csockid.recv(3074).decode('utf-8')
        #print("receive a line from client: ",hostNameStr)
    
        if hostNameStr == "":
            #print ("finished")
            break;
        else:
            #RS does a look up in the DNS_table
            #if there is a match, sends the entry as a string "Hostname IPaddess A"

            #read the DNS_table 
            sendBackMsg = "?"

            with open(RS_DNStable, 'r') as DNSfile:
                for line in DNSfile:
                    breakIntoArray = line.split()

                    if breakIntoArray[2] == "NS":#??????????
                        
                        NSname = line
                        #just in case if the TS server name is not in stored in the last line 
                        #of the DNSTS_table

                    if breakIntoArray[0] == hostNameStr:
                        sendBackMsg = line
                        csockid.send(sendBackMsg.encode('utf-8'))
                        break

                #else sends the name os the TS server as a string "TSHostname - NS"
                    #when reach the end of DNSfile
                if(sendBackMsg == "?"):
                    
                    if(reciArray[:-4] == '.com'):
                        comConnect.send(hostNameStr.encode('utf-8'))
                        returnstr = comConnect.recv(3074).decode('utf-8')
                        csockid.send(returnstr.encode('utf-8'))

                    elif(reciArray[:-4] == '.edu'):
                        eduConnect.send(hostNameStr.encode('utf-8'))
                        returnstr = eduConnect.recv(3074).decode('utf-8')
                        csockid.send(returnstr.encode('utf-8'))
                        
            DNSfile.close()
            
            
    
    csockid.close()
    comConnect.close()
    eduConnect.close()
    exit()


t2 = threading.Thread(name='server', target=server)
t2.start()
time.sleep(random.random()*5)










