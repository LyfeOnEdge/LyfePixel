import os, platform
from tkinter import Toplevel, Frame, Button, ttk, Menu, filedialog, Canvas, Scrollbar, Label, messagebox, simpledialog, PanedWindow, StringVar
from PIL import Image, ImageTk
from numpy import zeros, uint8, asarray
from .canvas import PixelCanvas, NewPixelCanvas
from .BaseWindow import BaseWindow
from .colormath import rgb_to_hex, hex_to_rgb
from .ImageViewer import ImageViewer
from .file_management import convert_tk_image_to_bytes_array, load_tk_image_from_bytes_array, load_tk_image_object_from_bytes_array
from .SaveMenu import SaveMenu
from .ToolBar import ToolBar
from .LayerViewer import LayerViewer
from .pixel import PixelProject
from .ToolController import ToolController, TOOLCONST
from .LyfeCanvas import LyfeCanvas
from .ToolBox import ToolBox
from .SaveMenu import SaveMenu
from .LayerManager import LayerManager

magnifying_glass_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00bIDATx\x9c\xe5RA\x0e\xc0 \x08+\xfe\xff\xcf\xecDc\x18\x16\xe6u\xbd\x98\xd0\x16\xaah\xd0p\xc1\x19\x00\xacK3y\x1b\x98+\ry\x95@\r`\xbdk\xd0\xe2\x07\rN\xabd]\xaeh\x00\xcb\t>\x99s\x82\xca|\xfa\x07D$\x98\x9a\xb3\xce\xd7\xc5d\xdf\xcfj\x0b\xca\x1c\\4y=b{\xe7Mc\x00\xf0\x00\x04\xc6\x11\x1b\xcc\xca$4\x00\x00\x00\x00IEND\xaeB`\x82'
floppy_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00YIDATx\x9c\xbd\x93A\n\x00 \x08\x04w\xa3\xff\x7f\xb9nb\x1bDj$t\x08\xb6q\x10#\x80\x81X\xd1_Z\xf01\xb4\xa1\x07P\x82tG3\x06\xc9\x18,\x90\x0c`\x81\xf4C\xe8j\xb8Y\x03+5\xd0A\xfe7\xb8]*3}n\xb0u\x90\xda\x0c\xcb\x06e\x00\x11\xff\x8do\r&2<\t)\xe6\x84\xac\xa0\x00\x00\x00\x00IEND\xaeB`\x82'
export_to_bytes_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00TIDATx\x9c\xc5R\xcb\x0e\x00 \x08\xa2\xd6\xff\xff\xb2\x9d<\xf8\xc0Z[\x93#"S\x11\xe8\xc6\x00 \x84\xcf\x90i\x03\x99\x8aXm\x16\xe2+\xf4\x1b\xac\x87\x1es\x07f \x88Ih\xa3\xe1\xd9\n>\xde\xcc\xb0\x9c\xc0\x9b\xb0\xbf\xf8\x9b\x82\x8e\xcd\xbe\x158\x14\xaf\x8e\xd8\x8f\r^q\x0f\x17I\xca\t\xc4\x00\x00\x00\x00IEND\xaeB`\x82'
to_grayscale_bytes=  b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x8bIDATx\x9c\xad\x93K\x0e\xc40\x08C\xedjn\x04\xf7\xbf\x9a\xbbh'\x9f\x16JT\xd5\xd9$!<\x8cD(@HD\x80Y\xec\xaf\xdf\x94pG\xf5\x1b\xc6\xb0\xad\xaaP\xa9\x01\xdc\xec,\xd9\xd7\x8a(@\x1c\x1eK\x00\xc9s\xaf\xee\xfcM\x0b$K'7\x00yT^\x85\xb0\x1b\x9f5\xb6r\x9c'h\x0b\xa4\x80\x0cB\x12\x92\xe0\xeeq\x0bU;W-\xcd\x81b\x83\x00\xda$\x06\xe8!=\xaa|\x01\xe4r\xf7G\x07\xe5g1\xb3\xc7A\xf8\xee/\xbc\xd5\x0e\xfa38\x83C\xf0\x9e\x91\x00\x00\x00\x00IEND\xaeB`\x82"
flip_horizontal_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00cIDATx\x9c\xb5\x92K\n\x00 \x08D\xc7\xe8\xfeW\xb6E\x10a\xa3)\xd1,\xfd\xbctL\x00(\xa6\x045)\x00\xb4b\xd3\xa1o\x00M\xc6(\x80\x16z9\x0b\x88\x0c\x15S\xb3\x82\x96z\xbb\xc6\x15P\xd2\xf3\x15:\x89\x95V\xd8'\xa0&9\xcd\xeb\x11\xbbB\x04\xa1\x17b\x1eD+\x1c9\xcf\xc4\xe8\x1f\xa4\x00i=\x03\x06R\x89\x10\x1d\x11\x13\xf1_\x00\x00\x00\x00IEND\xaeB`\x82"
flip_vertical_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00[IDATx\x9c\xcdS1\x12\x00 \x08\xc2\xfe\xffg\x9b\xba\xeb\x14tp(GQ\x025\x03\xe0\x18\xc4\x9a4\x03\x80\x15XTFk\x95\x02f\x8bZe\x04\xa7\xf0~\xd1\x02&\tXsKR\x85w\r\xe3-\xfcG\xd0yNx$\xa8&M7\xa4.Q\xa9H\xf5j\x06\xd5\x1d\xa4\xe4\xdb\xdf\xb8\x013\x0b\x12\x13\xd2\xdc\xdaE\x00\x00\x00\x00IEND\xaeB`\x82'
rotate_right_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00fIDATx\x9c\xad\x93Q\x0e\xc0 \x08C[\xb2\xfb_\x99\xfdl\xc9\x82E\xa6\xd8\xc4\x1fy\x14A\x05\x9a\xe2$\xe6\x05\xeb\x00\xa8\x0cb\xa2*\xfa2\x83\x81\x07\xb02\xa6\t\x80"Y\x19\x02\x00Lm&\x92\xadY\x08fCM\xe7r\xfd\xac\x9e\xde\xd6J\x0b_\xf9\xb3\xb6\r\xe6\xae+\\\xfb\x04\xbb\x0f\x89\x19\x14\xc1\xb2h\xe73\x9d\xd1\r4\xaa\x14\x12L4\x91\xa7\x00\x00\x00\x00IEND\xaeB`\x82'
rotate_left_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00cIDATx\x9c\xadS[\x12\x00\x11\x0c\xeb\x1a\xf7\xbfr\xf7\x07S6\xad\xd0\xcd\x0f\xfaH\xc2\x94H\x12O[\xd5\xec\xc5\xc4P\xadK\xd0\xcfk\xa3\xd7\x03\t"EE\xb9\xc2\xa8\x98\xd8G\xd0#\xd8]c\xc0#\x88H&\x17u\t\x1e\xa3;\xd0@\x91"\xf8\x05\xac\x8b\xa9.\xed\x80\x1a\x96(\x87^\xffj\x94\x11\xa8\xcf\x94\xc6\x0b\xc0j\x14\x121\x82h\xc9\x00\x00\x00\x00IEND\xaeB`\x82'
selection_options_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00aIDATx\x9c\xed\x94K\n\xc0 \x0cD\x9f\xa5\xf7\xbf\xf2t\xd3H\x08\xfd\xa8\xd1\x9d\x0f\x04cd\x98\x0c"\x80\xeee\xa4\xea\x83\xc9\x94\x89Z\x82\x05\x0eMY\xbf\xb7\x1a\xd9\x19\xe6\xd9\x19\xe6Y\xe2\xb0\x97\xafi4\xea\xf0IT~\xd3\x9b\xe1\xeb\x9f8\xea\xd0\x9e\x9b\x17.\xbeAl4\xd4\xf1L\x00\xe7\xa0\xc3\xe8\xb4r\x01\xe1\r#\xfeK\xaa+`\x00\x00\x00\x00IEND\xaeB`\x82'
layers_symbol_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00\x88IDATx\x9c\xdd\x94Q\x0e\xc0 \x08C\xd5\xfb\xdf\x99\xfd\x0c3\xb1\xd4\xea\xf65\x13\x13E\xf6V\x1a\xb4\x94|\xd8=\xb7F%05w\x99\xb4RE\xc1\xf1p\xa7D\x08~\x06\xb7\xfdB`\xdf\x9c\xc2&V\xfb\x126,^\x80\x87\x92[8\x90Z\x03\xc0\xba\x18/\xd9B\x92\x02\x86\xfe\xd7\x18\x000\xd6\xe4\x16\xf6\xd4\xc3\x0c\x9c\xc2\xd0G\n8\x83W\x0f\xc0?\x110U\xfa\x7f\x0f'Q\xac\xdf\x14\x0f\xa7\xb5\xd2\xc0\xab\xc76S+\x81\xb3\xfb\xde\xe3\x17\xc0\xce,\x11\xce3\xde\x16\x00\x00\x00\x00IEND\xaeB`\x82"
folder_options_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00dIDATx\x9c\xa5RA\x0e\xc0 \x08\x03\xb3\xff\x7f\x99\x1d\x16\x17m\xc0\x96\xd8\x0bQ\xda\xda n\x1f\xc2j\xf8\xa1g\x83\x88\x99\xb9\xf9B\xc8^\n\xe0\xb6\rh\x82qj21&`\xbc\xd4\x9c%\xa8\xc4?\x1e\x95XAIpm\x803\xda\xcej\x82\x80\xda2\x98\xb3I\xf7EM\xe0P\xdb\x06\xa9x^*\x8bT\xe2\xfa\x1b_\xdd\xf7\x10\x1a%V\x92.\x00\x00\x00\x00IEND\xaeB`\x82'
effects_wand_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00dIDATx\x9c\x9d\x93\xc1\x12\x00 \x04D\xe3\xff\xffY\xa7\x1aE\xbb\xd4%\x8c\xb7\xb32\x8d\xc1\x8f\xa1\xba4`y\xd4[\x0eB\xcc\x1cP7\xfa\x01\x1fyE \x9b\xb7\xec\x00\xc1\xf4\r(\x8c\x1c@\xdb.\x96L\x80\xc1\xe6k\xb7@\x15NG`\xb0\xcf\xc3\x16*\xf0\xea;\x1ci\x03\xf6"\xfb\x0ek!0\xec\xed\xfc\xb0\xdd;\x01\xa1\x94 \n\xf4#\xf2;\x00\x00\x00\x00IEND\xaeB`\x82'

WIDTH = 1080
HEIGHT = 720

def force_aspect(inner_frame, outer_frame, ratio):
	def force_ratio(event):
		w = event.width
		h = int(event.width / ratio)
		if h > event.height:
			h = event.height
			w = int(event.height * ratio)
		inner_frame.place( in_=outer_frame, relx = 0.5, rely = 0.5, x = - 0.5 * float(w), y = - 0.5 * float(h), width=w, height=h)
	outer_frame.bind("<Configure>", force_ratio)

def bind_popup(binding, widget, menu):
	def popup(event):
		menu.post(
			widget.winfo_rootx(),
			widget.winfo_rooty() + widget.winfo_height())
	widget.bind(binding, popup)

class ProjectWindow(BaseWindow): #A loaded canvas window
	def __init__(self, controller, width, height, *args, **kwargs):
		BaseWindow.__init__(self, controller, *args, **kwargs)
		self.controller = controller
		self.controller.configure_toplevel(self)
		self.resizable(True, True)
		self.attributes('-topmost', False) #Remove the toplevel priority
		self.set_exit_function(self.exit)
		self.set_title("Canvas")
		self.file = None
		self.width = int(width)
		self.height = int(height)
		self.geometry(f"{WIDTH}x{HEIGHT}")
		self.bind("<Escape>", self.exit)
		self.top_bar.pack(side = "top", fill = "x", pady = (2,0))
		self.magnifying_glass_image = load_tk_image_from_bytes_array(magnifying_glass_bytes)
		self.floppy_image = load_tk_image_from_bytes_array(floppy_bytes)
		self.bytes_image=  load_tk_image_from_bytes_array(export_to_bytes_bytes)
		self.horizontal_flip_image =  load_tk_image_from_bytes_array(flip_horizontal_bytes)
		self.vertical_flip_image = load_tk_image_from_bytes_array(flip_vertical_bytes)
		self.rotate_left_image = load_tk_image_from_bytes_array(rotate_left_bytes)
		self.rotate_right_image = load_tk_image_from_bytes_array(rotate_right_bytes)
		self.to_grayscale_image = load_tk_image_from_bytes_array(to_grayscale_bytes)
		self.selection_options_image = load_tk_image_from_bytes_array(selection_options_bytes)
		self.layers_symbol_image = load_tk_image_from_bytes_array(layers_symbol_bytes)
		self.folder_options_symbol = load_tk_image_from_bytes_array(folder_options_symbol_bytes)
		self.effects_wand_symbol = load_tk_image_from_bytes_array(effects_wand_symbol_bytes)

		self.drawtips_references = []
		self.project = PixelProject(self.width, self.height)

		panes = PanedWindow(self, orient = "horizontal", sashpad=3, sashrelief ="sunken")
		panes.pack(fill = "both", expand = True)
		panes.config(borderwidth = 0)

		self.left_side_frame = Frame(panes)
		self.left_side_frame.pack(fill = "both", expand = False, side = "left")
		panes.add(self.left_side_frame)

		tool_buttons = []
		self.gif_tool_bar = ToolBar(tool_buttons, self.left_side_frame)
		self.gif_tool_bar.pack(side = "top", fill = "x", pady = (0,2))

		save_options_button = Label(self.gif_tool_bar, image = self.floppy_image, font = "bold")
		save_options_button.pack(side = "left")
		save_menu = Menu(self, tearoff=0)
		save_menu.add_command(label="Export Gif", command=self.export_gif)
		save_menu.add_command(label="Export Selected Frame", command=self.export_selected_layer)
		save_menu.add_command(label="Export Selected Layer", command=self.export_selected_frame)
		# gif_menu.add_command(label="Export Project as Zip", command=self.export_zip)
		# gif_menu.add_command(label="Export Project as .lpixel", command=self.flip_selection_horizontal)
		# gif_menu.add_command(label="Load Folder as Layers in Current Frame", command=self.load_folder_as_layers)
		bind_popup("<Button-1>", save_options_button, save_menu)

		load_options_button = Label(self.gif_tool_bar, image = self.folder_options_symbol, font = "bold")
		load_options_button.pack(side = "left")
		load_options_menu = Menu(self, tearoff=0)
		load_options_menu.add_command(label="Import Gif as Frames", command=self.import_gif)
		load_options_menu.add_command(label="Load Folder as Frames", command=self.load_folder_as_frames)
		load_options_menu.add_command(label="Load Folder as Layers in Selected Frame", command=self.load_folder_as_layers)
		bind_popup("<Button-1>", load_options_button, load_options_menu)

		preview_options_button = Label(self.gif_tool_bar, image = self.magnifying_glass_image, font = "bold")
		preview_options_button.pack(side = "left")
		preview_options_menu = Menu(self, tearoff=0)
		preview_options_menu.add_command(label="Inspect Selected Frame", command=self.inspect_frame)
		preview_options_menu.add_command(label="Inspect Selected Layer", command=self.inspect_layer)
		bind_popup("<Button-1>", preview_options_button, preview_options_menu)

		panes2 = PanedWindow(self.left_side_frame, orient = "vertical", sashpad=3, sashrelief ="sunken")
		panes2.pack(fill = "both", expand = True, padx = 4, pady = (0,4))
		panes2.config(borderwidth = 0)

		
		self.gif_view = LayerViewer(self.project, self.width, self.height, panes2)
		self.gif_view.pack(fill = "both", expand = True)
		panes2.add(self.gif_view)
		
		self.frame_manager = LayerManager(self, self.project, panes2)
		self.frame_manager.pack(side = "left", fill = "both", expand = True, pady = 0)
		panes2.add(self.frame_manager)

		self.right_side_frame = Frame(panes)
		self.right_side_frame.pack(fill = "both", expand = True, side = "right")
		panes.add(self.right_side_frame)

		tool_buttons = [
			(self.vertical_flip_image, self.flip_vertical),
			(self.horizontal_flip_image, self.flip_horizontal),
			(self.rotate_left_image, self.rotate_left),
			(self.rotate_right_image, self.rotate_right),
		]

		self.tool_bar = ToolBar(tool_buttons, self.right_side_frame)
		self.tool_bar.pack(side = "top", fill = "x")


		layer_menu = Menu(self, tearoff = 0)
		layer_menu.add_command(label = "Rename Current Layer", command = self.rename_selected_layer)
		layer_menu.add_command(label = "Export Current Layer", command = self.save)
		layer_menu.add_command(label = "Export Current Layer as Bytes (Console)", command = self.export_selected_layer_as_bytes)
		layer_menu.add_command(label = "Delete Current Layer", command = self.delete_selected_layer)
		layer_menu.add_command(label = "Copy Current Layer", command = self.copy_selected_layer)
		layer_menu.add_command(label = "Promote Current Layer", command = self.promote_selected_layer)
		layer_menu.add_command(label = "Demote Current Layer", command = self.demote_selected_layer)
		layer_menu.add_command(label = "Merge Layer Down", command = self.merge_selected_layer_down)
		layer_menu.add_separator()
		layer_menu.add_command(label = "Rename Current Frame", command = self.rename_selected_frame)
		layer_menu.add_command(label = "Export Current Frame", command = self.save_selected_frame)
		layer_menu.add_command(label = "Export Current Frame as Bytes (Console)", command = self.export_selected_frame_as_bytes)
		layer_menu.add_command(label = "Delete Current Frame", command = self.delete_selected_frame)
		layer_menu.add_command(label = "Copy Current Frame", command = self.copy_selected_frame)
		layer_menu.add_command(label = "Promote Current Frame", command = self.promote_selected_frame)
		layer_menu.add_command(label = "Demote Current Frame", command = self.demote_selected_frame)
		layer_menu.add_command(label = "New Layer in Current Frame", command = self.new_layer_in_selected_frame)
		layer_menu.add_command(label = "New Layer from Image in Current Frame", command = self.new_layer_from_image_in_selected_frame)
		
		self.layer_options_menu_button = Label(self.tool_bar, image = self.layers_symbol_image, font = "bold")
		self.layer_options_menu_button.pack(side = "left")
		bind_popup("<Button-1>", self.layer_options_menu_button, layer_menu)

		# self.separator = Frame(self.tool_bar, background = "black")
		# self.separator.pack(side = "left", fill = "y", expand = False, pady = 2, padx = 4)

		# create a popup menu
		selection_menu = Menu(self, tearoff=0)
		selection_menu.add_command(label = "Flood Fill Selection", command = self.fill_selection)
		selection_menu.add_command(label = "Flip Selection Vertical", command = self.flip_selection_vertical)
		selection_menu.add_command(label = "Flip Selection Horizontal", command = self.flip_selection_horizontal)
		selection_menu.add_command(label = "Rotate Selection Right", command = self.rotate_selection_right)
		selection_menu.add_command(label = "Rotate Selection Left", command = self.rotate_seletion_left)
		selection_menu.add_command(label = "Export Selection", command = self.export_selection)
		selection_menu.add_command(label = "Export Selection as Bytes (Console)", command = self.export_selection_as_bytes)
		selection_menu.add_separator()
		selection_menu.add_command(label = "Copy Selection to Clipboard", command = self.copy_selection_to_clipboard)
		selection_menu.add_command(label = "New Layer from Selection", command = self.new_layer_image_from_selection)
		selection_menu.add_separator()
		selection_menu.add_command(label = "Apply Blur Filter to Selection", command = self.effect_blur_selection)
		selection_menu.add_command(label = "Apply Contour Filter to Selection", command = self.effect_contour_selection)
		selection_menu.add_command(label = "Apply Detail Filter to Selection", command = self.effect_detail_selection)
		selection_menu.add_command(label = "Apply Edge Enhance Filter to Selection", command = self.effect_edge_enhance_selection)
		selection_menu.add_command(label = "Apply Edge Enhance More Filter to Selection", command = self.effect_edge_enhance_more_selection)
		selection_menu.add_command(label = "Apply Emboss Filter to Selection", command = self.effect_emboss_selection)
		selection_menu.add_command(label = "Apply Find Edges Filter to Selection", command = self.effect_find_edges_selection)
		selection_menu.add_command(label = "Apply Sharpen Filter to Selection", command = self.effect_sharpen_selection)
		selection_menu.add_command(label = "Apply Smooth Filter to Selection", command = self.effect_smooth_selection)
		selection_menu.add_command(label = "Apply Smooth More Filter to Selection", command = self.effect_smooth_more_selection)
		selection_menu.add_command(label = "Apply Gaussian Filter to Selection", command = self.effect_gaussian_selection)
		selection_menu.add_command(label = "Apply Box Blur Filter to Selection", command = self.effect_box_blur_selection)
		selection_menu.add_command(label = "Apply Median Filter to Selection", command = self.effect_median_filter_selection)
		selection_menu.add_command(label = "Apply Min Filter to Selection", command = self.effect_min_filter_selection)
		selection_menu.add_command(label = "Apply Max Filter to Selection", command = self.effect_max_filter_selection)
		selection_menu.add_command(label = "Apply Mode Filter to Selection", command = self.effect_mode_filter_selection)


		self.selections_options_menu_button = Label(self.tool_bar, image = self.selection_options_image, font = "bold")
		self.selections_options_menu_button.pack(side = "left")
		bind_popup("<Button-1>", self.selections_options_menu_button, selection_menu)


		# create a popup menu
		effects_menu = Menu(self, tearoff=0)
		effects_menu.add_command(label = "Apply Blur Filter", command = self.effect_blur_layer)
		effects_menu.add_command(label = "Apply Contour Filter", command = self.effect_contour_layer)
		effects_menu.add_command(label = "Apply Detail Filter", command = self.effect_detail_layer)
		effects_menu.add_command(label = "Apply Edge Enhance Filter", command = self.effect_edge_enhance_layer)
		effects_menu.add_command(label = "Apply Edge Enhance More Filter", command = self.effect_edge_enhance_more_layer)
		effects_menu.add_command(label = "Apply Emboss Filter", command = self.effect_emboss_layer)
		effects_menu.add_command(label = "Apply Find Edges Filter", command = self.effect_find_edges_layer)
		effects_menu.add_command(label = "Apply Sharpen Filter", command = self.effect_sharpen_layer)
		effects_menu.add_command(label = "Apply Smooth Filter", command = self.effect_smooth_layer)
		effects_menu.add_command(label = "Apply Smooth More Filter", command = self.effect_smooth_more_layer)
		effects_menu.add_command(label = "Apply Gaussian Filter", command = self.effect_gaussian_layer)
		effects_menu.add_command(label = "Apply Box Blur Filter", command = self.effect_box_blur_layer)
		effects_menu.add_command(label = "Apply Median Filter", command = self.effect_median_filter_layer)
		effects_menu.add_command(label = "Apply Min Filter", command = self.effect_min_filter_layer)
		effects_menu.add_command(label = "Apply Max Filter", command = self.effect_max_filter_layer)
		effects_menu.add_command(label = "Apply Mode Filter", command = self.effect_mode_filter_layer)

		self.effects_options_menu_button = Label(self.tool_bar, image = self.effects_wand_symbol, font = "bold")
		self.effects_options_menu_button.pack(side = "left")
		bind_popup("<Button-1>", self.effects_options_menu_button, effects_menu)

		self.canvas_frame = ttk.LabelFrame(self.right_side_frame, text = "")
		self.canvas_frame.pack(fill = "both", expand = True, anchor = "n", padx = 3)
		inner_frame = Frame(self.canvas_frame)
		inner_frame.pack(fill = "both", expand = True, side = "top", anchor = "n", padx = 4, pady = 4)
		self.canvas = LyfeCanvas(self.project, inner_frame)
		force_aspect(self.canvas, inner_frame, float(self.width)/float(self.height))

		self.footer = Frame(self.right_side_frame)
		self.footer.pack(side = "bottom", fill = "x", expand = False, padx = 3)
		self.footer_var = StringVar()
		self.footer_label = Label(self.footer, textvariable = self.footer_var)
		self.footer_label.pack(side = "left", expand = False, fill = "x")

		self.grip = ttk.Sizegrip(self)
		self.grip.place(relx=1.0, rely=1.0, anchor="se")
		self.grip.bind("<ButtonPress-1>", self.on_press)
		self.grip.bind("<B1-Motion>", self.on_resize)
		self.grip.bind("<ButtonRelease-1>", self.on_release)

		self.canvas.bind_right(self.erase)
		self.canvas.bind_middle(self.eyedrop)
		self.canvas.bind_right_drag(self.erase)
		self.canvas.after_idle(self.refresh)
		self.canvas.bind_movement(self.on_mouse_move)

		self.canvas.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
		self.canvas.canvas.bind("<B1-Motion>", self.on_canvas_drag)
		self.canvas.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

	def load_folder_as_frames(self):
		path = filedialog.askdirectory()
		if path:
			entries = os.scandir(path)
			files = [e for e in entries if e.is_file()]
			for f in files: self.project.new_frame_from_image(Image.open(f.path))
			self.refresh()

	def import_gif(self):
		path = filedialog.askopenfilename()
		self.load_gif(path)
	def load_gif(self, path):
		self.project.import_gif(path)
		self.refresh()
	def load_gif_fresh(self, path):
		self.project.del_frame(self.project.selected_frame)
		self.project.import_gif(path)
		self.refresh()

	def load_folder_as_layers(self): print("Load folder as layers not implemented")
	def export_zip(self): print("Export zip not implemented")
	def export_project(self): print("Export project not implemented")
	def export_gif(self):
		gif_images = self.project.export_gif_frames()
		SaveMenu(self.controller, gif_images, gif = True)

	def export_selected_layer(self):
		image = self.project.selected_frame.selected_layer.export_image()
		SaveMenu(self.controller, image)

	def export_selected_layer_as_bytes(self):
		image = self.project.selected_frame.selected_layer.export_image()
		print(convert_tk_image_to_bytes_array(image))

	def export_selected_frame(self):
		image = self.project.selected_frame.export_composite_image()
		SaveMenu(self.controller, image)

	def export_selected_frame_as_bytes(self):
		image = self.project.selected_frame.export_composite_image()
		print(convert_tk_image_to_bytes_array(image))

	def refresh(self):
		self.canvas.redraw()
		self.frame_manager.refresh()
		self.canvas_frame.configure(text = f"{self.project.selected_frame.id} - {self.project.selected_frame.selected_layer.id}")
		self.controller.ClipboardWindow.refresh()

	def draw_canvas_draw_path(self, x1, y1, x2, y2):
		for r in self.drawtips_references: self.canvas.canvas.delete(r)
		if ToolController.tool in [TOOLCONST.LINE, TOOLCONST.MOVE_SELECTION]: return self.canvas.canvas.create_line(x1, y1, x2, y2, fill = "#000000", width = 2)
		elif ToolController.tool in [TOOLCONST.RECTANGLE, TOOLCONST.SELECT_BOX, TOOLCONST.FILLED_RECTANGLE]: return self.canvas.canvas.create_rectangle(x1, y1, x2, y2, fill = "", width = 2)
		elif ToolController.tool in [TOOLCONST.ELLIPSE, TOOLCONST.FILLED_ELLIPSE]: return self.canvas.canvas.create_oval(x1, y1, x2, y2, fill = "", width = 2)

	def on_canvas_click(self, event):
		x, y = event.x, event.y
		id = self.canvas.get_cell_id(x,y)
		if id:
			if ToolController.handle_start(self.project.selected_frame.selected_layer, id): self.refresh()
			if ToolController.drag:
				x1, y1 = (int(v) for v in ToolController.start_id.split("x"))
				x2, y2 = x1, y1
				self.drawtips_references.append(self.draw_canvas_draw_path(x1, y1, x2, y2))

	def on_canvas_drag(self, event):
		id = self.canvas.get_cell_id(event.x, event.y)
		if id:
			if ToolController.handle_drag(self.project.selected_frame.selected_layer, id):
				self.refresh()
			if ToolController.drag:
				x1, y1 = (int(v) for v in ToolController.start_id.split("x"))
				x2, y2 = (int(v) for v in id.split("x"))
				cords = (x1, y1, x2, y2)
				x1, y1, x2, y2 = ((self.canvas.pixel_width * x + 0.5 * self.canvas.pixel_width) for x in cords)
				self.drawtips_references.append(self.draw_canvas_draw_path(x1, y1, x2, y2))

	def on_canvas_release(self, event):
		x, y = event.x, event.y
		id = self.canvas.get_cell_id(x,y)
		if id:
			if ToolController.handle_end(self.project.selected_frame.selected_layer, id):
				self.refresh()
			if ToolController.drag:
				for r in self.drawtips_references:
					self.canvas.canvas.delete(r)

	def erase(self, event):
		id = self.canvas.get_cell_id(event.x, event.y)
		if id:
			ToolController.handle_erase(self.project.selected_frame.selected_layer, id)
			self.refresh()

	def eyedrop(self, event):
		id = self.canvas.get_cell_id(event.x, event.y)
		color = self.project.selected_frame.selected_layer.get_pixel_color(id)
		self.controller.PalletWindow.set_color(color)

	def on_press(self, event):
		self.grip["cursor"] = "bottom_right_corner"

	def on_mouse_move(self, event):
		x = event.x
		y = event.y
		id = self.canvas.get_cell_id(x,y)
		if id:
			color = self.project.selected_frame.selected_layer.get_pixel_color(id)
			rgba = f"R: {color[0]}, G: {color[1]}, B: {color[2]}, A: {color[3]}"
			self.footer_var.set(f"{id}  |  {rgba}")

	def on_resize(self, event):
		x_change = event.x_root - self.winfo_rootx()
		x_change = 1 if x_change < 1 else x_change
		y_change = event.y_root - self.winfo_rooty()
		y_change = 1 if y_change < 1 else y_change
		self.geometry("%sx%s" % (x_change, y_change))
		self.refresh()

	def on_release(self, event):
		self.grip["cursor"] = "arrow"
		self.refresh()

	def save(self):
		SaveMenu(self.controller, self.project.selected_frame.selected_layer.export_image())

	def new_layer_from_image(self, event = None):
		path = filedialog.askopenfilename()
		if path:
			image = Image.open(path).convert("RGBA")
			layer = self.project.selected_frame.new_layer_from_image(image)
		self.refresh()

	def new_layer(self, event = None):
		layer = self.project.selected_frame.new_layer()
		self.project.selected_frame.selected_layer = layer
		self.refresh()
	def load_image(self, tkimage):
		l = self.project.selected_frame.new_layer()
		l.load_image(tkimage)
		self.refresh()
	def load_blank(self):
		self.project.select_frame(0)
		self.project.selected_frame.select_layer(0)
		self.refresh()
	def flip_vertical(self):
		self.canvas.flip_vertical()
		self.refresh()
	def flip_horizontal(self):
		self.canvas.flip_horizontal()
		self.refresh()
	def rotate_left(self):
		self.canvas.rotate_left()
		self.refresh()
	def rotate_right(self):
		self.canvas.rotate_right()
		self.refresh()
	def to_grayscale(self):
		self.canvas.to_grayscale()
		self.refresh()

	def effect_blur_layer(self):
		ToolController.effect_blur_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_contour_layer(self):
		ToolController.effect_contour_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_detail_layer(self):
		ToolController.effect_detail_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_edge_enhance_layer(self):
		ToolController.effect_edge_enhance_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_edge_enhance_more_layer(self):
		ToolController.effect_edge_enhance_more_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_emboss_layer(self):
		ToolController.effect_emboss_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_find_edges_layer(self):
		ToolController.effect_find_edges_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_sharpen_layer(self):
		ToolController.effect_sharpen_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_smooth_layer(self):
		ToolController.effect_smooth_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_smooth_more_layer(self):
		ToolController.effect_smooth_more_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_gaussian_layer(self):
		radius = simpledialog.askinteger("Gaussian Blur Filter", "Filter Radius:", parent=self)
		ToolController.effect_gaussian_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_box_blur_layer(self):
		radius = simpledialog.askinteger("Box Blur Filter", "Filter Radius:", parent=self)
		ToolController.effect_box_blur_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_median_filter_layer(self):
		size = simpledialog.askinteger("Median Blur Filter", "Filter Size:", parent=self)
		ToolController.effect_median_filter_layer(self.project.selected_frame.selected_layer, size)
		self.refresh()
	def effect_min_filter_layer(self):
		size = simpledialog.askinteger("Min Blur Filter", "Filter Size:", parent=self)
		ToolController.effect_min_filter_layer(self.project.selected_frame.selected_layer, size)
		self.refresh()
	def effect_max_filter_layer(self):
		size = simpledialog.askinteger("Max Blur Filter", "Filter Size:", parent=self)
		ToolController.effect_max_filter_layer(self.project.selected_frame.selected_layer, size)
		self.refresh()
	def effect_mode_filter_layer(self):
		size = simpledialog.askinteger("Mode Blur Filter", "Filter Size:", parent=self)
		ToolController.effect_mode_filter_layer(self.project.selected_frame.selected_layer, size)
		self.refresh()

	def effect_blur_selection(self):
		ToolController.effect_blur_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_contour_selection(self):
		ToolController.effect_contour_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_detail_selection(self):
		ToolController.effect_detail_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_edge_enhance_selection(self):
		ToolController.effect_edge_enhance_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_edge_enhance_more_selection(self):
		ToolController.effect_edge_enhance_more_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_emboss_selection(self):
		ToolController.effect_emboss_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_find_edges_selection(self):
		ToolController.effect_find_edges_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_sharpen_selection(self):
		ToolController.effect_sharpen_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_smooth_selection(self):
		ToolController.effect_smooth_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_smooth_more_selection(self):
		ToolController.effect_smooth_more_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_gaussian_selection(self):
		radius = simpledialog.askinteger("Gaussian Blur Filter", "Filter Radius:", parent=self)
		ToolController.effect_gaussian_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_box_blur_selection(self):
		radius = simpledialog.askinteger("Box Blur Filter", "Filter Radius:", parent=self)
		ToolController.effect_box_blur_selection(self.project.selected_frame.selected_layer)
		self.refresh()
	def effect_median_filter_selection(self):
		size = simpledialog.askinteger("Median Blur Filter", "Filter Size:", parent=self)
		ToolController.effect_median_filter_selection(self.project.selected_frame.selected_layer, size)
		self.refresh()
	def effect_min_filter_selection(self):
		size = simpledialog.askinteger("Min Blur Filter", "Filter Size:", parent=self)
		ToolController.effect_min_filter_selection(self.project.selected_frame.selected_layer, size)
		self.refresh()
	def effect_max_filter_selection(self):
		size = simpledialog.askinteger("Max Blur Filter", "Filter Size:", parent=self)
		ToolController.effect_max_filter_selection(self.project.selected_frame.selected_layer, size)
		self.refresh()
	def effect_mode_filter_selection(self):
		size = simpledialog.askinteger("Mode Blur Filter", "Filter Size:", parent=self)
		ToolController.effect_mode_filter_selection(self.project.selected_frame.selected_layer, size)
		self.refresh()



	def fill_selection(self):
		layer = self.project.selected_frame.selected_layer
		if layer.start_selection and layer.end_selection:
			ToolController.fill_selection(layer, layer.start_selection, layer.end_selection)
			self.refresh()
	def flip_selection_vertical(self):
		layer = self.project.selected_frame.selected_layer
		if layer.start_selection and layer.end_selection:
			ToolController.flip_selection_vertical(layer, layer.start_selection, layer.end_selection)
			self.refresh()
	def flip_selection_horizontal(self):
		layer = self.project.selected_frame.selected_layer
		if layer.start_selection and layer.end_selection:
			ToolController.flip_selection_horizontal(layer, layer.start_selection, layer.end_selection)
			self.refresh()
	def rotate_selection_right(self):
		layer = self.project.selected_frame.selected_layer
		if layer.start_selection and layer.end_selection:
			ToolController.rotate_selection_right(layer, layer.start_selection, layer.end_selection)
			self.refresh()
	def rotate_seletion_left(self):
		layer = self.project.selected_frame.selected_layer
		if layer.start_selection and layer.end_selection:
			ToolController.rotate_selection_left(layer, layer.start_selection, layer.end_selection)
			self.refresh()
	def export_selection(self):
		layer = self.project.selected_frame.selected_layer
		if layer.start_selection and layer.end_selection:
			image = ToolController.export_selection(layer, layer.start_selection, layer.end_selection)
			SaveMenu(self.controller, image)
			self.refresh()
	def export_selection_as_bytes(self):
		layer = self.project.selected_frame.selected_layer
		if layer.start_selection and layer.end_selection:
			image = ToolController.export_selection(layer, layer.start_selection, layer.end_selection)
			print(convert_tk_image_to_bytes_array(image))
	def copy_selection_to_clipboard(self):
		layer = self.project.selected_frame.selected_layer
		if layer.start_selection and layer.end_selection:
			image = ToolController.copy_selection_to_clipboard(layer)
			self.refresh()

	def inspect_layer(self): ImageViewer(self.controller, self.project.selected_frame.selected_layer.export_image())
	def inspect_frame(self): ImageViewer(self.controller, self.project.selected_frame.export_composite_image())

	def new_layer_in_selected_frame(self): self.new_layer()
	def new_layer_from_image_in_selected_frame(self):
		path = filedialog.askopenfilename()
		if path:
			image = Image.open(path)
			layer = self.project.selected_frame.new_layer_from_image(image)
			self.refresh()
	def ask_delete_layer(self, frame, layer):
		if len(frame.layers) == 1:
			messagebox.showwarning("Warning", "Cannot delete last layer.")
			return
		return messagebox.askyesno("Delete Layer?", f"Are you sure you wish to delete this layer?\n{layer.id}")
	def delete_selected_layer(self):
		frame = self.project.selected_frame
		layer = self.project.selected_frame.selected_layer
		if self.ask_delete_layer(frame, layer):
			frame.del_layer(layer)
			frame.selected_layer = frame.layers[0]
		self.refresh()
	def copy_selected_layer(self):
		self.project.selected_frame.copy_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def promote_selected_layer(self):
		self.project.selected_frame.promote_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def demote_selected_layer(self):
		self.project.selected_frame.demote_layer(self.project.selected_frame.selected_layer)
		self.refresh()
	def merge_selected_layer_down(self):
		self.project.selected_frame.merge_layer_down(self.project.selected_frame.selected_layer)
		self.refresh()
	def rename_selected_frame(self):
		frame = self.project.selected_frame
		name = simpledialog.askstring("Rename Frame", f"What would you like to rename Frame: {frame.id} to?")
		if name:
			frame.set_id(name)
			self.refresh()
	def rename_selected_layer(self):
		layer = self.project.selected_frame.selected_layer
		name = simpledialog.askstring("Rename Layer", f"What would you like to rename Layer: {layer.id} to?")
		if name:
			layer.set_id(name)
			self.refresh()
	def save_selected_frame(self):
		image = self.project.selected_frame.export_composite_image()
		SaveMenu(self.controller, image)
	def ask_delete_frame(self):
		if len(self.project.frames) == 1:
			return messagebox.showwarning("Warning", "Cannot delete last frame.")
		return messagebox.askyesno("Delete", "Are you sure you wish to delete this frame?\nThis cannot be undone.")
	def delete_selected_frame(self):
		if self.ask_delete_frame():
			self.project.del_frame(self.project.selected_frame)
			self.project.selected_frame = self.project.frames[0]
			self.refresh()
	def copy_selected_frame(self):
		self.project.copy_frame(self.project.selected_frame)
		self.refresh()
	def promote_selected_frame(self):
		self.project.promote_frame(self.project.selected_frame)
		self.refresh()
	def demote_selected_frame(self):
		self.project.demote_frame(self.project.selected_frame)
		self.refresh()

	def new_layer_image_from_selection(self):
		if not self.project.selected_frame.selected_layer.selection: return
		image = ToolController.new_layer_image_from_selection(self.project.selected_frame.selected_layer, ToolController.start_selection, ToolController.end_selection)
		self.project.selected_frame.new_layer_from_image(image)
		self.refresh()

	def exit(self):
		if messagebox.askyesno("Exit?", f"Are you sure you wish to exit?\nAll unsaved work will be lost."):
			self.destroy()
