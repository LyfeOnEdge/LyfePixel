from tkinter import Toplevel, Label, Scale, PhotoImage, Frame, ttk
from .BaseWindow import BaseWindow
from .TopBar import TopBar
from .file_management import load_tk_image_from_bytes_array
from PIL import Image, ImageTk

SIZE = 300

class ImageViewer(BaseWindow):
	def __init__(self, controller, image_data):
		BaseWindow.__init__(self, controller)
		self.set_title("Preview")
		self.set_exit_function()
		controller = controller
		self.attributes('-toolwindow')
		self.geometry(f"{300}x{300}")
		self.minsize(200, 200)
		self.resizable(True, True)
		self.image_frame = Frame(self)
		self.image_view = Label(self.image_frame)
		self.image_view.place(relwidth = 1, relheight = 1)
		self.image_data = image_data
		self.image = None
		self.image_frame.pack(fill = "both", expand = True)
		self.set_image(self.image_data)
		image_scale = Scale(self, from_=1, to=64, orient="horizontal", command = self.resize_image)
		image_scale.pack(fill = "x", expand = True, side = "left")
		self.grip = ttk.Sizegrip(self)
		self.grip.place(relx=1.0, rely=1.0, anchor="se")
		self.grip.bind("<ButtonPress-1>", self.on_press)
		self.grip.bind("<B1-Motion>", self.on_resize)
		self.grip.bind("<ButtonRelease-1>", self.on_release)
				
	def resize_image(self, scale):
		scale = int(scale)
		#open image as a photoimage to get size
		img = ImageTk.PhotoImage(self.image_data)
		h = int(img.height())
		w = int(img.width())
		self.set_image(self.image_data.resize((h * scale, w * scale), Image.BOX))

	def set_image(self, data):
		self.image = ImageTk.PhotoImage(data)
		self.image_view.configure(image = self.image) 

	def on_press(self, event):
		self.grip["cursor"] = "bottom_right_corner"

	def on_resize(self, event):
		x_change = event.x_root - self.winfo_rootx()
		x_change = 1 if x_change < 1 else x_change
		y_change = event.y_root - self.winfo_rooty()
		y_change = 1 if y_change < 1 else y_change
		self.geometry("%sx%s" % (x_change, y_change))

	def on_release(self, event):
		sizegrip["cursor"] = "arrow"
		
		



