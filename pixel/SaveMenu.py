from tkinter import IntVar, StringVar, Frame, Text, Toplevel, Label, Button, Radiobutton, filedialog, ttk
from PIL import Image, ImageTk
from .BaseWindow import BaseWindow
from .TopBar import TopBar
from .canvas import PixelCanvas
from .colormath import get_gradient, get_rainbow
from .ImageViewer import ImageViewer
from .LabeledEntry import LabeledEntry
from .file_management import convert_image_to_grayscale, convert_image_to_blackandwhite

WIDTH = 300
HEIGHT = 400

#Constants, need to move to enum 
# #Color options constants
BLACKANDWHITE = 0
GRAYSCALE = 1
RGB = 2
COLOR_OPTIONS = {
	BLACKANDWHITE : "Black and White",
	GRAYSCALE : "Grayscale",
	RGB : "RGB"
}


# # Sizing options constants
SCALAR = 0
PIXELS = 1
SIZING_OPTIONS = {
	SCALAR : "Scale output",
	PIXELS : "Custom"
}

# # Sizing options constants
LOOP = 0
NO_LOOP = 1
LOOP_OPTIONS = {
	LOOP : "Loop Gif",
	NO_LOOP : "Don't Loop Gif"
}


#selection list is a list of tuples in form ("buttonstring", value)
#selection_list = [("Text1", VALUE1), ("Text2", VALUE2), ...]

class selection_box(ttk.LabelFrame):
	def __init__(self, label_text, selection_list, command, *args, **kwargs):
		ttk.LabelFrame.__init__(self, *args, **kwargs)
		self.inner_frame = Frame(self)
		self.inner_frame.pack(fill = "both", expand = True, side = "left")
		self.configure(text = label_text)
		self.var = IntVar()
		for text, value in selection_list:
			b = Radiobutton(self.inner_frame, text = text, variable = self.var, value = value, command = command)
			b.pack(anchor = "w", fill = "y", expand = False)
		#select first button
		for s in selection_list: self.var.set(s[1]); break

	def get(self):
		return self.var.get()

