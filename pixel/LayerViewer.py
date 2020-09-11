from tkinter import Frame, Label, Canvas, Scale, ttk
from PIL import Image, ImageTk

PAUSED = False
RUNNING = True

def force_aspect(inner_frame, outer_frame, ratio):
	def force_ratio(event):
		w = event.width
		h = int(event.width / ratio)
		if h > event.height:
			h = event.height
			w = int(event.height * ratio)
		inner_frame.place(
			in_=outer_frame, 
			relx = 0.5,
			rely = 0.5,
			x = - 0.5 * float(w),
			y = - 0.5 * float(h),
			width=w,
			height=h
		)
	outer_frame.bind("<Configure>", force_ratio)

class LayerViewer(ttk.LabelFrame):
	def __init__(self, project, width, height, *args, **kwargs):
		ttk.LabelFrame.__init__(self, *args, **kwargs)
		self.configure(text = "LayerViewer")
		self.project = project
		self.width = width
		self.height = height
		self.delay = 1000
		self.index = 0
		self.state = PAUSED

		self.outer_frame = Frame(self)
		self.outer_frame.pack(side = "top", fill = "both", expand = True, padx = 4, pady = 4)
		self.outer_frame.config(width = 250, height = 200)
		self.inner_frame = Frame(self)
		force_aspect(self.inner_frame, self.outer_frame, float(width)/float(height))

		self.canvas = Canvas(self.inner_frame, relief="sunken")
		self.canvas.config(
			width=50, #Parent frame width
			height = 50,
			highlightthickness=0)        
		self.canvas.config() 
		self.canvas_frame = Frame(self.canvas, border = 0, highlightthickness = 0)
		self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')
		self.canvas_frame.config(width= 50, height = 50)
		self.canvas.pack(fill = "both", expand = True)

		self.playback_scale = Scale(self, orient = "horizontal", from_ = 0, to = 30, command = self.set_delay)
		self.playback_scale.set(int(self.delay/1000))
		self.playback_scale.pack(fill = "both", expand = False, padx = 4, pady = 4)

		self.display_loop()

	# def pause(self, event = None):
	# 	self.state = PAUSED

	# def play(self, event = None):
	# 	self.state = RUNNING

	def set_delay(self, fps):
		if float(fps) < float(1.0):
			self.delay = None
			return
		self.delay = int(1000.0 / float(fps))



	"""
	Approximates an fps, milage will vary, it would be 
	better for me to run this as a thread spawned by a
	timer thread  that acts as the loop, so the fps 
	would more closely match the one selected with the menu bar
	"""
	def display_loop(self):
		if not self.project.frames or not self.delay: self.after(100, self.display_loop); return
		if self.index > len(self.project.frames) - 1:
			self.index = 0
		layer = self.project.frames[self.index]
		self.image = layer.export_composite_image().resize((self.inner_frame.winfo_width(), self.inner_frame.winfo_height()), Image.BOX)
		self.displayed = ImageTk.PhotoImage(self.image)
		self.canvas.delete("all")
		self.canvas.create_image(0, 0, image = self.displayed, anchor = "nw")
		self.configure(text = f"Preview: {layer.id}")
		self.index += 1
		if self.delay < 10:
			delay = 10
		delay = self.delay or 1000
		self.after(delay, self.display_loop)