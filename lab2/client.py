#client

import socket, sys, os

server = sys.argv[1]
port = int(sys.argv[2])
mode = sys.argv[3]
filename = sys.argv[4]

#connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect( (server, port) )

#recieve "READY" from server:
ready = s.recv(1024).decode("UTF-8")
#print("Ready status:", ready, "Sending: Mode:", mode, "Filename:", filename)

#THEN send <mode> <filename> to the server.
modefile = mode + " " + filename
s.send(modefile.encode("UTF-8"))

if(mode == "PUT"):  
	#recieve OK 
	OK = s.recv(1024).decode("UTF-8")
	#print("OK status: ", OK)

	#send number of bytes to server:
	size = os.path.getsize(filename)
	#print("Sending: ", filename, " filesize is", size)
	s.send(size.to_bytes(8, byteorder='big', signed=False)) 

	#recieve second OK
	OK2 = s.recv(1024).decode("UTF-8")
	print("client sending file " + filename + " (" + str(size) + " bytes)")
	f = open(filename, "rb") #open to read?
	while size > 0:
		data = f.read(1024)
		s.send(data)
		size -= len(data)
	f.close()
	#print("Sent the data")
elif(mode == "GET"):
	#recieve OK 
	OK = s.recv(1024).decode("UTF-8")
	#print("OK status: ", OK)
	
	#send ready
	#print("sending ready")
	s.send("READY".encode("UTF-8"))

	#recieve number of bytes from server:
	data = s.recv(8)
	size = int.from_bytes(data, byteorder='big', signed=False)
	#print("Recieved size:", size)
	
	#send OK
	#print("Sending OK again")
	s.send("OK".encode("UTF-8"))
	
	f = open(filename, "wb")
	#print("GET: getting data and writing it to file")
	print("client receiving file " + filename + " (" + str(size) + " bytes)")
	#loop and recieve data to write into file:
	while size > 0:
		#print("Recieving chunk:")
		data = s.recv(min(size, 1024))
		#print("Recieved", data)
		f.write(data)
		size -= len(data)
	f.close()
	#print("Written data")
elif(mode=="DEL"):
	print("client deleting file", filename)

done = s.recv(1024).decode("UTF-8")
#print("Recieved Done message: ", done)
print("Complete")
s.close()
