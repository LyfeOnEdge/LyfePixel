from tkinter import StringVar, Frame, Toplevel, Label, Button, PanedWindow, colorchooser, Scale, Menu, ttk
from .BaseWindow import BaseWindow
from .TopBar import TopBar
from .canvas import PixelCanvas
from .colormath import get_gradient, get_rainbow, hex_to_rgba, hex_to_rgb
from .ImageViewer import ImageViewer
from .file_management import load_tk_image_from_bytes_array
from .ToolController import ToolController, TOOLCONST
from .ToolBox import ToolBox
from .pixel import PixelProject
from .LyfeCanvas import LyfeCanvas
from .HelpWindow import HelpWindow
from .StartWindow import StartWindow

DRAW = "draw"
EYEDROPPER = "eyedropper"

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



class PalletWindow(ttk.Frame):
	def __init__(self, controller):
		ttk.Frame.__init__(self)
		self.controller = controller
		self.window = self._nametowidget(self.winfo_parent())
		self.window.bind("<Escape>", self.exit)
		self.window.title("LyfePixel")
		self.controller.configure_toplevel(self.window)
		self.window.overrideredirect(0)
		self.place(relwidth = 1, relheight = 1)
		self.state = TOOLCONST.DRAW
		self.window.resizable(True, True)
		self.project = PixelProject(8, 8)
		self.pallet = self.project.selected_frame.selected_layer
		self.pallet.selection = [f"{self.pallet.width - 1}x{self.pallet.height - 1}"]
		self.alpha = 255

		menubar = Menu(self.window)
		menubar.add_command(label="New", command=self.open_start_window)
		menubar.add_separator()
		menubar.add_command(label="Help", command=lambda: HelpWindow(self.controller))
		menubar.add_separator()
		menubar.add_command(label="Exit", command= self.exit)
		# display the menu
		self.window.config(menu=menubar)
		
		panes = PanedWindow(self, orient = "vertical", sashpad=3, sashrelief ="sunken")
		panes.pack(fill = "both", expand = True)
		panes.config(borderwidth = 0)
		
		canvas_frame = Frame(panes)
		canvas_frame.pack(fill = "both", expand = True, side = "top", anchor = "n")
		canvas_frame.configure(height = 150, width = 150)
		panes.add(canvas_frame)
		self.canvas = LyfeCanvas(self.project, canvas_frame)
		force_aspect(self.canvas, canvas_frame, 1.0)
		colors = get_gradient(8)
		colors.extend(get_rainbow(56))
		for id in self.canvas.itterate_canvas(): self.pallet.set_pixel_color(id, hex_to_rgba(colors.pop()))
		self.canvas.bind_left(self.select_color)
		self.canvas.bind_double_left(self.change_color)
		self.canvas.bind("<Configure>", self.on_configure)
		self.canvas.configure()
	
		outer_frame = Frame(panes)
		outer_frame.pack(fill = "x", expand = True, padx = 4)
		panes.add(outer_frame)
		
		color_label_frame = Frame(outer_frame)
		self.color_label_text_var = StringVar()
		self.color_label_text_var.set(ToolController.get_color())
		color_label = Label(color_label_frame, textvariable = self.color_label_text_var)
		color_label.pack(side = "bottom", fill = "x", expand = True)
		color_label_frame.pack(fill = "x", expand = False)

		self.alpha_scale = Scale(outer_frame, orient = "horizontal", from_ = 0, to = 255, command = self.set_alpha)
		self.alpha_scale.set(self.alpha)
		self.alpha_scale.pack(fill = "both", expand = False, pady = 2)
		
		div_1 = ttk.Separator(outer_frame)
		div_1.pack(fill = "x", expand = False, pady = 2)

		self.toolbox = ToolBox(outer_frame)
		self.toolbox.pack(fill = "both", expand = True, pady = 2)

		self.grip = ttk.Sizegrip(self)
		self.grip.place(relx=1.0, rely=1.0, anchor="se")
		self.grip.bind("<ButtonPress-1>", self.on_press)
		self.grip.bind("<B1-Motion>", self.on_resize)
		self.grip.bind("<ButtonRelease-1>", self.on_release)

		self.window.minsize(250, 400)

	def on_configure(self, event): self.canvas.redraw()
	def on_press(self, event): self.grip["cursor"] = "bottom_right_corner"

	def on_resize(self, event):
		x_change = event.x_root - self.window.winfo_rootx()
		x_change = 1 if x_change < 1 else x_change
		y_change = event.y_root - self.window.winfo_rooty()
		y_change = 1 if y_change < 1 else y_change
		# self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
		self.window.geometry("%sx%s" % (x_change, y_change))

	def on_release(self, event):
		self.grip["cursor"] = "arrow"
		self.canvas.redraw()

	def update(self):
		self.color_label_text_var.set(ToolController.get_color())
		self.canvas.redraw()

	def set_color(self, color):
		self.color = color
		self.color_label_text_var.set(color)

	def select_color(self, event):
		id = self.canvas.get_cell_id(event.x, event.y)
		if id:
			x, y  = (int(v) for v in id.split("x"))
			ToolController.set_color(self.pallet.array[y][x])
			self.alpha = self.pallet.array[y][x][3]
			self.alpha_scale.set(self.alpha)
			self.pallet.selection = [id]
			self.update()

	def change_color(self, event):
		id = self.canvas.get_cell_id(event.x, event.y)
		if not id: return
		color = colorchooser.askcolor()[0]
		if not color: return #If no color was selected
		r,g,b = color
		color = (r,g,b, 255)
		ToolController.set_color(color)
		self.alpha = color[3]
		self.alpha_scale.set(self.alpha)
		self.pallet.load_image(ToolController.draw(self.pallet, id))
		self.pallet.selection = [id]
		self.update()

	def set_color(self, color):
		id = self.pallet.selection[0]
		ToolController.set_color(color)
		self.alpha_scale.set(color[3])
		self.pallet.load_image(ToolController.draw(self.pallet, id))
		self.update()

	def set_alpha(self, alpha):
		self.alpha = alpha
		r,g,b,a = ToolController.get_color()
		ToolController.set_color([r,g,b,self.alpha])
		self.pallet.load_image(ToolController.draw(self.pallet, self.pallet.selection[0]))
		self.update()

	def open_start_window(self): StartWindow(self.controller)
	def exit(self): self.window.destroy()
