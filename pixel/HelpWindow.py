from tkinter import Text, ttk
from .BaseWindow import BaseWindow

class HelpWindow(BaseWindow):
	def __init__(self, controller):
		BaseWindow.__init__(self, controller)
		self.resizable(True, True)
		self.set_title("Help")
		self.set_exit_function()
		with open("help.txt") as hlp:
			helptext = hlp.read()
		self.help_label = Text(self, wrap = "word")
		self.help_label.insert('end', helptext)
		self.help_label.configure(state = "disable")
		self.help_label.pack(fill = "both", expand = True, padx = 3, pady = 3)
		grip = ttk.Sizegrip(self)
		grip.place(relx=1.0, rely=1.0, anchor="se")