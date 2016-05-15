#Leigh Baleja
#COMP 173 Lab 1
#April 21st, 2016

import sys, socket

port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind( ("", port) )    

while True:
	data, address = s.recvfrom(1024)
	#print("Recieved: ", data, "from ", address)

	#unpack the operand and length variables
	op = data[0]
	length = data[1]
	tmp = length
	#print("Length is:", length, "op is:", op)
	isEven = length %2 == 0
	if length%2 != 0:
		length = (length+1)//2
	else:
		length = length//2

	MASK_LOW = 0b00001111
	i = 2
	while i < length + 2:
		#print("i is", i, "tmp is", tmp,  "length is:", length, "isEven is: ", isEven)
		if (not isEven) and i == tmp:
			x = data[i] >> 4
			#print("Kinda special case hit")
			if op == 4:
				#print("Special special case hit")
				y = 1
			else:
				y = 0
		else: 
			x = data[i]  >> 4
			y = data[i] & MASK_LOW
		#print("processing:", x, y)
		if i == 2:
			result = x
		if op == 1:
			if i == 2:
				result = result + y
			else:
				result = result + x + y
		elif op == 2:
			if i == 2:
				result = result - y
			else:
				result = result - x - y
		else:
			if i == 2:
				result = result * y
			else:
				result = result * x * y
		#print("Temp result: ",result)
		i = i + 1
	#print("Final result:", result)
	
	#packing the bits:
	tosend = bytearray(4)
	MASK_MSB = 0b11111111 << 24
	MASK_MIDLEFT = 0b11111111 << 16
	MASK_MIDRIGHT = 0b11111111 << 8
	MASK_LSB = 0b11111111
	tosend[0] = (result & MASK_MSB) >> 24
	tosend[1] = (result & MASK_MIDLEFT) >> 16
	tosend[2] = (result & MASK_MIDRIGHT) >> 8
	tosend[3] = (result & MASK_LSB)
	
	s.sendto(tosend, address) 		
	


