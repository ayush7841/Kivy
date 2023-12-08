from kivymd.app import MDApp
from kivy.lang import Builder
import sqlite3
from kivymd.uix.label import MDLabel
from time import sleep

style = """
ScreenManager:
    id: screen

    Screen:
        name: "log"
        MDRelativeLayout:
            md_bg_color: 106/255, 196/255, 204/255
            AsyncImage:
                allow_stretch: True
                keep_ratio: False
                source: "/storage/emulated/0/Log.jpg"

            MDLabel:
                text: "LOG IN"
                pos_hint: {"center_x": 0.7, "center_y": 0.8}
                font_size: "40sp"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

            MDTextField:
                hint_text: "Name"
                line_color_focus: 1, 1, 1, 1
                mode: "fill"
                icon_left: "account"
                id: name
                size_hint: (None, None)
                size: (750, 60)
                pos_hint: {"center_x": 0.3, "center_y": 0.65}

            MDTextField:
                hint_text: "Phone no."
                id: phone
                input_filter: "int"
                icon_left: "phone"
                mode: "fill"
                line_color_focus: 1, 1, 1, 1
                size_hint: (None, None)
                size: (750, 60)
                pos_hint: {"center_x": 0.3, "center_y": 0.55}

            MDTextField:
                hint_text: "Email id"
                id: email
                icon_left: "email"
                mode: "fill"
                size_hint: (None, None)
                size: (750, 60)
                pos_hint: {"center_x": 0.3, "center_y": 0.45}

            MDTextField:
                hint_text: "Password"
                id: password
                mode: "fill"
                icon_left: "lock"
                size_hint: (None, None)
                size: (750, 60)
                password: True
                pos_hint: {"center_x": 0.3, "center_y": 0.35}

            MDRoundFlatButton:
                text: "Log In"
                theme_text_color: "Custom"
                text_color: 240/255, 240/255, 240/255, 1
                md_bg_color: 19/255, 214/255, 149/255
                pos_hint: {"center_x": 0.3, "center_y": 0.2}
                size_hint: (0.2, 0.08)
                on_release: app.log()
"""

class login(MDApp):
    def build(self):
        return Builder.load_string(style)

    def change_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name

    def log(self):
        n = self.root.ids["name"].text
        p = self.root.ids["phone"].text
        e = self.root.ids["email"].text
        pa = self.root.ids["password"].text
        if n and p and e and pa:
            data = sqlite3.connect("login.db")
            cursor = data.cursor()
            create = """
            CREATE TABLE IF NOT EXISTS log(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone  INTEGER,
            email TEXT NOT NULL,
            password TEXT NOT NULL
            );
            """
            cursor.execute(create)
            insart = """
            INSERT INTO log(name,phone,email,password) VALUES (?,?,?,?)
            """
            cursor.execute(insart, (n, p, e, pa))
            data.commit()
            data.close()



login().run()
