from tkinter import ttk, Button, filedialog
from .TopBar import TopBar
from .LabeledEntry import LabeledEntry
from .BaseWindow import BaseWindow

class StartWindow(BaseWindow):
	def __init__(self, controller, *args, **kwargs):
		BaseWindow.__init__(self, controller, *args, *kwargs)
		self.top_bar.set_title("New Project")
		self.top_bar.set_exit_function(self.close)

		self.width_entry = LabeledEntry("Width", 20, self)
		self.width_entry.pack(side = "top", fill = "x", padx = 3, pady = 3)

		self.height_entry = LabeledEntry("Height", 20, self)
		self.height_entry.pack(side = "top", fill = "x", padx = 3, pady = 3)

		# exit_button = Button(self, text = "Exit", command = self.close)
		# exit_button.pack(side = "bottom", fill = "x", padx = 3, pady = 3)	

		start_button = Button(self, text = "Spawn Canvas", command = self.spawn_canvas_window)
		start_button.pack(side = "bottom", fill = "x", padx = 3, pady = 3)

		load_button = Button(self, text = "Load Image", command = self.load_canvas_window)
		load_button.pack(side = "bottom", fill = "x", padx = 3, pady = 3)	

		load_gif = Button(self, text = "Load Gif", command = self.load_gif)
		load_gif.pack(side = "bottom", fill = "x", padx = 3, pady = 3)	

	def close(self, *args): self.destroy()

	def spawn_canvas_window(self):
		w = self.width_entry.get()
		h = self.height_entry.get()
		self.controller.spawn_canvas(w, h)
		self.close()

	def load_canvas_window(self):
		source = filedialog.askopenfilename(filetypes = [("All files", ".*"), ("PNG files", ".png"), ("JPEG files", ".jpg .jpeg"), ("BMP files", ".bmp")])
		if source:
			w = self.width_entry.get()
			h = self.height_entry.get()
			self.controller.load_canvas(source, w, h)
			self.close()

	def load_gif(self):
		source = filedialog.askopenfilename(filetypes = [("GIF files", ".gif"), ("All files", ".*")])
		if source:
			w = self.width_entry.get()
			h = self.height_entry.get()
			canvas = self.controller.spawn_canvas(w, h)
			canvas.load_gif_fresh(source)
			self.close()