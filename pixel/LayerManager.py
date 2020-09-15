from tkinter import Frame, Canvas, Scrollbar, Label, simpledialog, messagebox, filedialog, ttk
from .file_management import load_tk_image_from_bytes_array
from PIL import Image, ImageTk
from .BaseTile import BaseTile
import platform

trash_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00-IDATx\x9ccd\xc0\x0e\xfe\xe3\x10g\xc4%\x80K\x03!\xc0\xc8D\xa6F\xea\x01t?\x11\xeb\x15\xb8>\x8a\xbd0j\xc0\xa8\x01\x83\xc3\x00\x00\xf2\xb9\x03\x1c\xd6\xd7\xf8 \x00\x00\x00\x00IEND\xaeB`\x82'
copy_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00TIDATx\x9c\xc5\x93;\x0e\x00 \x08C\x8b\xf1\xfeW\xd6\t\x17\xc5V1\xb1#m^\x08\x1f\x03\xd0\xb0\x97\x11\x9f\x02\x98\xcf\x03,\xa3\x00\xc2\\=\x84z\xddVE\x050\xf9\x85\x04#\x99Cn\x01\x03\x92\x01 \xdb\xc1\x1b\x80\xafQ\xbd\x05Y\xf2q\xfd\x9fA\xf4\xaa\xf2L:6*\x12\x0b:\xd1\x01?\x00\x00\x00\x00IEND\xaeB`\x82'
copy_bytes_wide = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00_IDATx\x9c\xbd\x91A\x0e\x00!\x08\x03\x87\xcd\xfe\xff\xcb\xee\x89D\x8c\x05\xa3f{\x14R\xa7\xc5\x80\x86\x96%3\x00\x9eb\x9e\x99\x87%\xb5\x98\xcd\x96\x08<\x824y\x93\x9f\xd5[\xe8\xa5"(\xcd\x15\x81kv\x05\xef\xc5v\tB/;\x06A}\x84\xa5\x9b\x8f\xbaB\xa0\x8a\xfa\x87\xe0j\x893\x95Q\x8e\t>k\x92\x10\x1fW\xad\x10U\x00\x00\x00\x00IEND\xaeB`\x82'
new_layer_from_image_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00cIDATx\x9c\xbd\x90Q\n\x800\x0cC_\xc5\xfb_y\xfe8\xd1\x9a-s\xa8\x81\xc1(\xe9k\x9b\x00\n\xe3\nU,\x8d\x7f\xcfwh\x99\x00I@m\xc8+ZP\x05\xc4\xfe\x9e\xe4q\x01\xa8\xa9\xf9$\x19`6\xaa\xda\x19x\xf3\xaa\r2\xa89\x19`5[t\x9b\x190\xb8P\xc3\x9d\xf0\xaa\xa6B\xb4\xfa\xf5\x84o\xb4\x01\xb9\xd6\x17\x08\x7f~yJ\x00\x00\x00\x00IEND\xaeB`\x82'
up_arrow_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00JIDATx\x9cc`\xc0\x0f\xfeC1N\xc0D@366Q\x06`\xd3\x80\xd5\x10l\x06\xe0s2\x86\x1c\xba\x01x\xfd\x8bM\r\x13.\tb\raB\x17 \xd5\x10F25\xc3\x01#>\xd3\x89Q\x8f/\x1d\x10\x05F\r\x18\x0c\x06\x00\x00\x9f\xc8\x10\x0e\xae\xb1^D\x00\x00\x00\x00IEND\xaeB`\x82'
down_arrow_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00MIDATx\x9ccd\xc0\x0e\xfe\xe3\x10gD\x17`\xc2\xa1\x90h0j\xc0`0\x80\x91\x01w\x9c\x13\xed\x02\x8c\xc4A\x8a\x03`^ \xc7\x10F\x98\x0bP\x04H\xd1\x8cn\x00\xb1\x86\xa0\xa8\xc1\x16\x0b\xf8\x0c!:3a3\x84\xac\xc0\xfe\xcf@ \x9a\x01\x86\xa4\x04&EWG\x05\x00\x00\x00\x00IEND\xaeB`\x82'
name_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x11\x00\x00\x00\x10\x08\x06\x00\x00\x00\xf01\x94_\x00\x00\x00aIDATx\x9c\xad\x92Q\n\x00 \x08Cgt\xff+\xd7W`\xc5\x9cdB\x98d\xcf1\x04r1\x8eL\x1bTMAMM\xc8\xc4\x82X\x05\xd4\xdc\xbd\x04R\x1e\xb0?\xfe\xa4\xe1\xf4\xcd\x82&s9\x84\xf4H\x8a\x08&`\x9b\x12y#=Q\xcbG%U\x96\xcd\xaa\x00\x00\x18~\xd9\x98\x17*\xdf\xc5\x8b\x92/\x9eLo\xc5+\xeb\xbc\xec0\x94\x00\x00\x00\x00IEND\xaeB`\x82'
merge_down_symbol_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00VIDATx\x9c\xddQ1\x12\x00 \x08\xc2\xfe\xffg\xdb\xea\xce YZbT\xe0\x10\x03@\xe2D\x90\x19\x18w\xb8D1\x93\x06U@\xc5\xc0\x8e*\t\r\xa2\xde\xea\x1a-]=A\x95'9\xac\x83\x9b\xc9\xb1\xbb\x95hA\x19\xb0\x144\xd9\xb3\x046>~\xa3\xfd\x85\x0e\x89\xa6\x97\t\x0fz\x0b n\xf1\x8ds\x00\x00\x00\x00IEND\xaeB`\x82"
up_carret_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00QIDATx\x9c\xed\x92\xc1\x0e\x00 \x08B\xd5\xff\xffg;\xb55\x02\xe6\xadK\x1c\xe5\x81[\x16\xf1\xf5^i\xbc\x9e\xb05\x0c\xab\x19-\xa0\xa0\xf2\xb0\xc0\x85)S\xca\x98\x96\x14\x0e@\x19\xfa\xa1{\x03.L\xb7\x9eRW`[\xc7gt\x7f\xe3\xf2\xb0\xc0\x85)\xb3\x00\xc8\xb0\r\x10{\x8cD\xc6\x00\x00\x00\x00IEND\xaeB`\x82'
down_carret_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00TIDATx\x9c\xed\x91\xb1\x12\x00\x10\x0cCS\xff\xff\xcf5qJBM\x16\x99J\x9awU\xc0\xd7{\x19\x00\x9f\xce\x19\xf5LQF&\xcc\x00'\xc8\xe21\x80\x82Pp\x81~\xb7\x8bz\x94Y\xa2I\xc9\xda\x04\xe1\xe2&<\x03\xb2\x90\xd0\xc3\x96\xb8\x83,\x9e\xfa\x05\x06\xa1\xe0\nPm\x0b\x14\xaa\x93\x9f.\x00\x00\x00\x00IEND\xaeB`\x82"
plus_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00-IDATx\x9ccd\xc0\r\xfe\xa3\xf1\x19\xb1)b\xc2c\x00Q`\xd4\x00H\xc8\xa2\x876}]0\xf0\x06`M]P0\x9a\x12\xe9e\x00\x00"\xd2\x03\x1d\x12\xb9\x81\x89\x00\x00\x00\x00IEND\xaeB`\x82'

class LayerManager(ttk.LabelFrame):
	def __init__(self, canvas_window, project, *args, **kwargs):
		ttk.LabelFrame.__init__(self, *args, **kwargs)
		self.project = project
		self.canvas_window = canvas_window
		self.thumbnails = []
		self.tiles = []
		self.canvas_height = 700
		self.trash_image = load_tk_image_from_bytes_array(trash_bytes)
		self.copy_image = load_tk_image_from_bytes_array(copy_bytes_wide)
		self.up_image = load_tk_image_from_bytes_array(up_arrow_bytes)
		self.down_image = load_tk_image_from_bytes_array(down_arrow_bytes)
		self.name_image = load_tk_image_from_bytes_array(name_symbol_bytes)
		self.merge_image = load_tk_image_from_bytes_array(merge_down_symbol_bytes)
		self.new_image = load_tk_image_from_bytes_array(plus_symbol_bytes)
		self.new_from_image_image = load_tk_image_from_bytes_array(new_layer_from_image_bytes)
		self.up_carret_image = load_tk_image_from_bytes_array(up_carret_bytes)
		self.down_carret_image = load_tk_image_from_bytes_array(down_carret_bytes)

		self.nextid = 0
		self.configure(text = "Frames")
		frame_tools_frame = Frame(self)
		frame_tools_frame.pack(side = "top", fill = "x", expand = "False")
		self.new_frame_symbol = load_tk_image_from_bytes_array(plus_symbol_bytes)
		l = Label(frame_tools_frame, image = self.new_frame_symbol)
		l.pack(side = "left")
		l.bind("<Button-1>", self.new_frame)

		self.canvas = Canvas(self, relief="sunken")
		self.canvas.config(width=200, height = 700,	highlightthickness=0)
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
		self.canvas.after_idle(self.canvas_window.refresh)
		self.bind("<MouseWheel>", self._on_mouse_wheel)

	def new_frame(self, event = None):
		self.project.new_frame()
		self.canvas_window.refresh()
	def rename_frame(self, frame):
		name = simpledialog.askstring("Rename Frame", f"What would you like to rename Frame: {frame.id} to?")
		if name:
			frame.set_id(name)
			self.canvas_window.refresh()
	def ask_delete_frame(self):
		if len(self.project.frames) == 1:
			messagebox.showwarning("Warning", "Cannot delete last frame.")
			return
		return messagebox.askyesno("Delete", "Are you sure you wish to delete this frame?\nThis cannot be undone.")
	def delete_frame(self, frame):
		if self.ask_delete_frame():
			self.project.del_frame(frame)
			self.project.selected_frame = self.project.frames[0]
			self.canvas.after_idle(self.canvas_window.refresh)
	def copy_frame(self, frame):
		self.project.copy_frame(frame)
		self.canvas.after_idle(self.canvas_window.refresh)
	def promote_frame(self, frame):
		self.project.promote_frame(frame)
		self.canvas.after_idle(self.canvas_window.refresh)
	def demote_frame(self, frame):
		self.project.demote_frame(frame)
		self.canvas.after_idle(self.canvas_window.refresh)
	def toggle_collapsed(self, frame):
		self.project.toggle_collapsed(frame)
		self.canvas.after_idle(self.canvas_window.refresh)
	def rename_layer(self, frame, layer):
		name = simpledialog.askstring("Rename Layer", f"What would you like to rename Layer: {layer.id} to?")
		if name:
			layer.set_id(name)
			self.canvas.after_idle(self.canvas_window.refresh)
	def new_layer_from_image(self, frame):
		path = filedialog.askopenfilename()
		if path:
			image = Image.open(path)
			layer = frame.new_layer_from_image(image)
			self.canvas.after_idle(self.canvas_window.refresh)
	def new_layer(self, frame):
		layer = frame.new_layer()
		frame.selected_layer = layer
		self.canvas.after_idle(self.canvas_window.refresh)
	def ask_delete_layer(self, frame, layer):
		if len(frame.layers) == 1:
			messagebox.showwarning("Warning", "Cannot delete last layer.")
			return
		return messagebox.askyesno("Delete Layer?", f"Are you sure you wish to delete this layer?\n{layer.id}")
	def delete_layer(self, frame, layer):
		if self.ask_delete_layer(frame, layer):
			frame.del_layer(layer)
			frame.selected_layer = frame.layers[0]
		self.canvas.after_idle(self.canvas_window.refresh)
	def copy_layer(self, frame, layer):
		frame.copy_layer(layer)
		self.canvas.after_idle(self.canvas_window.refresh)
	def promote_layer(self, frame, layer):
		frame.promote_layer(layer)
		self.canvas.after_idle(self.canvas_window.refresh)
	def demote_layer(self, frame, layer):
		frame.demote_layer(layer)
		self.canvas.after_idle(self.canvas_window.refresh)
	def merge_layer_down(self, frame, layer):
		frame.merge_layer_down(layer)
		self.canvas.after_idle(self.canvas_window.refresh)
	
	def mouse_enter(self, event): pass
	def mouse_leave(self, event): pass
	def on_click(self, event):
		y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
		x = event.x
		for t in self.tiles:
			if t.is_in_row(y):
				mode = t.on_click(x, y)
				if not mode:
					t.activate()
					if type(t) is FrameTile:
						self.project.selected_frame = t.frame
					elif type(t) is LayerTile:
						self.project.selected_frame = t.frame
						t.frame.selected_layer = t.layer
					self.canvas_window.refresh()
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
		if self.project.frames:
			i = 0
			y_offset = 10
			y_padding = 10
			tile_height = 80
			x = 10
			width = 80
			height = tile_height
			child_offset = 0.5 * tile_height
			for f in self.project.frames:
				y = i * tile_height + y_offset + i * y_padding
				t = FrameTile(self, f)
				self.tiles.append(t)
				t.set_dimensions(x,  y, width, height)
				self.place_tile(t)
				i += 1
				firstlayer = True
				layers = []
				if f.layers:
					if f.collapsed:
						continue

					for l in f.layers:
						floffset = x + 0.5 * child_offset
						flyoffset = y + tile_height
						if firstlayer:
							firstlayer = False
							self.canvas.create_line(floffset, flyoffset, floffset, flyoffset + y_padding + 0.5 * tile_height)
						else:
							self.canvas.create_line(floffset, y + 0.5 * child_offset, floffset, flyoffset + y_padding + 0.5 * tile_height)
						self.canvas.create_line(floffset, flyoffset + y_padding + 0.5 * tile_height, x + child_offset, flyoffset + y_padding + 0.5 * tile_height,)
						y = i * tile_height + y_offset + i * y_padding
						L = LayerTile(self, l, f)
						L.set_dimensions(x + child_offset,  y, width, height)
						self.place_tile(L)
						self.tiles.append(L)
						i += 1

			height = i * (tile_height + y_padding) + y_offset
			frameheight = self.canvas_frame.winfo_height()
			height = height if height > frameheight else frameheight
			self.canvas_height = height
			self.canvas_frame.config(width= 200, height = self.winfo_height())
			self.canvas.config(scrollregion=(0,0, 200, self.canvas_height))
		else:
			print("No frames")

	def place_tile(self, tile):
		tn = ImageTk.PhotoImage(tile.get_thumbnail(tile.height - 8))
		self.thumbnails.append(tn)
		tile.references.append(self.canvas.create_image(tile.x + 4, tile.y + 4, anchor = "nw", image = tn))
		if type(tile) is FrameTile:
			if tile.frame is self.project.selected_frame: tile.references.append(self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 3))
			else: tile.references.append(self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 1))
		elif type(tile) is LayerTile:
			if tile.layer is self.project.selected_frame.selected_layer: tile.references.append(self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 3))
			else: tile.references.append(self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 1))
		if tile.active: self.activate_tile()
		tile.references.append(self.canvas.create_text(tile.x + tile.width + 10, tile.y, font="CourierNew 8", text=tile.id, anchor = "nw"))

	def activate_tile(self, tile):
		tile.active_references.extend([
			self.canvas.create_image(tile.trash_x, tile.trash_y, anchor = "nw", image = self.trash_image),
			self.canvas.create_image(tile.copy_x, tile.copy_y, anchor = "nw", image = self.copy_image),
			self.canvas.create_image(tile.up_x, tile.up_y, anchor = "nw", image = self.up_image),
			self.canvas.create_image(tile.down_x, tile.down_y, anchor = "nw", image = self.down_image),
			self.canvas.create_image(tile.name_x, tile.name_y, anchor = "nw", image = self.name_image),
		])

		if type(tile) is FrameTile:
			if tile.frame.collapsed: carret_image = self.down_carret_image
			else: carret_image = self.up_carret_image
			tile.active_references.extend([
				self.canvas.create_image(tile.new_x, tile.new_y, anchor = "nw", image = self.new_image),
				self.canvas.create_image(tile.new_from_image_x, tile.new_from_image_y, anchor = "nw", image = self.new_from_image_image),
				self.canvas.create_image(tile.carret_x, tile.carret_y, anchor = "nw", image = carret_image),
			])
		elif type(tile) is LayerTile: tile.active_references.append(self.canvas.create_image(tile.merge_x, tile.merge_y, anchor = "nw", image = self.merge_image))

	def deactivate_tile(self, tile):
		self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 1)
		for r in tile.active_references:
			self.canvas.delete(r)

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

