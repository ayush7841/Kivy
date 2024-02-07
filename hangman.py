import random
from time import sleep
from kivymd.app import MDApp
from kivy.graphics import Line, Color,Ellipse
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
import threading
from kivymd.uix.button import MDRoundFlatIconButton as button


words = ["apple", "soccer", "book", "lamp", "chocolate", "basketball", "keyboard", "chair", "football", "guitar", "pizza", "tennis", "table", "basket", "icecream", "swimming", "clock","volleyball", "couch", "drum", "burger", "baseball", "computer", "bed", "painting", "pasta", "cycling", "monitor", "desk", "camera",  "salad", "golf", "notebook", "mirror", "headphones", "sushi", "skiing", "mouse", "shelves", "television", "sandwich", "running", "printer", "wardrobe", "phone", "cake", "hiking", "mousepad", "stool", "microwave", "steak","boxing", "tablet", "ottoman", "globe", "smoothie", "skating", "speaker", "bench", "laptop","cookie", "climbing", "projector", "bookshelf", "calculator", "pancake", "badminton", "lampshade", "sofa", "keyboardstand", "donut", "surfing", "router", "ottoman", "easel","orange", "karate", "paperclip", "wardrobe", "printerstand", "grape", "hockey", "pencil", "mirrorstand", "gameconsole", "peanut", "archery", "journal", "beanbag", "gamingchair", "popcorn", "gymnastics", "tabletstand", "sidetable", "trampoline", "watermelon", "bowling", "pen", "coffeetable", "pingpong", "pineapple", "surfing", "marker", "cabinet", "dice"
]

hints = ["fruit often associated with teachers", "sport played with a round ball", "common item for reading", "provides illumination", "sweet treat made from cocoa", "sport involving a bouncing ball","input device for computers","furniture for sitting", "popular ball sport", "stringed musical instrument", "popular dish with various toppings","racket sport","common furniture piece", "used for carrying items", "frozen dessert combination", "water-based recreational activity", "device for timekeeping", "ball sport with a net", "comfortable seating furniture","percussion musical instrument", "popular dish often grilled","ball and bat sport", "electronic device", "sleeping furniture", "artistic creation on canvas","popular Italian dish", "activity on two wheels", "display device for computers", "workspace furniture","device for capturing images","dish with mixed ingredients", "outdoor sport with clubs", "stationery item", "reflective surface", "audio output device","Japanese dish with rice and fish", "winter sport on snow", "computer input device", "storage furniture","entertainment device", "layered dish with bread and fillings", "athletic activity", "output device for documents", "storage furniture for clothes", "communication device","celebratory dessert","outdoor activity","mouse accessory for precision", "seating without back support","quick cooking device","beef cut for grilling", "combat sport with gloves","portable computing device","low seat without back","earth model","blended fruit and liquid","activity on skates", "audio output device", "seating for multiple people", "portable computer", "sweet baked treat", "rock climbing activity", "presentation device", "shelving for books", "mathematical tool","round breakfast item","racquet sport","shade for a lamp","seating furniture","input device for computers","citrus fruit","martial art discipline","office supply item","storage furniture for clothes","printing device support","small fruit with a shell", "ice hockey sport","writing instrument", "stand for a mirror","video game system", "small legume", "precision sport with bows", "writing pad","soft seating", "special chair for gaming",  "popped corn snack", "athletic discipline", "support for a tablet",  "small table", "recreational device for bouncing", "large round fruit", "bowling sport",  "writing tool", "living room furniture","table tennis sport", "tropical fruit", "ocean activity with a board", "writing tool", "storage furniture", "random number generator"
]


