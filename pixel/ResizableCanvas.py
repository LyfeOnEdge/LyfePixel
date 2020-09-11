from tkinter import Canvas

class ResizableCanvas(Canvas):
	def __init__(self, parent, **kwargs):
		Canvas.__init__(self, parent, **kwargs)
		self.configure(borderwidth = 0, highlightthickness = 0)
		self.bind("<Configure>", self.on_configure)
		self.height = self.winfo_reqheight()
		self.width = self.winfo_reqwidth()
	def on_configure(self, event):
		wscale = float(event.width)/self.width
		hscale = float(event.height)/self.height
		self.width = event.width
		self.height = event.height
		self.config(width=self.width, height=self.height)
		self.scale("all",0,0,wscale,hscale)