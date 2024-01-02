from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import TwoLineAvatarListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import os
import threading as th
import socket

kv = """
MDNavigationLayout:
	ScreenManager:
		id:screen
		Screen:
			name:"main"
			ScrollView:
				size_hint_y:0.85				
				pos_hint:{"center_x":0.63,"center_y":0.5}
				BoxLayout:
					orientation:"vertical"
					spacing:"19sp"		
					MDCard:
						size_hint:0.6,0.13
						radius:[60]
						elevation:4
						md_bg_color:200/255,240/255,220/255
						on_release:app.change_screen("file"),app.info("self.add")
						MDLabel:
							text:"File access"
							pos_hint:{"center_x":0.5,"center_y":0.5} 
							halign:"center"
							bold:True
							font_size:"32sp"
					MDCard:
						size_hint:0.6,0.13
						radius:[60]
						elevation:4
						md_bg_color:200/255,240/255,220/255
						on_release:app.change_screen("edit"),app.info("self.add_edit")
						MDLabel:
							text:"Edit File"
							pos_hint:{"center_x":0.5,"center_y":0.5} 
							halign:"center"
							bold:True
							font_size:"32sp"
					MDCard:
						size_hint:0.6,0.13
						radius:[60]
						md_bg_color:200/255,240/255,220/255
						on_release:app.change_screen("delete"),app.info("self.delete")
						elevation:4
						MDLabel:
							text:"Delete File"
							bold:True
							pos_hint:{"center_x":0.5,"center_y":0.5} 
							halign:"center"
							font_size:"32sp"
					MDCard:
						size_hint:0.6,0.13
						radius:[60]
						elevation:4
						md_bg_color:200/255,240/255,220/255
						on_release:app.change_screen("run")
						MDLabel:
							text:"Run File"
							bold:True
							pos_hint:{"center_x":0.5,"center_y":0.5} 
							halign:"center"
							font_size:"32sp"
		Screen:
			name:"file"
			MDTopAppBar:
				pos_hint:{"top":1}
				left_action_items:[["arrow-left", lambda x : app.change_screen("main")]]
			ScrollView:
				pos_hint:{"top":0.9}
				MDList:
					id:list
		Screen:
			name:"run"
			MDTopAppBar:
				pos_hint:{"top":1}
				left_action_items:[["arrow-left", lambda x : app.change_screen("main")]]
			MDRelativeLayout:
				id:tem_run
				MDRoundFlatButton:
					text:"Select Your File"
					pos_hint:{"center_x":0.5,"center_y":0.55}
					size_hint:0.25,0.08
					md_bg_color:0,153/255,1,1
					theme_text_color:"Custom"
					on_release:app.open_run()
					text_color:1,1,1,1
					font_size:"32sp"
				MDRoundFlatButton:
					text:"RUN"
					pos_hint:{"center_x":0.5,"center_y":0.35}
					size_hint:0.25,0.08
					md_bg_color:0,153/255,1,1
					theme_text_color:"Custom"
					on_release:app.runn()
					text_color:1,1,1,1
					font_size:"32sp"
		Screen:
			name:"runn"
			MDTopAppBar:
				pos_hint:{"top":1}
				left_action_items:[["arrow-left", lambda x : app.change_screen("edit")]]
			ScrollView:
				pos_hint:{"top":0.9}
				MDList:
					id:run_list
		Screen:
			name:"edit_folder"
			MDTopAppBar:
				pos_hint:{"top":1}
				left_action_items:[["arrow-left", lambda x : app.change_screen("edit")]]
			ScrollView:
				pos_hint:{"top":0.9}
				MDList:
					id:edit_list
		Screen:
			name:"delete"
			MDTopAppBar:
				pos_hint:{"top":1}
				left_action_items:[["arrow-left", lambda x : app.change_screen("main")]]
			ScrollView:
				pos_hint:{"top":0.9}
				MDList:
					id:del_list
		Screen:
			name:"edit"
			MDTopAppBar:
				pos_hint:{"top":1}
				left_action_items:[["arrow-left", lambda x : app.change_screen("main")]]
			MDRelativeLayout:
				id:tem
				MDRoundFlatButton:
					text:"Select Your File"
					pos_hint:{"center_x":0.5,"center_y":0.65}
					size_hint:0.25,0.08
					md_bg_color:0,153/255,1,1
					theme_text_color:"Custom"
					on_release:app.open()
					text_color:1,1,1,1
					font_size:"32sp"
				MDRoundFlatButton:
					text:"Select The File to be edit"
					pos_hint:{"center_x":0.5,"center_y":0.45}
					size_hint:0.25,0.08
					md_bg_color:0,153/255,1,1
					theme_text_color:"Custom"
					on_release:app.change_screen("edit_folder")
					text_color:1,1,1,1
					font_size:"32sp"
"""
default= "/storage/emulated/0"
my_path ="/storage/emulated/0"
class FileControlApp(MDApp):
    def build(self):
        return Builder.load_string(kv)

    def change_screen(self, screen_name):
        self.root.ids.screen.current = screen_name

    def accept_connection(self):
        try:
            self.client, addr = self.server.accept()
            self.joined = True
        except:
            print("Server crashed")

    def on_start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(("192.168.29.154", 12345))
            print("staretd")
            self.server.listen()
        except:
            pass

        self.joined = False
        accept_thread = th.Thread(target=self.accept_connection)
        accept_thread.start()

    def info(self, func, path=default):
        if self.joined:
            self.client.send(f"<_folder_>{path}".encode("utf-8"))
            while True:
                try:
                    data = self.client.recv(1024)
                    if data:
                        data = eval(data.decode("utf-8"))
                        print(data)
                        f = eval(func)
                        f(data, path)
                        break
                except:
                    pass

    def delete(self, names, path=default):
        try:
            self.root.ids.list.clear_widgets()
            for name, type in names.items():
                del_path = f"{path}/{name}"
                list_item = TwoLineAvatarListItem(
                    text=name,
                    secondary_text='Folder' if type == 'folder' else 'File')
                icon = IconLeftWidget(icon='folder' if type == 'folder' else 'file-outline')
                list_item.add_widget(icon)
                if type == "folder":
                    list_item.bind(on_release=lambda x, pa = del_path: self.send_del(pa))
                elif type == "file":
                    list_item.bind(on_release=lambda x,p = del_path: self.deleted(p))

                self.root.ids.del_list.add_widget(list_item)
        except:
            pass

    def add_edit(self, names, path=default):
        try:
            self.root.ids.list.clear_widgets()
            for name, type in names.items():
                edit_path = f"{path}/{name}"
                list_item = TwoLineAvatarListItem(
                    text=name,
                    secondary_text='Folder' if type == 'folder' else 'File')
                icon = IconLeftWidget(icon='folder' if type == 'folder' else 'file-outline')
                list_item.add_widget(icon)
                if type == "folder":
                    list_item.bind(on_release=lambda x, pat = edit_path , n = name:self.send_edit(pat,n))
                elif type == "file":
                    list_item.bind(on_release=lambda x , pat = edit_path: self.edited(pat))

                self.root.ids.edit_list.add_widget(list_item)
        except:
            pass

    def add(self, names, path=default):
        try:
            self.root.ids.list.clear_widgets()
            for name, type in names.items():
                item_path = f"{path}/{name}"
                print(item_path)
                list_item = TwoLineAvatarListItem(
                    text=name,
                    secondary_text='Folder' if type == 'folder' else 'File')
                icon = IconLeftWidget(icon='folder' if type == 'folder' else 'file-outline')
                list_item.add_widget(icon)
                mp = f"{my_path}/{name}"
                if type == "folder":
                    list_item.bind(on_release=lambda x, item_path1 = item_path: self.send(item_path1))
                elif type == "file":
                    list_item.bind(on_release=lambda x, filen = mp: self.down(item_path, filen))

                self.root.ids.list.add_widget(list_item)
        except:
            pass

    def send_edit(self, path,n):
        if self.joined:            
            msg = f"<folder>{path}"
            Clock.schedule_once(lambda dt: self.info("self.add_edit", path))
            self.client.send(msg.encode("utf-8"))  
    def send_del(self, path):
        msg = f"<folder>{path}"
        Clock.schedule_once(lambda dt: self.info(self.delete, path))
        self.client.send(msg.encode("utf-8"))

    def send(self, spath):
        msg = f"<folder>{spath}"
        Clock.schedule_once(lambda dt: self.info("self.add", spath))
        self.client.send(msg.encode("utf-8"))
        print("sended")
    def open_run(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_run,
            select_path=self.path_run,
        )
        self.file_manager.show('E:')

    def exit_run(self):
        self.file_manager.close()

    def path_run(self, path):
        self.pr = os.path.basename(path)
        print(self.pr)
        self.file_manager.close()
        label = MDLabel(text=f"file : {path}", pos_hint={"center_x": 0.9, "center_y": 0.45})
        self.root.ids.tem_run.add_widget(label)

    def open(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit,
            select_path=self.select_path,
        )
        self.file_manager.show("/storage/emulated/0/")

    def runn(self):
        if self.pr:
            self.client.send(f"<run>{self.pr}".encode("utf-8"))
            run_thread = th.Thread(target=self.send_file, args=(self.pr,))
            run_thread.start()

    def send_file(self, file_name):
        with open(file_name, "rb") as file:
            data = file.read()
            self.client.sendall(data)
            self.client.send(b"<END>")

    def exit(self):
        self.file_manager.close()

    def select_path(self, path):
        self.p = path
        print(self.p)
        self.file_manager.close()
        label = MDLabel(text=f"file : {path}", pos_hint={"center_x": 0.85, "center_y": 0.55})
        self.root.ids.tem.add_widget(label)

    def deleted(self, path):
        dialog = MDDialog(
            title="Delete",
            text="Do you want to delete this file",
            buttons=[
                MDRoundFlatButton(
                    text="Cancel", on_release=lambda x: dialog.dismiss()),
                MDRoundFlatButton(
                    text="Delete", on_release=lambda t: self.deleted1(path)),
            ],
        )
        dialog.open()

    def deleted1(self, path):
        self.client.send(f"<_delete_>{path}".encode("utf-8"))

    def edited(self, path):
        dialog = MDDialog(
            title="Edit",
            text="Do you want to Edit this file",
            buttons=[
                MDRoundFlatButton(
                    text="Cancel", on_release=lambda x: dialog.dismiss()),
                MDRoundFlatButton(
                    text="Edit", on_release=lambda t: self.edited1(path)),
            ],
        )
        dialog.open()

    def edited1(self, path):
        self.client.send(f"<_edit_>{path} ".encode("utf-8"))
        edit_thread = th.Thread(target=self.send_file, args=(self.p,))
        edit_thread.start()

    def down(self, path, name):
        dialog = MDDialog(
            title="Download",
            text="Do you want to download this file",
            buttons=[
                MDRoundFlatButton(
                    text="Cancel", on_release=lambda x: dialog.dismiss()),
                MDRoundFlatButton(
                    text="Download", on_release=lambda x: self.download(path, name)),
            ],
        )
        dialog.open()

    def download(self, path, name):
        self.client.send(f"<_download_>{path}".encode("utf-8"))
        download_thread = th.Thread(target=self.receive_file, args=(name,))
        download_thread.start()

    def receive_file(self, file_name):
        file_data =b""
        with open(file_name,"wb") as file:
        	while True:
        		data = self.client.recv(1024)
        		if data:
        			if data == "<END>":
        				break
        			else:
        				file_data += data
        	file.write(file_data)
        	file.close()

if __name__ == '__main__':
    FileControlApp().run()
