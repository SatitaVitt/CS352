import numpy as mypy
import threading
import time
import random
import ast

import socket as mysoc

globalBoolVar = True

def client():
    try:
        cs=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[C]: Client socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
        
  
# Define the port on which you want to connect to the server
    port = 50004             
    sa_sameas_myaddr =mysoc.gethostbyname(mysoc.gethostname())
# connect to the server on local machine
    server_binding=(sa_sameas_myaddr,port)
    cs.connect(server_binding) 
    data_from_server=cs.recv(100)
#receive data from the server 
  
    print("[C]: Data received from server::  ",data_from_server.decode('utf-8'))
    
 #question2
    fileOutput = open('HW1out.txt', 'w')

    with open('HW1test.txt', 'r') as myfile:
      inputFile = ""
      inputFile = myfile.readline()
      if inputFile == "" or inputFile == "\n":
          globalBoolVar = False
          
      while inputFile != "":
        #print("[C]: Client sent this string to Server and ask for reverse: ", inputFile)
        cs.send(inputFile.encode('utf-8'))
        
        thisStr = cs.recv(1024).decode('utf-8')
        print("[C]: Client receive from the server: ", thisStr)
        fileOutput.write(thisStr)
        fileOutput.write('\n')
        inputFile = myfile.readline()
        if inputFile == "" or inputFile == "\n":
          globalBoolVar = False
          
          fileOutput.close()
          myfile.close()
          break
      
# close the cclient socket 
    cs.close() 
    exit()   
    
t2 = threading.Thread(name='client', target=client)
print("CLIENT START")
t2.start()   
    
    
    
    
    
    
    
    
    