kv ="""
Screen:
	MDRelativeLayout:
		id:scr
		MDLabel:
			text : "HangMan"
			halign:"center"
			theme_text_color:"Error"
			pos_hint:{"center_y":0.94}
			font_size:"40sp"
			underline:True
			bold:True
		MDLabel:
			pos_hint:{"center_y":0.8,"center_x":0.55}
			bold:True
			id:life
			text:"Life left : 7"
			font_size:"25sp"
			  
		Widget:
			canvas.before:
				Color:
					rgba:0,0,0,1
				Line:
					points:0,700,2000,700
					width:3
				Line:
					points:1460,970,1400,930
					width:3
				Line:
					points:1400,700,1400,1000
					width:3
				Line:
					points:1600,970,1370,970 
					width:3
				
		
		MDLabel:
			id:hint
			pos_hint:{"center_y":0.8}
			halign:"center"
			font_size:"30sp"
			bold:True		
			text:""
		MDLabel:
			id:under
			pos_hint:{"center_y":0.7}
			halign:"center"
			font_size:"50sp"
			text:""
		MDLabel:
			id:word
			pos_hint:{"center_y":0.76}
			halign:"center"
			font_size:"30sp"
			text:""
		MDLabel:
			id:result
			pos_hint:{"center_y":0.68}
			halign:"center"
			font_size:"50sp"
			text:""
		MDLabel:
			id:check
			text:""
			pos_hint:{"center_y":0.6}
			halign:"center"
			font_size:"30sp"
		MDGridLayout:
			rows :3
			size_hint:0.9,0.5
			pos_hint:{"center_x":0.5}
			spacing:"15sp"
			id:key
"""
class hangman(MDApp):
	def build(self):
		return Builder.load_string(kv)
	def create(self):
		self.root.ids["result"].text = ""
		try:
			self.root.ids.scr.remove_widget(self.btn)
		except:
			pass
		self.life = 7
		self.root.ids["life"].text = "Life left : 7"
		index = random.randint(0,len(words)-1)
		self.word = words[index]
		self.hin = hints[index]
		self.un = "_ "*len(self.word)
		self.root.ids["hint"].text = self.hin
		self.root.ids["under"].text = self.un
		
	def corr(self):
		self.root.ids["check"].text = "Correct !!"
		self.root.ids["check"].theme_text_color = "Custom"
		self.root.ids["check"].text_color = (20/255,170/255,105/255)
		sleep(1.5)
		self.root.ids["check"].text = ""
	def wrong(self):
		self.root.ids["check"].text = "Wrong !!"
		self.root.ids["check"].theme_text_color = "Custom"
		self.root.ids["check"].text_color = (200/255,40/255,90/255)
		sleep(1.5)
		self.root.ids["check"].text = ""
	def start(self):
		for i in range(1,7):
			line = f"self.line{i}"
			(eval(line)).points = [0,0,0,0]
		self.root.ids.scr.canvas.before.remove(self.circle)
		self.clear()
		self.create()
	def clear(self):		
		self.root.ids["word"].text = ""
	def won(self):
		for i in range(1,7):
			try:
				line = f"self.line{i}"
				(eval(line)).points = [0,0,0,0]
			except:pass
		try:
			self.root.ids.scr.canvas.before.remove(self.circle)
		except:pass
		self.root.ids["hint"].text =""
		self.root.ids["under"].text=""
		self.root.ids["result"].text="You Won !!"
		self.root.ids["result"].theme_text_color = "Custom"
		self.root.ids["result"].text_color = (20/255,170/255,105/255)
		btn = button(text="Play again",icon="reload",on_release=lambda x:self.create(),pos_hint={"center_y":0.55,"center_x":0.5},id="btn",md_bg_color=(90/255, 202/255,130/255),theme_text_color="Custom",text_color=(1,1,1,1),icon_color=(1,1,1,1))
		self.btn = btn
		self.root.ids.scr.add_widget(btn)
	def lose(self):
		self.root.ids["hint"].text =""
		self.root.ids["under"].text=""
		self.root.ids["result"].text="You Loss"
		self.root.ids["word"].text = f"The Word Was :- {self.word}"
		self.root.ids["result"].theme_text_color = "Error"
		btn = button(text="Play again",icon="reload",on_release=lambda x:self.start(),pos_hint={"center_y":0.55,"center_x":0.5},id="btn",md_bg_color=(90/255, 202/255,130/255),theme_text_color="Custom",text_color=(1,1,1,1),icon_color=(1,1,1,1))
		self.btn = btn
		self.root.ids.scr.add_widget(btn)
	def on_start(self):
		letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
		for letter in letters:
			btn = MDCard(id=letter,size_hint=(0.01,0.01),elevation=3.5,radius=[20],md_bg_color=(95/255, 190/255, 220/255, 1),on_release=lambda x ,l = letter.lower() :self.check(l))
			self.btn = btn
			text = MDLabel(text=letter,halign="center",bold=True)
			btn.add_widget(text)
			self.root.ids.key.add_widget(btn)				
		self.create()
	def check(self,lett):
		un = self.un.split()		
		if lett in self.word.lower():
			i = []
			for ind, a in enumerate(self.word.lower()):
			    if a == lett:
			        un[ind] = lett
			self.un = " ".join(un)
			self.root.ids["under"].text = self.un
			threading.Thread(target=self.corr).start()
			if "_" not in un:
				self.won()
		else:
			if self.life == 1:
				with self.root.ids.scr.canvas.before:
					    Color(0, 0, 0, 1)
					    self.line6 = Line(points=[1550,800,1600,760], width=3)	
				self.root.ids["life"].text = "Life left : 0"
				self.lose()
			else:
				self.life -=1
				self.root.ids["life"].text = f"Life left : {self.life}"
				threading.Thread(target=self.wrong).start()
				if self.life == 6:
					with self.root.ids.scr.canvas.before:
					    Color(0, 0, 0, 1)
					    self.line1 = Line(points=[1550,900,1550,970], width=3)
				elif self.life ==5:
					    with self.root.ids.scr.canvas.before:
					    	Color(0, 0, 0, 1)
					    	self.circle = Ellipse(pos=(1525, 870), size=(50, 50))
				elif self.life == 4:
					with self.root.ids.scr.canvas.before:
					    Color(0, 0, 0, 1)
					    self.line2 = Line(points=[1550,800,1550,870], width=3)
				elif self.life == 3:
					with self.root.ids.scr.canvas.before:
					    Color(0, 0, 0, 1)
					    self.line3 = Line(points=[1550,860,1500,830], width=3)
				elif self.life == 2:
					with self.root.ids.scr.canvas.before:
					    Color(0, 0, 0, 1)
					    self.line4 = Line(points=[1600,830,1550,860], width=3)
				elif self.life == 1:
					with self.root.ids.scr.canvas.before:
					    Color(0, 0, 0, 1)
					    self.line5 = Line(points=[1550,800,1500,760], width=3)
													   								   						   					   
hangman().run()
