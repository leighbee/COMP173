#Leigh Baleja
#COMP 173 Lab 1
#April 21, 2016

import sys, socket

server = sys.argv[1]
port = int(sys.argv[2])
length = len(sys.argv) - 4
value = sys.argv[3]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(( server, port ))

b = bytearray(length + 2)  #initalize byte array

#operands
operand = sys.argv[3]
if operand == '+':
	b[0] = 0b00000001
if operand == '-':
	b[0] = 0b00000010
if operand == '*':
	b[0] = 0b00000100
#second byte is a count of int values that follow
b[1] = length

#iterate through the rest of the arguments
i = 0
tmp = 4 #start at the 5th argv
a = 2  #start adding to the byte array at position 2
if length%2 == 0: #IF ITS EVEN DO THIS STUFF
	#print("It was even")
	while i < length:  #iterate through the arguments
		upper = int(sys.argv[tmp]) << 4  #first argument
		lower = int(sys.argv[tmp+1])     #the second argument
		b[a] = upper | lower
		#print(b)
		a = a + 1
		i = i + 2
		tmp = tmp + 2
else:
	while i < length-1:
		upper = int(sys.argv[tmp]) << 4
		lower = int(sys.argv[tmp+1])
		b[a] = upper | lower
		#print(b)
		a = a + 1
		i = i + 2
		tmp = tmp + 2
	#handle last operand
	b[a] = int(sys.argv[tmp]) << 4

#send the values to the server for processing
s.sendall(b)

#getting data back from the server
data = bytearray(4)
s.recv_into(data)

x = data[0] << 24
x = x | (data[1] << 16)
x = x | (data[2] << 8)
x = x | data[3]
#print(data)

if x >= 2**31:
	x = x - 2**32

print(x)

s.close()
