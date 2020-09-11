from tkinter import ttk, Label, StringVar

class LabeledEntry(ttk.Frame):
	def __init__(self, text = None, default = "", *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		label = Label(self, text = text)
		label.pack(side = "left", fill = None, padx = 2)
		self.var = StringVar()
		self.var.set(default)
		entry = ttk.Entry(self, textvariable = self.var)
		entry.pack(side = "right", fill = "x", expand = True, padx = 2)

	def get(self):
		return self.var.get()

	def set(self, val):
		self.var.set(val)