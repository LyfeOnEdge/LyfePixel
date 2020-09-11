from tkinter import Frame, ttk, Label
from .file_management import load_tk_image_from_bytes_array

class ToolBar(Frame):
	def __init__(self, button_list, *args, **kwargs):
		Frame.__init__(self, *args, *kwargs)
		self.bar = Label(self, font = "Bold")
		self.bar.configure(anchor = "center")
		self.pack(side = "top", fill = "x", padx = 2, pady = 2)
		self.button_list = button_list
		self.buttons = []
		self.build()

	def build(self):
		for image, command in self.button_list:
			button = BarButton(self, image = image, command = command)
			button.pack(side = "left")
			self.buttons.append(button)
		self.bar.pack(side = "right", fill="both", expand = True)		

	def set_title(self, title):
		self.bar.configure(text = title)

	def exit(self):
		if self.exit_function:
			self.exit_function()


class BarButton(Label):
	def __init__(self, *args, **kwargs):
		self.command = kwargs.pop("command") if kwargs.get("command") else None        	
		self.image = kwargs.pop("image") if kwargs.get("image") else None

		Label.__init__(self, *args, **kwargs)
		# self.configure(background = "#888888")
		self.bind('<Button-1>', self.on_click)
		self.set_image(self.image)

	#Use callback when our makeshift "button" clicked
	def on_click(self, event=None):
		if self.command:
			self.command()

	#Function to update the button's set command
	def set_command(self,command):
		self.command = command

	#Function to set the button's image
	def set_image(self,image):
		self.configure(image=image)
		self.image = image

	#Function to set the button's text
	def set_text(self,text):
		self.configure(text=text)
