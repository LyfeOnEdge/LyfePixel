from .colormath import rgb_to_hex, hex_to_rgba
from PIL import Image, ImageTk, ImageOps, ImageDraw
from numpy import asarray, zeros, uint8
import io

def crop(layer,start_id,end_id):
	layer.export_image()
	x1, y1 = (int(v) for v in start_id.split("x"))
	x2, y2 = (int(v) for v in end_id.split("x"))
	im_crop = im.crop((min(x1, x2), min(y1,y2), max(x1, x2), max(y1,y2)))

def flip_layer_vertical(layer):
	layer.load_image(ImageOps.flip(layer.export_image()))
def flip_layer_horizontal(layer):
	layer.load_image(ImageOps.mirror(layer.export_image()))
def merge_layers(layer, layer2):
	merged_images = Image.fromarray(layer2.get_data())
	img2 = Image.fromarray(layer.get_data())
	merged_images.paste(img2, (0,0), img2)
	return merged_images
def convert_layer_to_grayscale(layer):
	image = asarray(ImageOps.grayscale(layer.export_image()))
	out_array = zeros((layer.height, layer.width, 3), dtype=uint8)
	for x, y in layer.itterate_layer():
		d = image[y][x]
		out_array[y][x] = [d, d, d]
	layer.load_image(Image.fromarray(out_array))
def invert_layer(layer):
	layer.load_image(ImageOps.invert(layer.export_image()))
def rotate_layer_left(layer):
	layer.load_image(layer.export_image().rotate(90).resize((layer.width, layer.height), Image.BOX))
def rotate_layer_right(layer):
	layer.load_image(layer.export_image().rotate(-90).resize((layer.width, layer.height), Image.BOX))






class LyfeLayer:
	def __init__(self, id, width, height, data = None):
		self.id = id
		self.width = width
		self.height = height
		self.active = False
		self.array = zeros((self.height, self.width, 4), dtype=uint8)
		self.image = None
		self.collapsed = False
		self.selection = []

	def set_id(self, id): self.id = id
	def get_ints_from_id(self, id): return (int(v) for v in id.split("x"))
	def copy(self):
		l = LyfeLayer(self.id, self.width, self.height)
		for y in range(self.height):
			for x in range(self.width):
				l.array[y][x] = self.array[y][x] 
		return l

	def set_pixel_color(self, id, color):
		x, y = self.get_ints_from_id(id)
		self.array[y][x] = color

	def get_pixel_color(self, id):
		x, y = self.get_ints_from_id(id)
		color = self.array[y][x]
		return color

	def itterate_layer_id(self):
		for j in range(self.height):
			for i in range(self.width):
				yield f"{i}x{j}"

	def itterate_layer(self):
		for y in range(self.height):
			for x in range(self.width):
				yield x, y

	def activate(self): self.active = True
	def deactivate(self): self.active = False
	def collapse(self): self.collapsed = True
	def uncollapse(self): self.collapsed = False
	def export_array(self): return self.array
	def load_array(self, array): self.array = array
	def export_image(self):
		self.image = Image.fromarray(self.export_array(), 'RGBA')
		return self.image
	def export_image_bytes(self):
		bytes_array = io.BytesIO()
		self.export_image().save(bytes_array, format="PNG")
		return bytes_array.getvalue()
	def load_image(self, image):
		image = image.resize((self.width, self.height), Image.BOX)
		self.load_array(asarray(image))
	def flip_vertical(self): flip_layer_vertical(self)
	def flip_horizontal(self): flip_layer_horizontal(self)
	def convert_layer_to_grayscale(self): convert_layer_to_grayscale(self)
	def invert(self): invert_layer(self)
	def rotate_left(self): rotate_layer_left(self)
	def rotate_right(self): rotate_layer_right(self)
	def flood_fill_layer(self, xy, color): flood_fill_layer(self, xy, color)

class LyfeFrame:
	def __init__(self, id, width, height):
		self.id = id
		self.height = height
		self.width = width 
		self.layers = []
		self.active = False
		self.selected_layer = None
		self.collapsed = False
		self.new_layer()

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

	def new_layer(self):
		l = LyfeLayer("New Layer", self.width, self.height)
		self.layers.append(l)
		self.selected_layer = l
		return l

	def new_layer_from_image(self, tkimage):
		l = self.new_layer()
		l.load_image(tkimage)

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

	def merge_layer_down(self, layer):
		index = self.layers.index(layer)
		if index == len(self.layers) - 1: return
		layer2 = self.layers.pop(index + 1)
		merged_images = layer2.export_image()
		img2 = layer.export_image()
		merged_images.paste(img2, (0,0), img2)
		if not merged_images:
			raise
		layer.load_image(merged_images)

	def export_composite_image(self):
		images = [l.export_image() for l in self.layers]
		image = images.pop(0) #Top layer
		for i in images:
			i.paste(image, (0,0), image)
			image = i
		return image

	def export_composite_bytes(self):
		pass

	def export_composite_array(self):
		pass

class PixelProject:
	def __init__(self, width, height):
		self.id = None
		self.height = height
		self.width = width 
		self.frames = []
		self.selected_frame = None
		self.new_frame()

	def activate_frame(self, frame):
		for f in self.frames:
			if f is frame:
				f.activate()

	def toggle_collapsed(self, frame):
		for f in self.frames:
			if f is frame:
				if f.collapsed: f.uncollapse()
				else: f.collapse()

	def new_frame(self):
		f = LyfeFrame("New Frame", self.width, self.height)
		self.frames.append(f)
		self.selected_frame = f
		return f

	def del_frame(self, frame):
		self.frames.remove(frame)

	def select_frame(self, selection):
		self.selected_frame = self.frames[selection]

	def copy_frame(self, frame):
		id = frame.id
		f = self.new_frame()
		l = f.selected_layer
		f.del_layer(l)
		for l in frame.layers:
			f.layers.append(l.copy())
		f.select_layer(0)
		f.set_id(f"Copy of {id}")

	def get_frames(self):
		for frame in self.frames:
			yield frame

	def promote_frame(self, frame):
		index = self.frames.index(frame)
		if not index: return
		frame = self.frames.pop(index)
		self.frames.insert(index - 1, frame)

	def demote_frame(self, frame):
		index = self.frames.index(frame)
		if index == len(self.frames) - 1: return
		frame = self.frames.pop(index)
		self.frames.insert(index + 1, frame)

	def export_gif(self):
		images = []
		for f in self.frames: images.append(f.export_composite_image())
		return images