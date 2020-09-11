import os, threading
from tkinter import ttk, Tk, Toplevel, Listbox, Button, StringVar, Frame
from PIL import Image, ImageTk
from pixel.PalletWindow import PalletWindow
from pixel.ProjectWindow import ProjectWindow
from pixel.StartWindow import StartWindow
from pixel.file_management import load_tk_image_from_bytes_array, load_tk_image_object_from_bytes_array
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 150
HEIGHT = 250
OFFSET = 5

style = ttk.Style()
style.configure("TLabel", foreground="white", background="#888888")
style.configure("Entry.TLabel", background="white", foreground="black")
style.configure("TEntry", foreground="black", background="white", highlightthickness=2, highlightbackground = "#aaaaaa", borderwidth=0)

class threader: #An object declared outside of tkinter mainloop territory for calling threads
	def __init__(self):
		pass
	def do_loop(self, func, arglist = [], delay = 1):
		func(arglist) if arglist else func()
		threading.Timer(delay, self.do_loop, (func, arglist)).start()
Threader = threader()

class CanvasController:
	def __init__(self, devmode = False):
		self.devmode = devmode
		self.canvases = []

	def start_mainloop(self):
		self.root = self.PalletWindow = PalletWindow(self)
		# self.StartWindow = StartWindow(self)
		self.PalletWindow.mainloop()

		

	def spawn_canvas(self, width, height, *args, **kwargs):
		print(f"Spawning canvas - {width} x {height}")
		c = ProjectWindow(self, width, height, *args, **kwargs)
		c.load_blank()
		self.canvases.append(c)
		return c

	def load_canvas(self, source, width, height, *args, **kwargs):
		print(f"Loading canvas - {width} x {height} from {source}")
		c = ProjectWindow(self, width, height, *args, **kwargs)
		image = Image.open(source).convert("RGBA")
		f = c.project.selected_frame
		f.del_layer(f.selected_layer)
		c.load_image(image)
		self.canvases.append(c)
		return c

	# def test_load_image(self):
	# 	rotate_right_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00fIDATx\x9c\xad\x93Q\x0e\xc0 \x08C[\xb2\xfb_\x99\xfdl\xc9\x82E\xa6\xd8\xc4\x1fy\x14A\x05\x9a\xe2$\xe6\x05\xeb\x00\xa8\x0cb\xa2*\xfa2\x83\x81\x07\xb02\xa6\t\x80"Y\x19\x02\x00Lm&\x92\xadY\x08fCM\xe7r\xfd\xac\x9e\xde\xd6J\x0b_\xf9\xb3\xb6\r\xe6\xae+\\\xfb\x04\xbb\x0f\x89\x19\x14\xc1\xb2h\xe73\x9d\xd1\r4\xaa\x14\x12L4\x91\xa7\x00\x00\x00\x00IEND\xaeB`\x82'
	# 	c = ProjectWindow(self, 16, 16)
	# 	image = load_tk_image_object_from_bytes_array(rotate_right_bytes)
	# 	c.load_image(image)
	# 	self.canvases.append(c)

	def configure_toplevel(self, tl):
		tl.wait_visibility(tl)
		tl.attributes('-topmost', True)
		tl.geometry(f"{WIDTH}x{HEIGHT}")
		tl.resizable(False, False)
		tl.overrideredirect(1)

if __name__ == "__main__":
	app = CanvasController(devmode = True)
	app.start_mainloop() #Call tk mainloop

	# self.starter_window = StartWindow(controller) #Create StarterWindow, inits in its own toplevel
	# self.starter_window.mainloop()