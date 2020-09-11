from tkinter import Toplevel
from .TopBar import TopBar

class BaseWindow(Toplevel):
	def __init__(self, controller):
		Toplevel.__init__(self)
		self.controller = controller
		self.controller.configure_toplevel(self)
		self.top_bar = TopBar(self)
		self.top_bar.set_title("BaseWindow")

	def set_title(self, title):	self.top_bar.set_title(title)
	
	def set_exit_function(self, exit_function = None):
		exit_function = exit_function or self.exit
		self.top_bar.set_exit_function(exit_function)

	def exit(self):	self.destroy()