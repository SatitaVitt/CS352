import  numpy as mypy
import threading
import time
import random

import socket as mysoc

def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',48732)
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)
    
    # receive a string contain hostname from the client
    hostNameStr = csockid.recv(1024).decode('utf-8')
    
    if hostNameStr == "":
        print ("not a thing from client")
    else:
        print("[RS]: Receive request from the connect client: ", hostNameStr)
        #RS does a look up in the DNS_table
        #if there is a match, sends the entry as a string "Hostname IPaddess A"
        
        #read the DNS_table 
        sendBackMsg = "?"
        with open('PROJI-DNSRS.txt', 'r') as DNSfile:
            for line in DNSfile:
                breakIntoArray = line.split()
                print ("we are at :", breakIntoArray[0])
                

                if breakIntoArray[2] == "NS":
                    NSname = line
                    #just in case if the TS server name is not in stored in the last line 
                    #of the DNSTS_table

                if breakIntoArray[0] == hostNameStr:
                    #?
                    print ("found it!!! no need to go to TS!!")
                    sendBackMsg = line
                    csockid.send(sendBackMsg.encode('utf-8'))
                    break
                    
            #else sends the name os the TS server as a string "TSHostname - NS"
                #when reach the end of DNSfile
            if(sendBackMsg == "?"):
                print ("sorry, we need to go to TS....")
                sendBackMsg = NSname
                csockid.send(sendBackMsg.encode('utf-8'))

        DNSfile.close()
        #ss.close()
        #exit()


t2 = threading.Thread(name='RSserver', target=server)
t2.start()
time.sleep(random.random()*5)
