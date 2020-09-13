from PIL import Image, ImageTk, ImageOps, ImageDraw
from tkinter import Frame, Button, Scrollbar, ttk
import platform
from .LabeledEntry import LabeledEntry
from .colormath import hex_to_rgb
from .file_management import load_tk_image_from_bytes_array
from .ToolController import ToolController, TOOLCONST
from .ResizableCanvas import ResizableCanvas

eyedropper_symbol_gray_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00\x9fIDATx\x9c\xb5\xd2K\x0e\x800\x08\x04\xd0\xc1\x8b\x13N\xae\x1b1\x8a\xfd\xd10\xb3\xb3ixN\xa8\xa00\xaaz\xc633\x13a\x02\x9e\x83\rl#\xaaz\xfa\xe0\x19\xb0\x85\xac\x0c\x8dI\xedd\x07\x00\x8av2\xca\xf6\xebZmdf\x02\x10\x9b8\x00$w\x02\xcc[\xbc\x87{RM\xde@k\x98\xdf\x89?\xb2\x8cD \xf3\xd2\x96\x90\x11`f\x12[\xc5\xef)2\x03\xe2\xfd\xd6\xd9p\xf1Y\xa0\x97n\x93*\xa0\x8bT\x02M\xa4\x1a\xf8!\x0c\xe0\x83\xb0\x80\x07a\x02\x0f\xc2\x04\x00\xe0\xf0\xa1,\x00\xb8\x9b0\x01\x00\xa0\x0e\xf7\\\x1a\xdd\x93\xa0\x10\x9c\x9a\xcf\x00\x00\x00\x00IEND\xaeB`\x82'
pencil_symbol_gray_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00\xacIDATx\x9c\xb5\xd1\xcb\r\xc4 \x0c\x04\xd0I\xb4\x85\xd9\x95YT\x06\x9deO C\x08\xf90\xcc\xcdD\x9a\x87\x03@N\x8c\xf1h\xcf\xf6\x15@\x0b\xd1\x90\xb6\xd8\xcf\x14\xa4\xf7\x8b\xfc\xf9\xc6@F\x100\xb9\x89\x99\x95bU\xed^XU\xb7\xcfH\x06FP\x9e?!\xbe\xf8\n\xf2\xe0\xeb7i\x01\x9f\x10B\xb7\xef\xd5&#`\xf4\xfd1r\x07\x00\x93\x9b\xcc\x00\x8f\x90Y\xe0\x16a\x00C\x84\x05\\"L\xa0\x8b\xb0\x81\x13\xb2\x02\xa8\x90U@\x85\xac\x02\nbf\x87\x88@D\xe8@A|Zh\x16\x00\x80=o\xd1\x0b\x03\x00\x80\x9f\x1fRJ\xd4\xf2\nYU\x9e\xf3\x07\xccum\x9f\x08^FI\x00\x00\x00\x00IEND\xaeB`\x82'
updownleftright_symbol_gray_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00\xb1IDATx\x9c\xb5\x96Q\x0e\xc0 \x08C'\xd9\xbd\x1bN\xee\xbeL\x9cS)L\xfa9\xa5O\x01u\xe5\xda\x08@\xdd\x8d\xf7R\xd5\xc2\xce5\xe5\x017I\x04\xe0\x05\xd1\x90\xd1\xd8\x03\xa2 +C\x16dB,#\x06\xe4\xea\x88\xde\xd0\xd3M\x12\xe9\x16\x8f\x00\xd4i\xba\xa2\xe0U\xdc\x07\xf2wg\xb3x\xb1&\x9c\x00\x15\x00UUKFm\x9ao\x8a\xf9(i\xc4\x0c\xf3\xe6{\xf7\x1f\xacs\x10\x1d\x7f\x15\xfe\xd4\x8eF\x9fO\x0b\xff\x05\xcd\xe2\xa7\x871\nZ\xc5IV\xd1{\xb0\t`Z\xdcZ\xa8y\xd5[\x06L&\xa8Gke\xc4\xa6\x9a~~G\xc3\xd4ZF\xae\xa1\xedjN\xfdw=\xd1\xc3o\x9f\xa8R\x18\xfd\x00\x00\x00\x00IEND\xaeB`\x82"
updownarrow_symbol_gray_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00fIDATx\x9c\xed\x96A\x0e\x00!\x08\xc4t?Nx\xb9{7\x92\xe9p\x86;\xadJ\xc2\xb8\x96Y\x11q\xdc\x9e\xaf#pEXr\x83\x1d\x11\x92T@*\x92\x12\x05"\xa2MN\xf2\x02f&\xee\xb5\x06\xdf\xad\x91\x8cd$#\x19IQr]\x93\xbcPk_\xdeD\x01H\xae\xa0\xe7\xaa@4\xb8\xf0Ln\xa0\x93\x8cvu\xfe]?\xd9\xf2*\x1d\xee\xe3\xa2\x9c\x00\x00\x00\x00IEND\xaeB`\x82'
leftrightarrow_symbol_gray_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00RIDATx\x9c\xed\xd3A\n\x800\x0cD\xd1N.\x1e\xfe\xc9u\xa5\x14\xb1\x8a\x98\xec\xe6-[\x92O\x17\x1d\xc3\xcc>\xcb\xcc\xadz>*\x03\xab=\xb1\xba\xa8\x0c\xa9#0\x03\xa4\xce\xc0!\x00u\x06\x00\x9d\x81\xf9E\x7f\xc2w{\xe2zP\xe5q_\xc7?1\xb3w;\x83K(x5d\xef\x85\x00\x00\x00\x00IEND\xaeB`\x82'
bucket_symbol_gray_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00mIDATx\x9c\xed\x92;\x0e\x00!\x08D\xd5\xecu\xe74\x1cX+\x13\x1b\x85\x01\x8b\x8d\x81\xc4J\x98\xc7gjQ\x02@\xd7rD\xa4j9!\x00\x93\x17.\xa4A\xde\xcevu\xcd#\xc6\xc6;\x90o\xf7\xe1v\x0c\x03\xb1x\xdf\xda\xc8q]Sd\x15\x03\xd0\xe7\xb3\x00\x8e\x90\x9b\xeb\xa2\x0e\xef\x05\xbfca\x15r\xe36\xe6I"\xb0\x7f\xac+!\tIH\x19\xe27,\x90`:\x96\xb5\x00\x00\x00\x00IEND\xaeB`\x82'
eraser_symbol_gray_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00\x9eIDATx\x9c\xed\xd4I\x0e\x830\x0c\x05\xd0\x84\x8b\x7f\xfd\x93\xa7+\xaaby&\xb0\xaa\x97\xc4\xf6\x9330\xc6?\xde\x0c\x00+\xca9v\x00\x11\xd4Fdc\x0fj!VC\xeb{\x19\x89\xb6F[/!\x99C\xd6\xf2\xd2H\x16\xd0\xf2SH\x15\x90u\xf3)\xe07\xdcIv\x00$\xa7\x89\x00X$'\xc9pZ\x0f\x18\xc3\x98\xe4\x04dr\x07P\x11\tt \x99{A,\xa0\x02i9_$\x022\x90\xb5vT\x00\xaf\x99[\x7f\xe7\x9a\x02X\xe9\xfa\xbb/\xfa\xb1\x82\xf6\x0et\xff\xb2\xdb\xa1\x0e\xa0\xde\x08\xafQ\xe7\xf5\x7f\x00\xaf@uc\x98]\x9f \x00\x00\x00\x00IEND\xaeB`\x82"
line_symbol_gray_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00>IDATx\x9ccd\xa0\x01\xa8\xaf\xaf\xff\x8f\xccg\xa2\x85%\xe8`\xf8XBu\x80\x1e\x1f\xa3\x16\x8cZ0j\xc1\xa8\x05\xa3\x16\x8cZ@-\xc0\x88nhcc##\xb5-\x19>u<],\x01\x00q\xba0\xc7"<{\xe6\x00\x00\x00\x00IEND\xaeB`\x82'
rectangle_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00WIDATx\x9ccd\xa02\xa8\xaf\xaf\xff\x8f.\xc6DmK\xb0\x01F|.\xa0\x16`A\xe64662\xe2RH,\x18\xb0\xe0\xc2\xeb\x02j\x99G\x17\x9f\x8cZ2j\xc9\xa8%\xa3\x96\x8cZ\x82\x03\xb0 \x17\xc9065*/d0\x8c\x82\x0b\x9b \xb5kI\xac\x96P;N\x00\xea\xb8\x18\xa3\xbb\xe5\xcah\x00\x00\x00\x00IEND\xaeB`\x82'
select_box_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00FIDATx\x9c\xed\x96!\x12\x00 \x0c\xc3v|\xbcO\x1f\n\x1c\xa2"\xc34j\xaa\xedE\xadj\nI-\xa9\xa9\xfb\x96P\xe3\x89\xdc\xf9\xc6\x93\xbb\x88\xf0\x7fD\x97EtYD\x97EtYD\x97\xc5\x98.\xe2[!\x86?\xd9P\xa4rW\xca\xd5\xe3\x1e\x00\x00\x00\x00IEND\xaeB`\x82'
filled_rectangle_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00qIDATx\x9c\xed\x96\xd1\n\x800\x08E3\xfc\xef\x8b_nO\x03)\r\xa1[\xbdx\x9e\xdc\x10\x8e\x9bc\x9bld\x00\xf8yngK2\xe4\xae\x02\x16\x1a\x07f&Ub\x97\xacX\xed$u\xa9\x8a\xbcH\x9e\xb2D\x00|\xc5\xd4\xc6\x03\xf0\xdfN\xd7HF2\x92\x91\xbc-13a\xbc+\x11\x8d\xb7\xe6\x8a\xd9\x92O\xb6\xab|\xb4\x98\xabI%\xecOE*a\xf7\xe4\x00Cs&\xbb\x8d\xf9\xfa\xf7\x00\x00\x00\x00IEND\xaeB`\x82'
ellipse_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00\x8dIDATx\x9c\xed\x95A\x12\x80 \x0c\x03\xad\x1fg\xf2r\xbdJ\xb5M\x8a\x8c\x07\x87\\I\\\xda\x02\xdaF\xd4Z;\x98\x07\x80e\x99\xfd-@\xf1Y\xb4p\r\xfa\x9d2\x9fT\x89\n\xf0\xebQE\xb7\x0fT\x00j.\x9cI\x05\xc0\xfc\xe9\xe0g\xa9\x83\xa8\xa7\x89I\x1a|\xb5U,\xf7}\xbb\x16dA~\x02\x19\xbd\xf9Q\xae\x83\x8c\xdet/\xf9\x15\x9e\xa9\x10RmY\xe67\xbf\x08\xc0\xaa?.\xe6\xa7\xaf0\xabH\xd9\xd0c%* \xcay\xa5\x83WO\x1b\xf3\x9d\x81\x02]&s]_\x9b\x00\x00\x00\x00IEND\xaeB`\x82'
filled_ellipse_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00\x9fIDATx\x9c\xed\x96\xd1\x0e\x80 \x08E\xb5\xf5\xdf\x8e/\xaf\'6"/\x08\xba\x1e\x9aw\xeb\x89Kg\x80F\xb58j\xad]\x9e\x87\x88\xaa\x95sz\x00\xfd\x82\x8c\x0f\x06d\xa2U\x8d\xf4 \xff1\x03\x90q"\xaa\xc8\xfb\xaa$\x02\x90\xeaU\xc4\xeaV\x12\x05x~\x08Y\xa9\x07d\xf44Y\xea\xcd\x06\x0e>\x03@y\xdf\xb7kC6\xe4\'\x90\xec\xadGy\x876eo;+\xf4\x15^)\x08\x89\xb6\xcc\\\xbf\xba=\xdc\xb2\xc8\xe2\xb2\x16V)\xc6\xe0\xe5Z\x9d\x01\x14\x0e\xcaG\xc7\xbc*F|\xe6/\xd1\xe8i\xf3\xaa\xbd\x01\xe0\xd4\x85\x95\x04;\xab\x01\x00\x00\x00\x00IEND\xaeB`\x82'
move_selection_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x19\x00\x00\x00\x19\x08\x06\x00\x00\x00\xc4\xe9\x85c\x00\x00\x00\xa3IDATx\x9c\xc5V\xd1\x12\x80 \x08S~\x9c\xe3\xcb\xeb\x89\xee\xd4\x84Aj{\xeab\x0c\xdaAZ\xca)0\xf3\xc5\xcc\xd7\xae\xe7\xa7H\xa4\xa1(\xb7\xa2\t}\x01\x11\x81s\t\xed\xae\xe7Dr\x08\xe9d&\x18\xb1.\x84\x8c0lW\x06!\xbb\xb6\xc0\xfa\xb2Ll\xb0\xeb\xabuoZ4#X\x02(OQg\x81\x15\xd0\x85\xadZ@D\xaa\xb7\xd1\xd1\xb8\xea6vy\xbf\n\x8d\xa3<\x13\xab\xa7\xcb\x0f.\xe0\xfe\xb7\x8c\x162S\xd8LWF\xd8\xcb\x1b\xa6+*\x84\x1e\\GN\xc6!y\x07\x97\xfa\x17\xde\xedC7\x19\xe1\xa3\xcd,\xc1\rN$\xd3:r\x9eWL\x00\x00\x00\x00IEND\xaeB`\x82'

class draw_frame(Frame):
	def __init__(self, controller, *args, **kwargs):
		Frame.__init__(self)
		self.controller = controller
		self.radius_entry = LabeledEntry("Draw Radius", 1)
		self.radius_entry.pack(side = "top", fill = "x", expand = True, padx = 4, pady = 4)

class erase_frame(Frame):
	def __init__(self, controller, *args, **kwargs):
		Frame.__init__(self)
		self.controller = controller
		self.radius_entry = LabeledEntry("Eraser Radius", 1)
		self.radius_entry.pack(side = "top", fill = "x", expand = True, padx = 4, pady = 4)

class draw_line_frame(Frame):
	def __init__(self, controller, *args, **kwargs):
		Frame.__init__(self)
		self.controller = controller
		self.thickness_entry = LabeledEntry("Brush Thickness", 1)
		self.thickness_entry.pack(side = "top", fill = "x", expand = True, padx = 4, pady = 4)

class draw_row_frame(Frame):
	def __init__(self, controller, *args, **kwargs):
		Frame.__init__(self)
		self.controller = controller
		self.thickness_entry = LabeledEntry("Brush Thickness", 1)
		self.thickness_entry.pack(side = "top", fill = "x", expand = True, padx = 4, pady = 4)

class draw_column_frame(Frame):
	def __init__(self, controller, *args, **kwargs):
		Frame.__init__(self)
		self.controller = controller
		self.thickness_entry = LabeledEntry("Brush Thickness", 1)
		self.thickness_entry.pack(side = "top", fill = "x", expand = True, padx = 4, pady = 4)

class draw_rectangle_frame(Frame):
	def __init__(self, controller, *args, **kwargs):
		Frame.__init__(self)
		self.controller = controller
		self.thickness_entry = LabeledEntry("Rectangle Thickness", 1)
		self.thickness_entry.pack(side = "top", fill = "x", expand = True, padx = 4, pady = 4)

class fill_frame(Frame):
	def __init__(self, controller, *args, **kwargs):
		Frame.__init__(self)
		self.controller = controller
		self.threshold_entry = LabeledEntry("Fill Threshold", 1)
		self.threshold_entry.pack(side = "top", fill = "x", expand = True, padx = 4, pady = 4)

class ToolBox(Frame):
	def __init__(self, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
		self.config(height = 200, width = 200)
		self.eyedropper_symbol = load_tk_image_from_bytes_array(eyedropper_symbol_gray_bytes)
		self.pencil_symbol = load_tk_image_from_bytes_array(pencil_symbol_gray_bytes)
		self.updownleftright = load_tk_image_from_bytes_array(updownleftright_symbol_gray_bytes)
		self.updownarrow_symbol = load_tk_image_from_bytes_array(updownarrow_symbol_gray_bytes)
		self.leftrightarrow_symbol = load_tk_image_from_bytes_array(leftrightarrow_symbol_gray_bytes)
		self.bucket_symbol = load_tk_image_from_bytes_array(bucket_symbol_gray_bytes)
		self.eraser_symbol = load_tk_image_from_bytes_array(eraser_symbol_gray_bytes)
		self.line_symbol = load_tk_image_from_bytes_array(line_symbol_gray_bytes)
		self.rectangle_symbol = load_tk_image_from_bytes_array(rectangle_symbol_bytes)
		self.filled_rectangle_symbol = load_tk_image_from_bytes_array(filled_rectangle_bytes)
		self.select_box_symbol = load_tk_image_from_bytes_array(select_box_symbol_bytes)
		self.ellipse_symbol = load_tk_image_from_bytes_array(ellipse_symbol_bytes)
		self.filled_ellipse_symbol = load_tk_image_from_bytes_array(filled_ellipse_symbol_bytes)
		self.move_selection_symbol = load_tk_image_from_bytes_array(move_selection_symbol_bytes)

		self.tool_symbol_map = {
			TOOLCONST.DRAW : self.pencil_symbol,
			TOOLCONST.LINE : self.line_symbol,
			TOOLCONST.SELECT_BOX : self.select_box_symbol,
			TOOLCONST.MOVE_SELECTION : self.move_selection_symbol,
			TOOLCONST.RECTANGLE : self.rectangle_symbol,
			TOOLCONST.FILLED_RECTANGLE: self.filled_rectangle_symbol,
			TOOLCONST.ELLIPSE : self.ellipse_symbol,
			TOOLCONST.FILLED_ELLIPSE : self.filled_ellipse_symbol,
			TOOLCONST.BUCKET : self.bucket_symbol,
			TOOLCONST.DRAW_ROW : self.leftrightarrow_symbol,
			TOOLCONST.DRAW_COLUMN : self.updownarrow_symbol,
			# TOOLCONST.EYEDROPPER : self.eyedropper_symbol,
			TOOLCONST.ERASE : self.eraser_symbol,
		}

		self.thumbnails = []
		self.tiles = []
		self.canvas_height = 200

		#make canvas and scroll bar
		self.canvas = ResizableCanvas(self, relief="sunken")
		self.canvas.config(
			width = 200, #Parent frame width
			height = 200,
			highlightthickness=0)
		self.scrollbar = Scrollbar(self)

		#Bind sidebar to canvas and
		self.scrollbar.config(command=self.on_scroll_bar)           
		self.canvas.config(yscrollcommand=self.scrollbar.set) 

		#pack the sidebar and canvas
		self.scrollbar.pack(side="right", fill="y")                     
		self.canvas.pack(side = "right", expand=True, fill="both")

		#A frame to put in the canvas window
		self.canvas_frame = Frame(self.canvas, border = 0, highlightthickness = 0)
		self.canvas_frame.bind("<MouseWheel>", self._on_mouse_wheel)

		#Creates a "window" and places the canvas in it
		self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')

		#Bind resize
		# self.bind("<Configure>", self.on_configure)
		self.bind("<MouseWheel>", self._on_mouse_wheel)
		self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)

		self.canvas_frame.config(width= 200, height = 200)
		self.canvas.config(scrollregion=(0,0, 200, self.canvas_height))

		self.canvas.bind("<Enter>", self.mouse_enter)
		self.canvas.bind("<Leave>", self.mouse_leave)
		self.canvas.bind("<Motion>", self.on_mouse_move)
		self.canvas.bind("<Button-1>", self.on_click)
		self.canvas.bind("<Configure>", self.on_configure)
		self.bind("<Configure>", self.on_configure)

		if kwargs.get("controller"):
			self.controller = kwargs.pop("controller")
		else:
			self.controller = ToolController

		self.refresh()

	def on_configure(self, event = None):
		self.refresh()
		self.canvas.config(
			width=self.winfo_width(),
			height=self.winfo_height(),
			highlightthickness=0)

	def mouse_enter(self, event): pass
	def mouse_leave(self, event): pass
	def on_click(self, event):
		y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
		x = event.x
		for t in self.tiles:
			if t.is_in_range(x,y):
				ToolController.set_tool(t.tool)
				self.refresh()
			else: t.deactivate()

	def on_mouse_move(self, event):
		y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
		x = event.x
		for t in self.tiles:
			if t.is_in_range(x,y):
				if t.active: continue
				else: t.activate()
			else: t.deactivate()

	def refresh(self, event = None):
		self.winfo_toplevel().update_idletasks()
		self.canvas.delete("all")
		self.thumbnails = []
		self.tiles = []

		self.canvas.delete("all")
		BUTTONWIDTH = 25.0
		padding = 10.0
					   
		x_spacing = BUTTONWIDTH + padding
		y_spacing = BUTTONWIDTH + padding
		y_space_offset = padding
		#Set the width 
		_framewidth = self.canvas.winfo_width() - self.scrollbar.winfo_width()
		self.canvas_frame.config(width=_framewidth)
		#Get integer number of tiles fittable in the window
		_maxperrow = _framewidth // x_spacing
		#If there's not enough room to build anything
		if not _maxperrow:
			return
		empty_space = _framewidth - (_maxperrow * x_spacing)
		space_offset = empty_space / (_maxperrow + 1)
		_y = 0
		_x = 0
		for t in self.tool_symbol_map:
			base_y = _y * y_spacing + padding + (_y + 1) * (y_space_offset)
			base_x = _x * x_spacing + padding + (_x + 1) * (space_offset)

			tt = ToolTile(self, t, self.tool_symbol_map[t])
			self.tiles.append(tt)
			tt.set_dimensions(base_x,  base_y, x_spacing, y_spacing)
			self.place_tile(tt)
			_x += 1
			if _x == _maxperrow:
				_x = 0
				_y += 1

		_canvasheight = (_y + 1) * (y_spacing)
		if _canvasheight < self.winfo_height():
			_canvasheight = self.winfo_height()
		self.canvas_frame.config(height = _canvasheight,width= _framewidth)
		self.canvas.config(scrollregion=(0,0,_framewidth, _canvasheight))
		

	def place_tile(self, tile):
		tn = tile.thumbnail
		self.thumbnails.append(tn)
		tile.references.append(self.canvas.create_image(tile.x + 4, tile.y + 4, anchor = "nw", image = tn))
		if tile.active: self.activate_tile()
		if tile.tool == ToolController.tool: self.select_tile(tile)

	def select_tile(self, tile):
		self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 2),
		
	def activate_tile(self, tile):
		tile.active_references.extend([
			self.canvas.create_rectangle(tile.x, tile.y, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 1),
		])

	def deactivate_tile(self, tile):
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

class ToolTile:
	def __init__(self, manager, tool, thumbnail):
		self.x, self.y, self.width, self.height = None, None, None, None
		self.manager = manager
		self.thumbnail = thumbnail
		self.references = []
		self.active_references = []
		self.active = False
		self.tool = tool

	def set_dimensions(self, x, y, width, height):
		self.x, self.y, self.width, self.height = x, y, width, height

	def set_id(self, id): self.id = id

	def activate(self):
		self.active = True
		self.manager.activate_tile(self)

	def deactivate(self):
		self.active = False
		self.manager.deactivate_tile(self)

	def is_in_range(self, pointer_x, pointer_y):
		left_bound = self.x
		right_bound = self.x + self.width
		top_bound = self.y
		bottom_bound = self.y + self.height
		if pointer_x > left_bound and pointer_x < right_bound:
			if pointer_y > top_bound and pointer_y < bottom_bound:
				return True

	def on_click(self, pointer_x, pointer_y): return self.check_click_regions(pointer_x, pointer_y)

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
		# if is_in_new_layer(): self.manager.new_layer(self.frame); return True