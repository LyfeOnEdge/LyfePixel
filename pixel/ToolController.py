from .colormath import hex_to_rgb
from .file_management import load_tk_image_from_bytes_array
from PIL import Image, ImageTk, ImageOps, ImageDraw


DRAW = "draw"
DRAW_ROW = "vertical"
DRAW_COLUMN = "horizontal"
EYEDROPPER = "eyedropper"
BUCKET = "bucket"
LINE = "line"
RECTANGLE = "rectangle"
FILLED_RECTANGLE = "filledrectangle"
ERASE = "erase"
SELECT_BOX = "selectbox"
ELLIPSE = "ellipse"
FILLED_ELLIPSE = "filledellipse"

OVERWRITE_SELECTION = "overwriteselection"
EXTEND_SELECTIION = "extendselection"


class constants:
	def __init__(self):
		self.DRAW = DRAW
		self.DRAW_ROW = DRAW_ROW
		self.DRAW_COLUMN = DRAW_COLUMN
		self.EYEDROPPER = EYEDROPPER
		self.BUCKET = BUCKET
		self.LINE = LINE
		self.RECTANGLE = RECTANGLE
		self.FILLED_RECTANGLE = FILLED_RECTANGLE
		self.ELLIPSE = ELLIPSE
		self.FILLED_ELLIPSE = FILLED_ELLIPSE
		self.ERASE = ERASE
		self.SELECT_BOX = SELECT_BOX
		self.OVERWRITE_SELECTION = OVERWRITE_SELECTION
		self.EXTEND_SELECTIION = EXTEND_SELECTIION
		

TOOLCONST = constants()

TOOLS = {
	DRAW : {
		"text" : "Draw",
		"drag" : False,
	},
	
	LINE : {
		"text" : "Draw Line",
		"drag" : True,
	},

	DRAW_COLUMN : {
		"text" : "Fill Vertical",
		"drag" : False,
	},

	DRAW_ROW : {
		"text" : "Fill horizontal",
		"drag" : False,
	},

	RECTANGLE : {
		"text" : "Draw Rectangle",
		"drag" : True,
	},

	FILLED_RECTANGLE : {
		"text" : "Draw Filled Rectangle",
		"drag" : True,
	},

	ELLIPSE : {
		"text" : "Draw Ellipse",
		"drag" : True,
	},

	FILLED_ELLIPSE : {
		"text" : "Draw Filled Ellipse",
		"drag" : True,
	},

	BUCKET : {
		"text" : "Bucket Fill",
		"drag" : False,
	},

	EYEDROPPER : {
		"text" : "Eyedropper",
		"drag" : False,
	},
	ERASE : {
		"text" : "Eraser",
		"drag" : False,
	},
	SELECT_BOX : {
		"text" : "Select Box",
		"drag" : True,
	},
}

