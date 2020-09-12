from .colormath import hex_to_rgb
from .file_management import load_tk_image_from_bytes_array
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFilter


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
MOVE_SELECTION = "moveselect"
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
		self.MOVE_SELECTION = MOVE_SELECTION

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
	MOVE_SELECTION : {
		"text" : "Move Selection",
		"drag" : True,
	}
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
			MOVE_SELECTION : self.start_drag,
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
			MOVE_SELECTION : self.end_move_selection,
			ELLIPSE : self.end_ellipse,
			FILLED_ELLIPSE: self.end_filled_ellipse,
		}
		self.set_color((0,0,0,255))
		self.start_id = None
		self.end_id = None
		self.start_selection = None
		self.end_selection = None

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
		self.end_selection = end_id
		self.start_selection = self.start_id
		return self.select_box(layer, self.start_selection, self.end_selection)

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
		image.paste(crop, (min(x0, x1), min(y0, y1)), crop)
		return image

	def end_move_selection(self, layer, end_id):
		self.end_id = end_id
		return self.move_selection(layer, self.start_id, self.end_id)

	def move_selection(self, layer, start_move_id, end_move_id):
		image = layer.export_image()
		x0, y0 = (int(v) for v in self.start_selection.split("x"))
		x1, y1 = (int(v) for v in self.end_selection.split("x"))
		x0, x1 = min(x0, x1), max(x0, x1)
		y0, y1 = min(y0, y1), max(y0, y1)
		selection_width = x1 - x0
		selection_height = y1 - y0
		crop = self.crop_to_selection(layer, self.start_selection, self.end_selection).convert("RGBA")
		empty_cover = Image.new("RGBA",(selection_width + 1, selection_height + 1), (0,0,0,0))
		image.paste(empty_cover, (x0, y0, x1 + 1, y1 + 1))
		x2, y2 = (int(v) for v in start_move_id.split("x"))
		x3, y3 = (int(v) for v in end_move_id.split("x"))
		moved_x = x3 - x2
		moved_y = y3 - y2
		print(f"Moving {moved_x}, {moved_y}")
		image.paste(crop, (x0 + moved_x, y0 + moved_y))
		new_selection_start_x = x0 + moved_x
		new_selection_end_x = x1 + moved_x
		new_selection_start_y = y0 + moved_y
		new_selection_end_y = y1 + moved_y
		if new_selection_start_x < 0: new_selection_start_x = 0
		if new_selection_end_x > layer.width - 1: new_selection_end_x = layer.width - 1
		if new_selection_start_y < 0: new_selection_start_y = 0
		if new_selection_end_y > layer.height - 1: new_selection_end_y = layer.height - 1
		self.start_selection = f"{new_selection_start_x}x{new_selection_start_y}"
		self.end_selection = f"{new_selection_end_x}x{new_selection_end_y}"
		
		self.select_box(layer, self.start_selection, self.end_selection, mode = OVERWRITE_SELECTION)
		return image

	def effect_blur_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.BLUR)
		layer.load_image(image)

	def effect_contour_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.CONTOUR)
		layer.load_image(image)

	def effect_detail_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.DETAIL)
		layer.load_image(image)

	def effect_edge_enhance_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.EDGE_ENHANCE)
		layer.load_image(image)

	def effect_edge_enhance_more_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
		layer.load_image(image)

	def effect_emboss_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.EMBOSS)
		layer.load_image(image)

	def effect_find_edges_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.FIND_EDGES)
		layer.load_image(image)

	def effect_sharpen_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.SHARPEN)
		layer.load_image(image)

	def effect_smooth_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.SMOOTH)
		layer.load_image(image)

	def effect_smooth_more_layer(self, layer):
		image = layer.export_image()
		image = image.filter(ImageFilter.SMOOTH_MORE)
		layer.load_image(image)

	def effect_gaussian_layer(self, layer, radius = 2):
		image = layer.export_image()
		image = image.filter(ImageFilter.GaussianBlur(radius = radius))
		layer.load_image(image)

	def effect_box_blur_layer(self, layer, radius = 2):
		image = layer.export_image()
		image = image.filter(ImageFilter.BoxBlur(radius = radius))
		layer.load_image(image)

	def effect_unsharp_mask_layer(self, layer, radius=2, percent=150, threshold=3):
		image = layer.export_image()
		image = image.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))
		layer.load_image(image)

	def effect_kernal_layer(self, size, kernel, scale=None, offset=0):
		image = layer.export_image()
		image = image.filter(ImageFilter.Kernel(size, kernel, scale=None, offset=0))
		layer.load_image(image)

	def effect_rank_layer(self, size, kernel, scale=None, offset=0):
		image = layer.export_image()
		image = image.filter(ImageFilter.Kernel(size, kernel, scale=None, offset=0))
		layer.load_image(image)



# ImageFilter.RankFilter(size, rank)
# ImageFilter.MedianFilter(size=3)
# ImageFilter.MinFilter(size=3)
# ImageFilter.MaxFilter(size=3)
# ImageFilter.ModeFilter(size=3)
# ImageDraw.ImageDraw.arc(xy, start, end, fill=None)
# ImageDraw.ImageDraw.chord(xy, start, end, fill=None, outline=None)
# ImageDraw.ImageDraw.pieslice(xy, start, end, fill=None, outline=None)
# ImageDraw.ImageDraw.polygon(xy, fill=None, outline=None)
# ImageEnhance.Color(image, 1.0)
# ImageEnhance.Contrast(image) 0 - 1
# ImageEnhance.Brightness(image) 0 -> 1
# ImageEnhance.Sharpness(image) 0 -> 2
# ImageOps.autocontrast(image, cutoff=0, ignore=None) #Normalize
# ImageOps.colorize(image, black, white) #Colorize Grayscale
# ImageOps.equalize(image, mask=None)
# ImageOps.expand(image, border=0, fill=0) #For canvas resize
# ImageOps.fit(image, size, method=0, bleed=0.0, centering=(0.5, 0.5))
# ImageOps.posterize(image, bits)
# ImageOps.solarize(image, threshold=128)


ToolController = Controller()

def make_checkerboard(width, height, repeat = 14, color_1 = (127,127,127,255), color_2 = (64,64,64,255)):
	image = Image.new("RGBA",(width, height), (0,0,0,0))
	draw = ImageDraw.Draw(image)
	w, h = image.size
	draw.rectangle((0, 0, w, h), fill = color_1)
	wmax, rem = divmod(width, repeat)
	hmax, rem = divmod(height, repeat)
	for x in range(wmax + 1):
		for y in range(hmax + 1):
				if (x + y) % 2:	draw.rectangle((x * repeat, y * repeat, (x + 1) * repeat, (y + 1) * repeat), fill = color_2)
	return image