class SaveMenu(BaseWindow):
	def __init__(self, controller, image_data, gif = False):
		BaseWindow.__init__(self, controller)
		self.geometry(f"{WIDTH}x{HEIGHT}")
		self.set_exit_function()
		self.set_title("Export")
		self.resizable(True, True)
		self.image_data = image_data
		self.gif = gif

		# sizing_options = [(SIZING_OPTIONS[SCALAR], SCALAR), (SIZING_OPTIONS[PIXELS], PIXELS)]
		# self.size_selection = selection_box("SIZING", sizing_options, self)
		# self.size_selection.pack(fill = "x", expand = False, padx = 4, anchor = "n")

		# color_and_format_frame = Frame(self)
		# color_options = [(COLOR_OPTIONS[RGB], RGB), (COLOR_OPTIONS[GRAYSCALE], GRAYSCALE), (COLOR_OPTIONS[BLACKANDWHITE], BLACKANDWHITE)]
		# self.color_selection = selection_box("COLOR", color_options, color_and_format_frame)
		# self.color_selection.pack(fill = "both", expand = True, side = "left", padx = 4, )
		# format_options = [
		# 	(OUTPUT_OPTIONS[PNG], PNG),
		# 	(OUTPUT_OPTIONS[JPG], JPG),
		# 	(OUTPUT_OPTIONS[BMP], BMP),
		# 	(OUTPUT_OPTIONS[PXSTUDIO], PXSTUDIO)
		# 	]
		# self.format_selection = selection_box("FORMAT", format_options, color_and_format_frame)
		# self.format_selection.pack(fill = "both", expand = True, side = "left", padx = 4)
		# color_and_format_frame.pack(side = "top", expand = False, fill = "x")
		self.outer_frame = Frame(self)
		self.outer_frame.pack(fill = "both", expand = True)
		sizing_and_color_frame = Frame(self.outer_frame)
		sizing_and_color_frame.pack(expand = True, fill = "both")
		sizing_options = [(SIZING_OPTIONS[SCALAR], SCALAR), (SIZING_OPTIONS[PIXELS], PIXELS)]
	
		#-------------------------------------------------
		#Size

		size_selection_and_size_option_frame = Frame(sizing_and_color_frame)
		size_selection_and_size_option_frame.pack(fill = "both", expand = True, padx = 4)
		self.size_selection = selection_box("SIZING", sizing_options, self.on_size_select, size_selection_and_size_option_frame)
		self.size_selection.pack(side = "left", fill = "y")

		selection_frame_frame = ttk.LabelFrame(size_selection_and_size_option_frame, text = "SIZE OPTIONS")
		selection_frame_frame.pack(fill = "both", expand = True, side = "left")
		self.scaling_frame = Frame(selection_frame_frame)
		self.scaling_frame.place(relwidth = 1, relheight = 1)
		self.scaling_factor = LabeledEntry("Scaling Factor - ", 1, self.scaling_frame)
		self.scaling_factor.place(relwidth = 1, relheight = 1)

		self.custom_dimensions_frame = Frame(selection_frame_frame)
		self.custom_dimensions_frame.place(relwidth = 1, relheight = 1)
		self.dimension_x_entry = LabeledEntry("Width - ", "16", self.custom_dimensions_frame)
		self.dimension_x_entry.pack(fill = "both", expand = True, anchor = "w")
		self.dimension_y_entry = LabeledEntry("Height - ", "16", self.custom_dimensions_frame)
		self.dimension_y_entry.pack(fill = "both", expand = True, anchor = "w")
		self.on_size_select()

		#Loop--------------------------------------------
		if self.gif:
			gif_option_frame = Frame(sizing_and_color_frame)
			gif_option_frame.pack(fill = "both", expand = True, padx = 4)
			loop_options = [(LOOP_OPTIONS[LOOP], LOOP), (LOOP_OPTIONS[NO_LOOP], NO_LOOP)]
			self.loop_selection = selection_box("LOOP OPTIONS", loop_options, self.on_loop_select, gif_option_frame)
			self.loop_selection.pack(side = "left", fill = "y")

			loop_frame = ttk.LabelFrame(gif_option_frame, text = "LOOP OPTIONS")
			loop_frame.pack(fill = "both", expand = True, side = "left")
			self.number_of_loops_frame = Frame(loop_frame)
			self.number_of_loops_frame.place(relwidth = 1, relheight = 1)
			self.number_of_loops = LabeledEntry("Loops, blank for limitless -", "", self.number_of_loops_frame)
			self.number_of_loops.place(relwidth = 1, relheight = 1)

			self.no_loop_frame = Frame(loop_frame)
			self.no_loop_frame.place(relwidth = 1, relheight = 1)
			Label(self.no_loop_frame, text = "Don't loop gif.").place(relwidth = 1, relheight = 1)

			self.on_loop_select()

		#Color--------------------------------------------

		color_options = [(COLOR_OPTIONS[RGB], RGB), (COLOR_OPTIONS[GRAYSCALE], GRAYSCALE), (COLOR_OPTIONS[BLACKANDWHITE], BLACKANDWHITE)]
		self.color_selection = selection_box("COLOR", color_options, self.on_color_select, sizing_and_color_frame)
		self.color_selection.pack(fill = "both", expand = True, side = "top", padx = 4, )

		if self.gif:
			duration_frame = ttk.LabelFrame(sizing_and_color_frame, text = "GIF PLAYBACK")
			duration_frame.pack(side = "top", expand = True, fill = "x", padx = 2)
			self.duration_entry = LabeledEntry("Frame Duration (Divide 1000 by fps) - ", 100, duration_frame)
			self.duration_entry.pack(side = "top", expand = True, fill = "both", padx = 2)

		footer = ttk.LabelFrame(self.outer_frame, text = "FILE")

		select_path_frame = Frame(footer)
		select_path_frame.pack(fill = "both", expand = True)
		self.file_path_entry = LabeledEntry("File path", "", select_path_frame)
		self.file_path_entry.pack(fill = "both", expand = True, side = "left", padx = (2, 2))
		select_path_button = Button(select_path_frame, command = self.set_save_path, text = "Select file").pack(side = "right", pady = (4,6), padx = (2, 2), expand = False)

		Button(footer, text = "Save", command = self.save if not self.gif else self.save_gif).pack(fill = "x", expand = False, padx = 4, pady = 4)

		footer.pack(fill = "x", expand = False, padx = 4, side = "top", pady = 4)

		grip = ttk.Sizegrip(self)
		grip.place(relx=1.0, rely=1.0, anchor="se")

	def set_save_path(self):
		if self.gif:
			save_as = filedialog.asksaveasfilename(
				defaultextension = ".*",
				filetypes = [("GIF files", ".gif")]
			)
		else:
			save_as = filedialog.asksaveasfilename(
				defaultextension = ".*",
				filetypes = [
						("All files", ".*"), 
						("PNG files", ".png"), 
						("JPEG files", ".jpg .jpeg"), 
						("BMP files", ".bmp"), 
						("ICO files", ".ico")
				]
			)
		self.file_path_entry.set(save_as)

	def on_size_select(self):
		sizing_mode = self.size_selection.get()
		def handle_scalar():self.scaling_frame.tkraise()
		def handle_pixels():self.custom_dimensions_frame.tkraise()
		modes = {SCALAR : handle_scalar,PIXELS : handle_pixels}
		modes[sizing_mode]()

	def on_loop_select(self):
		loop_mode = self.loop_selection.get()
		def handle_loop(): self.number_of_loops_frame.tkraise()
		def handle_no_loop(): self.no_loop_frame.tkraise()
		modes = { LOOP : handle_loop, NO_LOOP : handle_no_loop }
		modes[loop_mode]()

	def on_color_select(self):
		pass

	def save(self):
		print("Beginning image conversion")
		image_data = self.image_data #Make a copy of the image data for manipulation in case save fails and needs to bre redone
		def handle_scalar(image):
			print("Appling scalar resize to image")
			try:
				factor = int(self.scaling_factor.get())
				print(f"Resizing image by factor {factor}")
			except Exception as e:
				self.error(f"Invalid scaling factor: {e}")
				return
			if not factor:
				self.error(f"Scaling factor cannot be zero")
				return

			if factor == 1:
				return image
			else:
				return image.resize((int(image.height) * int(factor), int(image.width) * int(factor)), Image.BOX)

		def handle_pixels(image): 
			try:
				width = self.dimension_x_entry.get()
				height = self.dimension_y_entry.get()
				print(f"Resizing image to {width} x {height}")
			except Exception as e:
				self.error(f"Invalid pixel resize values {e}")
				return

			try:
				return image.resize((int(height), int(width)), Image.BOX)
			except Exception as e:
				self.error(f"Error resizing image - {e}")
				return
			
		def handle_RGB(image):
			print(f"ALREADY RGB")
			return image

		sizing_options = {
			SCALAR : handle_scalar,
			PIXELS : handle_pixels
		}
		sizing_mode = self.size_selection.get()
		image_data = sizing_options[sizing_mode](image_data)
		if not image_data: return

		color_options = {
			RGB : handle_RGB,
			GRAYSCALE : convert_image_to_grayscale,
			BLACKANDWHITE : convert_image_to_blackandwhite
		}
		color_mode = self.color_selection.get()
		try:
			mode = color_options[color_mode]
			if not mode:
				self.error("Unable to determine color mode")
				return
		except Exception as e:
			self.error(f"Error determining color mode: {e}")
			return
		try:
			image_data = mode(image_data)
			if not image_data:
				self.error("Invalid data after applying color mode")
				return
		except Exception as e:
			self.error(f"Error applying color mode: {e}")
			return

		try:
			filename = self.file_path_entry.get()
		except Exception as e:
			self.error(f"Error getting file name: {e}")
			return
		if not filename:
			self.error(f"No filename specified")
			return

		try:
			print("Saving...")
			image_data.save(filename)
		except Exception as e:
			self.error(f"Error saving image: {e}")
			return

		self.destroy() #Sucessful!

	def save_gif(self):
		print("Beginning image conversion")
		def handle_scalar(image):
			print("Appling scalar resize to image")
			try:
				factor = int(self.scaling_factor.get())
				print(f"Resizing image by factor {factor}")
			except Exception as e:
				self.error(f"Invalid scaling factor: {e}")
				return
			if not factor:
				self.error(f"Scaling factor cannot be zero")
				return

			if factor == 1:
				return image
			else:
				return image.resize((int(image.height) * int(factor), int(image.width) * int(factor)), Image.BOX)

		def handle_pixels(image): 
			try:
				width = self.dimension_x_entry.get()
				height = self.dimension_y_entry.get()
				print(f"Resizing image to {width} x {height}")
			except Exception as e:
				self.error(f"Invalid pixel resize values {e}")
				return

			try:
				return image.resize((int(height), int(width)), Image.BOX)
			except Exception as e:
				self.error(f"Error resizing image - {e}")
				return
			
		def handle_RGB(image):
			print(f"ALREADY RGB")
			return image

		sizing_options = {
			SCALAR : handle_scalar,
			PIXELS : handle_pixels
		}
		sizing_mode = self.size_selection.get()

		images = []
		
		try:
			for i in self.image_data: images.append(sizing_options[sizing_mode](i))
		except Exception as e:
			self.error(f"Error resizing images: {e}")
			return
		for i in images:
			if not i:
				self.error(f"Invalid image data after applying resize")
				return

		color_options = {
			RGB : handle_RGB,
			GRAYSCALE : convert_image_to_grayscale,
			BLACKANDWHITE : convert_image_to_blackandwhite
		}
		color_mode = self.color_selection.get()
		try:
			mode = color_options[color_mode]
			if not mode:
				self.error("Unable to determine color mode")
				return
		except Exception as e:
			self.error(f"Error determining color mode: {e}")
			return
		try:
			images = [mode(i) for i in images]
			for i in images:
				if not i:
					self.error("Invalid data after applying color mode")
					return
		except Exception as e:
			self.error(f"Error applying color mode: {e}")
			return

		try:
			filename = self.file_path_entry.get()
		except Exception as e:
			self.error(f"Error getting file name: {e}")
			return
		if not filename:
			self.error(f"No filename specified")
			return

		duration = 100

		def handle_loop():
			print(":handleloop")
			if self.number_of_loops.get(): return int(self.number_of_loops.get())
			else: return 0
		def handle_no_loop(): return 1

		loop_options = {
			LOOP : handle_loop,
			NO_LOOP : handle_no_loop,
		}

		loop = loop_options[self.loop_selection.get()]()
		duration = int(self.duration_entry.get())
		print(loop, duration)
		try:
			print("Saving...")
			images[0].save(filename, save_all=True, append_images=images[1:], optimize=False, duration=int(duration), loop=int(loop))
		except Exception as e:
			self.error(f"Error saving image: {e}")
			return

		self.destroy() #Sucessful!


	def error(self, error):
		error_frame = error_window(error, self.outer_frame)
		error_frame.place(relwidth = 1, relheight = 1)


class error_window(Frame):
	def __init__(self, error, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
		self.error = Text(self, wrap = "word")
		self.error.insert("end", error)
		self.error.configure(state = "disable")
		self.error.place(relwidth = 1, x = +4, width = -8, height = - 33, relheight = 1)
		self.exit_button = Button(self, command = self.exit, text = "Accept")
		self.exit_button.place(relwidth = 1, x = +4, width = -8, rely = 1, y = - 29, height = 25)

	def exit(self):
		self.destroy()
