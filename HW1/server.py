import numpy as mypy
import threading
import time
import random

import socket as mysoc
#import client

def reverseString(strz):
  if strz == "\n" or strz == "":
    client.globalBoolVar = False
    return
  
  #remove '\n'
  if strz[len(strz)-1] == '\n':
    str1 = strz[0:len(strz)-1]
  
  chars = list(str1)
  for i in range(len(str1)//2):
    tmp = chars[i]
    chars[i] = chars[len(str1)-i-1]
    chars[len(str1)-i-1] = tmp
    
  outputStr = ''.join(chars)
  return outputStr

def server():
    try:
        ss=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    server_binding=('',50004)
    ss.bind(server_binding)
    ss.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)
    #send a intro  message to the client.  
    msg="Welcome to CS 352"
    csockid.send(msg.encode('utf-8'))
  
#Q2 - recv string
    while client.globalBoolVar == True:

      stringIN = csockid.recv(1024).decode('utf-8')
      if stringIN == "":
        break
      else:
        print("[S]: Receive request from the connect client: ", stringIN[0:len(stringIN)-1])
        stringOut002 = reverseString(stringIN)
        csockid.send(stringOut002.encode('utf-8'))

   # Close the server socket
    ss.close()
    exit()
    

t1 = threading.Thread(name='server', target=server)
print("SERVER START")
t1.start()
time.sleep(random.random()*5)
#t2 = threading.Thread(name='client', target=client.client)
#print("CLIENT START")
#t2.start()
  
input("Hit ENTER  to exit")

exit()


