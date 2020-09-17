from tkinter import Toplevel, Frame, Canvas, Scrollbar, Label, simpledialog, messagebox, filedialog, ttk
from .file_management import load_tk_image_from_bytes_array
from .BaseTile import BaseTile
from .BaseWindow import BaseWindow
from PIL import Image, ImageTk
import platform

trash_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00-IDATx\x9ccd\xc0\x0e\xfe\xe3\x10g\xc4%\x80K\x03!\xc0\xc8D\xa6F\xea\x01t?\x11\xeb\x15\xb8>\x8a\xbd0j\xc0\xa8\x01\x83\xc3\x00\x00\xf2\xb9\x03\x1c\xd6\xd7\xf8 \x00\x00\x00\x00IEND\xaeB`\x82'
class ClipBoardClass:
	def __init__(self):
		self.layers = []
		self.selection = []
		self.selected_layer = None
	
	def set_id(self, id): self.id = id
	def activate(self): self.active = True
	def deactivate(self): self.active = False
	def collapse(self): self.collapsed = True
	def uncollapse(self): self.collapsed = False
	def activate_layer(self, layer):
		for l in self.layers:
			if l is layer:
				l.activate()
				return
		raise FrameNotFound

	def copy_item(self, tkimage, name = "Clip"):
		l = ClipboardLayer(name, tkimage)
		self.layers.append(l)
		self.selected_layer = l
		
	def del_layer(self, layer):
		self.layers.remove(layer)

	def select_layer(self, selection):
		self.selected_layer = self.layers[selection]

	def copy_layer(self, layer):
		id = layer.id
		l = self.new_layer()
		l.load_image(layer.export_image())
		l.set_id(f"Copy of {id}")

	def get_layers(self):
		for layer in self.layers:
			yield layer

	def promote_layer(self, layer):
		index = self.layers.index(layer)
		if not index: return
		layer = self.layers.pop(index)
		self.layers.insert(index - 1, layer)

	def demote_layer(self, layer):
		index = self.layers.index(layer)
		if index == len(self.layers) - 1: return
		layer = self.layers.pop(index)
		self.layers.insert(index + 1, layer)
ClipBoard = ClipBoardClass()

class ClipboardLayer:
	def __init__(self, id, image):
		self.id = id
		self.image = image
		self.width, self.height = self.image.size
		self.active = False

	def set_id(self, id): self.id = id
	def activate(self): self.active = True
	def deactivate(self): self.active = False
	def export_image(self):
		return self.image

# class ClipboardWindow(BaseWindow):
# 	def __init__(self, controller):
# 		BaseWindow.__init__(self, controller)
# 		self.clipboard = controller.clipboard
# 		self.resizable(True, True)
# 		self.set_title("Clipboard")
# 		self.geometry(f"{250}x{400}")
# 		self.minsize(100, 200)


class ClipBoardBox(ttk.Labelframe):
	def __init__(self, controller, *args,):
		ttk.Labelframe.__init__(self, *args, text = "Clipboard")
		self.clipboard = controller.clipboard
		
		self.thumbnails = []
		self.tiles = []
		self.canvas_height = 300
		self.trash_image = load_tk_image_from_bytes_array(trash_bytes)
	
		self.nextid = 0

		self.canvas = Canvas(self, relief="sunken")
		self.canvas.config(width=200, height = self.canvas_height,	highlightthickness=0)
		self.scrollbar = Scrollbar(self)
		self.scrollbar.config(command=self.on_scroll_bar)           
		self.canvas.config(yscrollcommand=self.scrollbar.set) 
		self.scrollbar.pack(side="right", fill="y")                     
		self.canvas.pack(side = "right", expand=True, fill="both")
		self.canvas_frame = Frame(self.canvas, border = 0, highlightthickness = 0)
		self.canvas_frame.bind("<MouseWheel>", self._on_mouse_wheel)
		self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')
		self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
		self.canvas_frame.config(width= 200, height = self.winfo_height())
		self.canvas.config(scrollregion=(0,0, 200, self.canvas_height))
		self.canvas.bind("<Enter>", self.mouse_enter)
		self.canvas.bind("<Leave>", self.mouse_leave)
		self.canvas.bind("<Motion>", self.on_mouse_move)
		self.canvas.bind("<Button-1>", self.on_click)
		self.canvas.after_idle(self.refresh)
		self.bind("<MouseWheel>", self._on_mouse_wheel)

		self.grip = ttk.Sizegrip(self)
		self.grip.place(relx=1.0, rely=1.0, anchor="se")
		self.grip.bind("<ButtonPress-1>", self.on_press)
		self.grip.bind("<B1-Motion>", self.on_resize)
		self.grip.bind("<ButtonRelease-1>", self.on_release)

	# def on_resize(self, event):
	# 	x_change = event.x_root - self.winfo_rootx()
	# 	x_change = 1 if x_change < 1 else x_change
	# 	y_change = event.y_root - self.winfo_rooty()
	# 	y_change = 1 if y_change < 1 else y_change
	# 	# self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
	# 	self.geometry("%sx%s" % (x_change, y_change))
	
	def on_press(self, event): self.grip["cursor"] = "bottom_right_corner"

	def on_resize(self, event):
		x_change = event.x_root - self.winfo_rootx()
		x_change = 1 if x_change < 1 else x_change
		y_change = event.y_root - self.winfo_rooty()
		y_change = 1 if y_change < 1 else y_change
		# self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
		self.geometry("%sx%s" % (x_change, y_change))

	def on_release(self, event):
		self.grip["cursor"] = "arrow"
		self.refresh()

	def mouse_enter(self, event): pass
	def mouse_leave(self, event): pass
	def on_click(self, event):
		y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
		x = event.x
		for t in self.tiles:
			if t.is_in_row(y):
				mode = t.on_click(x, y)
				if not mode:
					self.clipboard.selected_layer = t.layer
					t.layer.activate()
					self.refresh()
			else: t.deactivate()

	def on_mouse_move(self, event):
		y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
		x = event.x
		for t in self.tiles:
			if t.active:
				if t.is_in_row(y): continue
				else: t.deactivate()
			elif t.is_in_row(y): t.activate()


	def refresh(self, event = None):
		self.winfo_toplevel().update_idletasks()
		self.canvas.delete("all")
		self.thumbnails = []
		self.tiles = []
		if self.clipboard.layers:
			i = 0
			y_offset = 10
			y_padding = 10
			tile_height = 80
			x = 10
			width = 80
			height = tile_height
			child_offset = 0.5 * tile_height
			for c in self.clipboard.layers:
				y = i * tile_height + y_offset + i * y_padding
				t = ClipTile(self, c)
				self.tiles.append(t)
				t.set_dimensions(x,  y, width, height)
				self.place_tile(t)
				if c is self.clipboard.selected_layer: self.select_tile(t)

				i+= 1
				
			height = i * tile_height + y_offset + i * y_padding
			frameheight = self.canvas_frame.winfo_height()
			height = height if height > frameheight else frameheight
			self.canvas_height = height
			self.canvas_frame.config(width= 200, height = self.canvas_height)
			self.canvas.config(scrollregion=(0,0, 200, self.canvas_height))

		else:
			pass

	def place_tile(self, tile):
		tn = ImageTk.PhotoImage(tile.get_thumbnail(tile.height))
		self.thumbnails.append(tn)
		tile.references.append(self.canvas.create_image(tile.x + 0.5 * tile.width, tile.y +  0.5 * tile.height, image = tn))
		tile.references.append(self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 1))
		tile.references.append(self.canvas.create_text(tile.x + tile.width + 10, tile.y, font="CourierNew 8", text=tile.id, anchor = "nw"))
		tile.references.append(self.canvas.create_text(tile.x + tile.width + 10, tile.y + 10, font="CourierNew 8", text=f"Size: {tile.layer.width}px x {tile.layer.height}px", anchor = "nw"))

	def activate_tile(self, tile):
		tile.active_references.extend([
			self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 2),
			self.canvas.create_image(tile.trash_x, tile.trash_y, anchor = "nw", image = self.trash_image),
		])

	def deactivate_tile(self, tile):
		self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 1)
		for r in tile.active_references:
			self.canvas.delete(r)

	def select_tile(self, tile):
		tile.references.append(self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 3))

	def _on_mouse_wheel(self, event):
		if platform.system() == 'Windows':
			self.canvas.yview_scroll(-1 * int(event.delta / 120), 'units')
		elif platform.system() == 'Darwin':
			self.canvas.yview_scroll(-1 * int(event.delta), 'units')
		else:
			if event.num == 4:
				self.canvas.yview_scroll(-1, 'units')
			elif event.num == 5:
				self.canvas.yview_scroll(1, 'units')

	def on_scroll_bar(self, move_type, move_units, __ = None):
		if move_type == "moveto":
			self.canvas.yview("moveto", move_units)

	def delete_layer(self, layer):
		self.clipboard.del_layer(layer)
		self.clipboard.selected_layer = self.clipboard.layers[0] if self.clipboard.layers else None
		self.canvas.after_idle(self.refresh)


class ClipTile(BaseTile):
	def __init__(self, manager, cliplayer):
		BaseTile.__init__(self, manager)
		self.layer = cliplayer
		self.id = cliplayer.id
		self.thumbnail = None
		self.references = []
		self.active = cliplayer.active
		self.active_references = []

	def set_dimensions(self, x, y, width, height):
		self.x, self.y, self.width, self.height = x, y, width, height
		self.trash_x, self.trash_y = self.x + self.width + 4, self.y + self.height - 16

	def get_thumbnail(self, size = 50):
		self.thumbnail = self.layer.image.resize((70,70), Image.BOX)
		return self.thumbnail

	def check_click_regions(self, pointer_x, pointer_y):
		def in_bounds(x, y, width, height):
			left_bound = x
			right_bound = x + width
			top_bound = y
			bottom_bound = y + height
			if pointer_x > left_bound and pointer_x < right_bound:
				if pointer_y > top_bound and pointer_y < bottom_bound:
					return True
		# def is_in_new_layer(): return in_bounds(self.new_x, self.new_y, 16, 16)
		# def is_in_new_from_image(): return in_bounds(self.new_from_image_x, self.new_from_image_y, 16, 16)
		def is_in_trash(): return in_bounds(self.trash_x, self.trash_y, 16, 16)
		# def is_in_copy(): return in_bounds(self.copy_x, self.copy_y, 16, 16)
		# def is_in_up(): return in_bounds(self.up_x, self.up_y, 16, 16)
		# def is_in_down(): return in_bounds(self.down_x, self.down_y, 16, 16)
		# def is_in_name(): return in_bounds(self.name_x, self.name_y, 17, 16) #Intentional 17 due to extra wide icon
		# def is_in_carret(): return in_bounds(self.carret_x, self.carret_y, 16, 16) #Intentional 17 due to extra wide icon
		# if is_in_new_layer(): self.manager.new_layer(self.frame); return True
		# if is_in_new_from_image(): self.manager.new_layer_from_image(self.frame); return True
		if is_in_trash(): self.manager.delete_layer(self.layer); return True
		# if is_in_copy(): self.manager.copy_frame(self.frame);	return True
		# if is_in_up(): self.manager.promote_frame(self.frame); return True
		# if is_in_down(): self.manager.demote_frame(self.frame); return True
		# if is_in_name(): self.manager.rename_frame(self.frame); return True
		# if is_in_carret(): self.manager.toggle_collapsed(self.frame); return True