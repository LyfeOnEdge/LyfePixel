from PIL import Image, ImageTk
from numpy import asarray
import io, os

#Converts a png encoded in bytes to an image tkinter can process
def load_tk_image_object_from_bytes_array(bytes_array):
	return Image.open(io.BytesIO(bytes_array))
def load_tk_image_from_bytes_array(bytes_array):
	return ImageTk.PhotoImage(load_tk_image_object_from_bytes_array(bytes_array))


#Not Used. Function to create byte-encoded images for use with tkinter
def convert_tk_image_to_bytes_array(image):
	bytes_array = io.BytesIO()
	image.save(bytes_array, format="PNG")
	return bytes_array.getvalue()

#Not Used. Function to create byte-encoded images for use with tkinter
def convert_png_to_bytes_array(png_path):
	bytes_array = io.BytesIO()
	Image.open(png_path, mode="r").save(bytes_array, format="PNG")
	return bytes_array.getvalue()

def load(file_name, size = None):
	width, height = size
	img = Image.open(file_name)
	if size:
		img = img.resize((width, height), Image.BOX)
	
def convert_tk_image_to_pixel_array(img):
	img = asarray(img)
	for j in range(height):
		for i in range(width):	
			d = img[j][i]
			d = [k for k in d]
	return d


def convert_image_to_grayscale(image):
	return image.convert('LA')

def convert_image_to_blackandwhite(image):
	image = image.convert('L')
	return image.convert('1')

