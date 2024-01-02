import socket
import threading



def request():
	host='localhost'
	port = 12345
	c_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	c_server.connect((host, port))
	while True:
		try:
			data=c_server.recv(1024)
			msg = data.encode('utf-8')
			if msg =="ACCPETED":
			  	chat(message)
			  	break
			else:
				  pass
		except:
		   		pass
		   		
def chat(message):    	
		    		
	  