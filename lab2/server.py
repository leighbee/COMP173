#server

import socket, sys, os

port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( ("", port) )
s.listen(3)  #listen on all ports
#print("server waiting on port", port)
while True:
	#accept connection:
	conn, address = s.accept()
	#send a ready command
	conn.send("READY".encode("UTF-8"))
	#print("Sent 'SERVER READY'")

	#receive string with mode and filename:
	modefile = conn.recv(1024).decode("UTF-8")
	
	#need to SPLIT the mode and file string up here.....
	dataArray = modefile.split()
	mode = dataArray[0]
	filename = dataArray[1]
	#print("Mode: " + mode + " Filename: " + filename)
	
	#IF STATEMENTS BELOW:
	if(mode=="PUT"):
		#send an OK message:
		#print("Sending an OK message")
		conn.send("SERVER OK".encode("UTF-8"))

		#recieve the number of bytes (size)
		data = conn.recv(8)
		size = int.from_bytes(data, byteorder='big', signed=False)
		#print("Recieved size:", size)
		
		#Send back another OK in response: 
		conn.send("OK".encode("UTF-8"))
		
		#open the file to WRITE to it: 
		f = open(filename, "wb")
		
		#write to the file:
		#print("PUT: recieving data and writing to file:")
	
		#loop and recieve the data to write into the new file
		while size > 0:
			data = conn.recv(1024)
			f.write(data)
			size -= len(data)
		f.close()
		#print("Written data")
	elif(mode=="GET"):
		#send an OK message:
		#print("Sending an OK message")
		conn.send("OK".encode("UTF-8"))
		
		#recv ready message
		ready = conn.recv(1024).decode("UTF-8")
		#print("Recieved ready message: ", ready)

		#SEND NUMBER OF BYTES
		size = os.path.getsize(filename)
		#print("Sending: ", filename, " filesize is", size)
		conn.send(size.to_bytes(8, byteorder='big', signed=False))
		
		#recieve OK message
		OK = conn.recv(1024).decode("UTF-8")
		
		f = open(filename, "rb")   
		#print("GET: reading file and sending the data to client")

		#loop and send the data to the client
		while size > 0:
			#print("Sending chunk")
			data = f.read(1024)
			conn.send(data)
			#print("Sent", data)
			size -= len(data)    
		f.close()	
	elif(mode=="DEL"):
		#print("DEL FILE: ", filename)
		os.remove(filename)
	
	#send done, close connection with client. 
	conn.send("DONE".encode("UTF-8"))
	conn.close()