class FrameTile(BaseTile):
	def __init__(self, manager, frame):
		BaseTile.__init__(self, manager)
		self.frame = frame
		self.id = frame.id
		self.thumbnail = None
		self.references = []
		self.active = frame.active
		self.active_references = []

	def set_dimensions(self, x, y, width, height):
		self.x, self.y, self.width, self.height = x, y, width, height

		self.new_x, self.new_from_image_x = [self.x + self.width + 10 + (i * 20) for i in range(2)]
		self.copy_x, self.name_x, self.trash_x = [self.x + self.width + 10 + (i * 20) for i in range(3)]
		self.up_x, self.down_x, self.carret_x = [self.x + self.width + 10 + (i * 20) for i in range(3)]

		self.new_y, self.new_from_image_y, = [self.y + 20] * 2
		self.copy_y, self.name_y, self.trash_y = [self.y + 40] * 3
		self.up_y, self.down_y, self.carret_y = [self.y + 60] * 3

	def get_thumbnail(self, size):
		self.thumbnail = self.frame.export_composite_image()
		if self.thumbnail: self.thumbnail = self.thumbnail.resize((size, size), Image.BOX)
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
		def is_in_new_layer(): return in_bounds(self.new_x, self.new_y, 16, 16)
		def is_in_new_from_image(): return in_bounds(self.new_from_image_x, self.new_from_image_y, 16, 16)
		def is_in_trash(): return in_bounds(self.trash_x, self.trash_y, 16, 16)
		def is_in_copy(): return in_bounds(self.copy_x, self.copy_y, 16, 16)
		def is_in_up(): return in_bounds(self.up_x, self.up_y, 16, 16)
		def is_in_down(): return in_bounds(self.down_x, self.down_y, 16, 16)
		def is_in_name(): return in_bounds(self.name_x, self.name_y, 17, 16) #Intentional 17 due to extra wide icon
		def is_in_carret(): return in_bounds(self.carret_x, self.carret_y, 16, 16) #Intentional 17 due to extra wide icon
		if is_in_new_layer(): self.manager.new_layer(self.frame); return True
		if is_in_new_from_image(): self.manager.new_layer_from_image(self.frame); return True
		if is_in_trash(): self.manager.delete_frame(self.frame); return True
		if is_in_copy(): self.manager.copy_frame(self.frame);	return True
		if is_in_up(): self.manager.promote_frame(self.frame); return True
		if is_in_down(): self.manager.demote_frame(self.frame); return True
		if is_in_name(): self.manager.rename_frame(self.frame); return True
		if is_in_carret(): self.manager.toggle_collapsed(self.frame); return True