class Controller:
	def __init__(self):
		self.tool = DRAW
		self.drag = False
		self._color = None
		self.start_dict = {
			ERASE: self.erase,
			DRAW : self.draw,
			LINE : self.start_drag,
			DRAW_ROW : self.draw_row,
			DRAW_COLUMN : self.draw_column,
			RECTANGLE : self.start_drag,
			FILLED_RECTANGLE : self.start_drag,
			BUCKET : self.flood_fill,
			EYEDROPPER : self.eyedropper,
			SELECT_BOX : self.start_drag,
			ELLIPSE : self.start_drag,
			FILLED_ELLIPSE : self.start_drag,
		}
		self.drag_dict = {
			ERASE: self.erase,
			DRAW : self.draw,
			DRAW_ROW : self.draw_row,
			DRAW_COLUMN : self.draw_column,
			BUCKET : self.flood_fill,
			EYEDROPPER : self.eyedropper,
		}
		self.end_dict = {
			LINE : self.end_line,
			RECTANGLE : self.end_rectangle,
			FILLED_RECTANGLE: self.end_filled_rectangle,
			SELECT_BOX : self.end_select_box,
			ELLIPSE : self.end_ellipse,
			FILLED_ELLIPSE: self.end_filled_ellipse,
		}
		self.set_color((0,0,0,255))
		self.start_id = None
		self.end_id = None

	def set_color(self, color):
		self._color = tuple([int(v) for v in color])
		print(f"Color set to {self._color}")

	def get_color(self):
		return self._color

	def set_tool(self, tool):
		print(f"Set Tool - {tool}")
		self.tool = tool
		self.drag = TOOLS[self.tool]["drag"]

	def get_tool(self, tool):
		return self.tool

	def draw(self, layer, id, radius = 1):
		x, y = (int(v) for v in id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		draw.point((x, y), fill = tuple(self._color))
		return image

	def start_drag(self, layer, start_id):
		self.start_id = start_id

	def end_line(self, layer, end_id):
		self.end_id = end_id
		return self.draw_line(layer, self.start_id, self.end_id)

	def draw_line(self, layer, start_id, end_id, width = 1):
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		draw.line((x0, y0, x1, y1), width=width, fill = self._color)
		return image

	def draw_row(self, layer, id, width = 1):
		x, y = (int(v) for v in id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		draw.line((0, y, layer.width-1, y), width=width, fill = self._color)
		return image

	def draw_column(self, layer, id, width = 1):
		x, y = (int(v) for v in id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		draw.line((x, 0, x, layer.height - 1), width=width, fill = self._color)
		return image

	def end_rectangle(self, layer, end_id):
		self.end_id = end_id
		return self.draw_rectangle(layer, self.start_id, self.end_id)

	def end_filled_rectangle(self, layer, end_id):
		self.end_id = end_id
		return self.draw_filled_rectangle(layer, self.start_id, self.end_id)

	def draw_rectangle(self, layer, start_id, end_id, fill = False, width = 1):
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		fill = self._color if self._color else fill
		draw.rectangle((x0, y0, x1, y1), outline = fill)
		return image

	def draw_filled_rectangle(self, layer, start_id, end_id, fill = False, width = 1):
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		fill = self._color if self._color else fill
		draw.rectangle((x0, y0, x1, y1), fill = fill)
		return image

	def end_select_box(self, layer, end_id):
		self.end_id = end_id
		return self.select_box(layer, self.start_id, self.end_id)

	def select_box(self, layer, start_id, end_id, mode = OVERWRITE_SELECTION):
		x1, y1 = (int(v) for v in start_id.split("x"))
		x2, y2 = (int(v) for v in end_id.split("x"))
		ids = []
		for x in range(max(0, min(x1, x2)), min(max(x1, x2), layer.width - 1) + 1):
			for y in range(max(0, min(y1, y2)), min(max(y1, y2), layer.height - 1) + 1):
				ids.append(f"{x}x{y}")
		if mode == OVERWRITE_SELECTION:
			layer.selection = ids
		elif mode == EXTEND_SELECTIION:
			for id in ids:
				if id not in layer.selection:
					layer.selection.append(id)
		return layer.image #send layers last exported image since no data has changed but canvas needs a rewrite

	def end_ellipse(self, layer, end_id):
		self.end_id = end_id
		return self.draw_ellipse(layer, self.start_id, self.end_id)

	def draw_ellipse(self, layer, start_id, end_id):
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		fill = self._color
		draw.ellipse((min(x0, x1), min(y0, y1), min(max(x0, x1), layer.width - 1), min(max(y0, y1), layer.height - 1)), outline = fill)
		return image

	def end_filled_ellipse(self, layer, end_id):
		self.end_id = end_id
		return self.draw_filled_ellipse(layer, self.start_id, self.end_id)

	def draw_filled_ellipse(self, layer, start_id, end_id):
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		fill = self._color
		draw.ellipse((min(x0, x1), min(y0, y1), min(max(x0, x1), layer.width - 1), min(max(y0, y1), layer.height - 1)), fill = fill)
		return image

	def flood_fill(self, layer, id, thresh = 0):
		x, y = (int(v) for v in id.split("x"))
		image = layer.export_image()
		ImageDraw.Draw(image)
		ImageDraw.floodfill(image, xy = (x, y), value = self._color, thresh = thresh)
		return image

	def erase(self, layer, id):
		x, y = (int(v) for v in id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		draw.point((x, y), fill = (0,0,0,0))
		return image

	def eyedropper(self, layer, id):
		x,y = (int(v) for v in id.split("x"))
		self.set_color(layer.array[y,x])
	
#---------------------------------------------
#Handles input by passing args to the function for the currently selected tool
#Allows one function to be used for input rather than an outside tool calling functions individually

	def handle_start(self, layer, *args, **kwargs): #Returns true if canvas should redraw
		if self.start_dict.get(self.tool):
			image = self.start_dict[self.tool](layer, *args, **kwargs)
			if image:
				layer.load_image(image)
				return True

	def handle_drag(self, layer, *args, **kwargs):  #Returns true if canvas should redraw
		if self.drag_dict.get(self.tool):
			image = self.drag_dict[self.tool](layer, *args, **kwargs)
			if image:
				layer.load_image(image)
				return True

	def handle_end(self, layer, *args, **kwargs):  #Returns true if canvas should redraw
		if self.end_dict.get(self.tool):
			image = self.end_dict[self.tool](layer, *args, **kwargs)
			if image:
				layer.load_image(image)
				return True

#-----------------------------------------------

	def handle_erase(self, layer, id):
		x, y = (int(v) for v in id.split("x"))
		image = layer.export_image()
		draw = ImageDraw.Draw(image)
		draw.point((x, y), fill = (0,0,0,0))
		layer.load_image(image)

	def rotate_selection_right(self, layer, start_id, end_id):
		image = layer.export_image()
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		crop = image.crop((min(x0, x1), min(y0, y1), max(x0, x1) + 1, max(y0, y1) + 1))
		size = crop.size
		crop = crop.rotate(-90).resize(size, Image.BOX)
		image.paste(crop, (min(x0, x1), min(y0, y1)))
		layer.load_image(image)

	def rotate_selection_left(self, layer, start_id, end_id):
		image = layer.export_image()
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		crop = image.crop((min(x0, x1), min(y0, y1), max(x0, x1) + 1, max(y0, y1) + 1))
		size = crop.size
		crop = crop.rotate(90).resize(size, Image.BOX)
		image.paste(crop, (min(x0, x1), min(y0, y1)))
		layer.load_image(image)

	def flip_selection_vertical(self, layer, start_id, end_id):
		image = layer.export_image()
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		crop = image.crop((min(x0, x1), min(y0, y1), max(x0, x1) + 1, max(y0, y1) + 1))
		crop = ImageOps.flip(crop)
		image.paste(crop, (min(x0, x1), min(y0, y1)))
		layer.load_image(image)

	def flip_selection_horizontal(self, layer, start_id, end_id):
		image = layer.export_image()
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		crop = image.crop((min(x0, x1), min(y0, y1), max(x0, x1) + 1, max(y0, y1) + 1))
		crop = ImageOps.mirror(crop)
		image.paste(crop, (min(x0, x1), min(y0, y1)))
		layer.load_image(image)

	def fill_selection(self, layer, start_id, end_id):
		image = layer.export_image()
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		crop = image.crop((min(x0, x1), min(y0, y1), max(x0, x1) + 1, max(y0, y1) + 1))
		draw = ImageDraw.Draw(crop)
		draw.rectangle((0, 0, crop.size[0], crop.size[1]), fill = self._color)
		image.paste(crop, (min(x0, x1), min(y0, y1)))
		layer.load_image(image)

	def crop_to_selection(self, layer, start_id, end_id):
		image = layer.export_image()
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		crop = image.crop((min(x0, x1), min(y0, y1), max(x0, x1) + 1, max(y0, y1) + 1))
		return crop

	def export_selection(self, layer, start_id, end_id):
		return self.crop_to_selection(layer, start_id, end_id)

	def new_layer_image_from_selection(self, layer, start_id, end_id):
		x0, y0 = (int(v) for v in start_id.split("x"))
		x1, y1 = (int(v) for v in end_id.split("x"))
		image = Image.new("RGBA",(layer.width, layer.height), (0,0,0,0)) #New background for layer
		crop = self.crop_to_selection(layer, start_id, end_id)
		image.paste(crop, (min(x0, x1), min(y0, y1)))
		return image

ToolController = Controller()