#This object holds both the layer data and the data for the layer panels for a respective layer
class LayerTile(BaseTile):
	def __init__(self, manager, layer, frame):
		BaseTile.__init__(self, manager)
		self.layer = layer
		self.frame = frame
		self.id = layer.id
		self.thumbnail = None
		self.references = []
		self.active = layer.active
		self.active_references = []

	def set_dimensions(self, x, y, width, height):
		self.x, self.y, self.width, self.height = x, y, width, height
		self.copy_x, self.name_x, self.trash_x = [self.x + self.width + 10 + (i * 20) for i in range(3)]
		self.up_x, self.down_x, self.merge_x = [self.x + self.width + 10 + (i * 20) for i in range(3)]

		self.copy_y, self.name_y, self.trash_y = [self.y + 40] * 3
		self.up_y, self.down_y, self.merge_y = [self.y + 60] * 3

	def get_thumbnail(self, size):
		self.thumbnail = self.layer.export_image()
		self.thumbnail = self.thumbnail.resize((size, size), Image.BOX)
		# self.thumbnail = ImageTk.PhotoImage(Image.fromarray(self.get_data(), 'RGBA').resize((50, 50), Image.BOX))
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
		def is_in_trash(): return in_bounds(self.trash_x, self.trash_y, 16, 16)
		def is_in_copy(): return in_bounds(self.copy_x, self.copy_y, 16, 16)
		def is_in_up(): return in_bounds(self.up_x, self.up_y, 16, 16)
		def is_in_down(): return in_bounds(self.down_x, self.down_y, 16, 16)
		def is_in_name(): return in_bounds(self.name_x, self.name_y, 17, 16) #Intentional 17 due to extra wide icon
		def is_in_merge(): return in_bounds(self.merge_x, self.merge_y, 16, 16)
		if is_in_trash(): self.manager.delete_layer(self.frame, self.layer); return True
		if is_in_copy(): self.manager.copy_layer(self.frame, self.layer);	return True
		if is_in_up(): self.manager.promote_layer(self.frame, self.layer); return True
		if is_in_down(): self.manager.demote_layer(self.frame, self.layer); return True
		if is_in_name(): self.manager.rename_layer(self.frame, self.layer); return True
		if is_in_merge(): self.manager.merge_layer_down(self.frame, self.layer); return True