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

magnifying_glass_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x01\x85iCCPICC Profile\x00\x00x\x9c}\x91=H\xc3P\x14\x85\x8f\xa9\xd2"\x15\x07;hq\xc8P\x9d,\x88\x8a8J+\x16\xc1Bi+\xb4\xea`\xf2\xd2?h\xd2\x90\xa4\xb88\n\xae\x05\x07\x7f\x16\xab\x0e.\xce\xba:\xb8\n\x82\xe0\x0f\x88\x93\xa3\x93\xa2\x8b\x94x_Rh\x11\xe3\x85G>\xce\xbb\xe7\xe4\xbd\xfb\x00\xa1Ye\xaa\xd9;\t\xa8\x9ae\xa4\x1311\x97_\x15\xfd\xaf\x08`\x04@\x0f\xc2\x123\xf5df1\x0b\xcf\xfa\xba\xa7>\xaa\xbb(\xcf\xf2\xee\xfb\xb3\x06\x94\x82\xc9\xe8G"\xf1<\xd3\r\x8bx\x83xv\xd3\xd29\xef\x13\x87XYR\x88\xcf\x89\'\x0c: \xf1#\xd7e\x97\xdf8\x97\x1c\x16xf\xc8\xc8\xa6\xe3\xc4!b\xb1\xd4\xc5r\x17\xb3\xb2\xa1\x12\xcf\x10G\x14U\xa3|!\xe7\xb2\xc2y\x8b\xb3Z\xad\xb3\xf69\xf9\r\x83\x05m%\xc3uZ\xa3H`\tI\xa4 BF\x1d\x15Ta!J_\x8d\x14\x13i\xda\x8fy\xf8\xc3\x8e?E.\x99\\\x150r,\xa0\x06\x15\x92\xe3\x07\x7f\x83\xdf\xb35\x8b\xd3SnR0\x06\xf4\xbd\xd8\xf6\xc7\x18\xe0\xdf\x05Z\r\xdb\xfe>\xb6\xed\xd6\t\xe0{\x06\xae\xb4\x8e\xbf\xd6\x04\xe6>Iot\xb4\xc8\x110\xb8\r\\\\w4y\x0f\xb8\xdc\x01\x86\x9ft\xc9\x90\x1c\xc9GK(\x16\x81\xf73z\xa6<0t\x0b\xf4\xaf\xb9sk\xef\xe3\xf4\x01\xc8\xd2\xac\x96o\x80\x83C`\xbcD\xd9\xeb\x1e\xf7\x0et\xcf\xed\xdf\x9e\xf6\xfc~\x00 Tr\x86  \xb6\xb6\x00\x00\x00UIDATx\x9c\xdd\x93K\x12\x00 \x08B\xa5\xfb\xdf\xb9\x96\xfd\x84\xd4e,C\xec\xcdP\xb0\xa9n\\`F\x0b\x84\xa5\x8f\xc3\xf4n\x92~S\xe6\xe3\xfcZP\xd2g\x0bXU\xb2bD\x86Hf#\x90U)\xa2h\xd0#\xc4J\xf0\x12}\xa1\x19t\x97$[\xa3\xfc\x0b\xa5%\x03\t\x0b\x0c\x1bW\xf4ba\x00\x00\x00\x00IEND\xaeB`\x82'
floppy_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00YIDATx\x9c\xbd\x93A\n\x00 \x08\x04w\xa3\xff\x7f\xb9nb\x1bDj$t\x08\xb6q\x10#\x80\x81X\xd1_Z\xf01\xb4\xa1\x07P\x82tG3\x06\xc9\x18,\x90\x0c`\x81\xf4C\xe8j\xb8Y\x03+5\xd0A\xfe7\xb8]*3}n\xb0u\x90\xda\x0c\xcb\x06e\x00\x11\xff\x8do\r&2<\t)\xe6\x84\xac\xa0\x00\x00\x00\x00IEND\xaeB`\x82'
export_to_bytes_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00TIDATx\x9c\xc5R\xcb\x0e\x00 \x08\xa2\xd6\xff\xff\xb2\x9d<\xf8\xc0Z[\x93#"S\x11\xe8\xc6\x00 \x84\xcf\x90i\x03\x99\x8aXm\x16\xe2+\xf4\x1b\xac\x87\x1es\x07f \x88Ih\xa3\xe1\xd9\n>\xde\xcc\xb0\x9c\xc0\x9b\xb0\xbf\xf8\x9b\x82\x8e\xcd\xbe\x158\x14\xaf\x8e\xd8\x8f\r^q\x0f\x17I\xca\t\xc4\x00\x00\x00\x00IEND\xaeB`\x82'
to_grayscale_bytes=  b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x8bIDATx\x9c\xad\x93K\x0e\xc40\x08C\xedjn\x04\xf7\xbf\x9a\xbbh'\x9f\x16JT\xd5\xd9$!<\x8cD(@HD\x80Y\xec\xaf\xdf\x94pG\xf5\x1b\xc6\xb0\xad\xaaP\xa9\x01\xdc\xec,\xd9\xd7\x8a(@\x1c\x1eK\x00\xc9s\xaf\xee\xfcM\x0b$K'7\x00yT^\x85\xb0\x1b\x9f5\xb6r\x9c'h\x0b\xa4\x80\x0cB\x12\x92\xe0\xeeq\x0bU;W-\xcd\x81b\x83\x00\xda$\x06\xe8!=\xaa|\x01\xe4r\xf7G\x07\xe5g1\xb3\xc7A\xf8\xee/\xbc\xd5\x0e\xfa38\x83C\xf0\x9e\x91\x00\x00\x00\x00IEND\xaeB`\x82"
flip_horizontal_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00cIDATx\x9c\xb5\x92K\n\x00 \x08D\xc7\xe8\xfeW\xb6E\x10a\xa3)\xd1,\xfd\xbctL\x00(\xa6\x045)\x00\xb4b\xd3\xa1o\x00M\xc6(\x80\x16z9\x0b\x88\x0c\x15S\xb3\x82\x96z\xbb\xc6\x15P\xd2\xf3\x15:\x89\x95V\xd8'\xa0&9\xcd\xeb\x11\xbbB\x04\xa1\x17b\x1eD+\x1c9\xcf\xc4\xe8\x1f\xa4\x00i=\x03\x06R\x89\x10\x1d\x11\x13\xf1_\x00\x00\x00\x00IEND\xaeB`\x82"
flip_vertical_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00[IDATx\x9c\xcdS1\x12\x00 \x08\xc2\xfe\xffg\x9b\xba\xeb\x14tp(GQ\x025\x03\xe0\x18\xc4\x9a4\x03\x80\x15XTFk\x95\x02f\x8bZe\x04\xa7\xf0~\xd1\x02&\tXsKR\x85w\r\xe3-\xfcG\xd0yNx$\xa8&M7\xa4.Q\xa9H\xf5j\x06\xd5\x1d\xa4\xe4\xdb\xdf\xb8\x013\x0b\x12\x13\xd2\xdc\xdaE\x00\x00\x00\x00IEND\xaeB`\x82'
rotate_right_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00fIDATx\x9c\xad\x93Q\x0e\xc0 \x08C[\xb2\xfb_\x99\xfdl\xc9\x82E\xa6\xd8\xc4\x1fy\x14A\x05\x9a\xe2$\xe6\x05\xeb\x00\xa8\x0cb\xa2*\xfa2\x83\x81\x07\xb02\xa6\t\x80"Y\x19\x02\x00Lm&\x92\xadY\x08fCM\xe7r\xfd\xac\x9e\xde\xd6J\x0b_\xf9\xb3\xb6\r\xe6\xae+\\\xfb\x04\xbb\x0f\x89\x19\x14\xc1\xb2h\xe73\x9d\xd1\r4\xaa\x14\x12L4\x91\xa7\x00\x00\x00\x00IEND\xaeB`\x82'
rotate_left_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00cIDATx\x9c\xadS[\x12\x00\x11\x0c\xeb\x1a\xf7\xbfr\xf7\x07S6\xad\xd0\xcd\x0f\xfaH\xc2\x94H\x12O[\xd5\xec\xc5\xc4P\xadK\xd0\xcfk\xa3\xd7\x03\t"EE\xb9\xc2\xa8\x98\xd8G\xd0#\xd8]c\xc0#\x88H&\x17u\t\x1e\xa3;\xd0@\x91"\xf8\x05\xac\x8b\xa9.\xed\x80\x1a\x96(\x87^\xffj\x94\x11\xa8\xcf\x94\xc6\x0b\xc0j\x14\x121\x82h\xc9\x00\x00\x00\x00IEND\xaeB`\x82'
plus_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00-IDATx\x9ccd\xc0\r\xfe\xa3\xf1\x19\xb1)b\xc2c\x00Q`\xd4\x00H\xc8\xa2\x876}]0\xf0\x06`M]P0\x9a\x12\xe9e\x00\x00"\xd2\x03\x1d\x12\xb9\x81\x89\x00\x00\x00\x00IEND\xaeB`\x82'
trash_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00-IDATx\x9ccd\xc0\x0e\xfe\xe3\x10g\xc4%\x80K\x03!\xc0\xc8D\xa6F\xea\x01t?\x11\xeb\x15\xb8>\x8a\xbd0j\xc0\xa8\x01\x83\xc3\x00\x00\xf2\xb9\x03\x1c\xd6\xd7\xf8 \x00\x00\x00\x00IEND\xaeB`\x82'
copy_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00TIDATx\x9c\xc5\x93;\x0e\x00 \x08C\x8b\xf1\xfeW\xd6\t\x17\xc5V1\xb1#m^\x08\x1f\x03\xd0\xb0\x97\x11\x9f\x02\x98\xcf\x03,\xa3\x00\xc2\\=\x84z\xddVE\x050\xf9\x85\x04#\x99Cn\x01\x03\x92\x01 \xdb\xc1\x1b\x80\xafQ\xbd\x05Y\xf2q\xfd\x9fA\xf4\xaa\xf2L:6*\x12\x0b:\xd1\x01?\x00\x00\x00\x00IEND\xaeB`\x82'
copy_bytes_wide = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00_IDATx\x9c\xbd\x91A\x0e\x00!\x08\x03\x87\xcd\xfe\xff\xcb\xee\x89D\x8c\x05\xa3f{\x14R\xa7\xc5\x80\x86\x96%3\x00\x9eb\x9e\x99\x87%\xb5\x98\xcd\x96\x08<\x824y\x93\x9f\xd5[\xe8\xa5"(\xcd\x15\x81kv\x05\xef\xc5v\tB/;\x06A}\x84\xa5\x9b\x8f\xbaB\xa0\x8a\xfa\x87\xe0j\x893\x95Q\x8e\t>k\x92\x10\x1fW\xad\x10U\x00\x00\x00\x00IEND\xaeB`\x82'
new_layer_from_image_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00cIDATx\x9c\xbd\x90Q\n\x800\x0cC_\xc5\xfb_y\xfe8\xd1\x9a-s\xa8\x81\xc1(\xe9k\x9b\x00\n\xe3\nU,\x8d\x7f\xcfwh\x99\x00I@m\xc8+ZP\x05\xc4\xfe\x9e\xe4q\x01\xa8\xa9\xf9$\x19`6\xaa\xda\x19x\xf3\xaa\r2\xa89\x19`5[t\x9b\x190\xb8P\xc3\x9d\xf0\xaa\xa6B\xb4\xfa\xf5\x84o\xb4\x01\xb9\xd6\x17\x08\x7f~yJ\x00\x00\x00\x00IEND\xaeB`\x82'
up_arrow_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00JIDATx\x9cc`\xc0\x0f\xfeC1N\xc0D@366Q\x06`\xd3\x80\xd5\x10l\x06\xe0s2\x86\x1c\xba\x01x\xfd\x8bM\r\x13.\tb\raB\x17 \xd5\x10F25\xc3\x01#>\xd3\x89Q\x8f/\x1d\x10\x05F\r\x18\x0c\x06\x00\x00\x9f\xc8\x10\x0e\xae\xb1^D\x00\x00\x00\x00IEND\xaeB`\x82'
down_arrow_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00MIDATx\x9ccd\xc0\x0e\xfe\xe3\x10gD\x17`\xc2\xa1\x90h0j\xc0`0\x80\x91\x01w\x9c\x13\xed\x02\x8c\xc4A\x8a\x03`^ \xc7\x10F\x98\x0bP\x04H\xd1\x8cn\x00\xb1\x86\xa0\xa8\xc1\x16\x0b\xf8\x0c!:3a3\x84\xac\xc0\xfe\xcf@ \x9a\x01\x86\xa4\x04&EWG\x05\x00\x00\x00\x00IEND\xaeB`\x82'
name_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x11\x00\x00\x00\x10\x08\x06\x00\x00\x00\xf01\x94_\x00\x00\x00aIDATx\x9c\xad\x92Q\n\x00 \x08Cgt\xff+\xd7W`\xc5\x9cdB\x98d\xcf1\x04r1\x8eL\x1bTMAMM\xc8\xc4\x82X\x05\xd4\xdc\xbd\x04R\x1e\xb0?\xfe\xa4\xe1\xf4\xcd\x82&s9\x84\xf4H\x8a\x08&`\x9b\x12y#=Q\xcbG%U\x96\xcd\xaa\x00\x00\x18~\xd9\x98\x17*\xdf\xc5\x8b\x92/\x9eLo\xc5+\xeb\xbc\xec0\x94\x00\x00\x00\x00IEND\xaeB`\x82'
merge_down_symbol_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00VIDATx\x9c\xddQ1\x12\x00 \x08\xc2\xfe\xffg\xdb\xea\xce YZbT\xe0\x10\x03@\xe2D\x90\x19\x18w\xb8D1\x93\x06U@\xc5\xc0\x8e*\t\r\xa2\xde\xea\x1a-]=A\x95'9\xac\x83\x9b\xc9\xb1\xbb\x95hA\x19\xb0\x144\xd9\xb3\x046>~\xa3\xfd\x85\x0e\x89\xa6\x97\t\x0fz\x0b n\xf1\x8ds\x00\x00\x00\x00IEND\xaeB`\x82"
selection_options_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00aIDATx\x9c\xed\x94K\n\xc0 \x0cD\x9f\xa5\xf7\xbf\xf2t\xd3H\x08\xfd\xa8\xd1\x9d\x0f\x04cd\x98\x0c"\x80\xeee\xa4\xea\x83\xc9\x94\x89Z\x82\x05\x0eMY\xbf\xb7\x1a\xd9\x19\xe6\xd9\x19\xe6Y\xe2\xb0\x97\xafi4\xea\xf0IT~\xd3\x9b\xe1\xeb\x9f8\xea\xd0\x9e\x9b\x17.\xbeAl4\xd4\xf1L\x00\xe7\xa0\xc3\xe8\xb4r\x01\xe1\r#\xfeK\xaa+`\x00\x00\x00\x00IEND\xaeB`\x82'
up_carret_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00QIDATx\x9c\xed\x92\xc1\x0e\x00 \x08B\xd5\xff\xffg;\xb55\x02\xe6\xadK\x1c\xe5\x81[\x16\xf1\xf5^i\xbc\x9e\xb05\x0c\xab\x19-\xa0\xa0\xf2\xb0\xc0\x85)S\xca\x98\x96\x14\x0e@\x19\xfa\xa1{\x03.L\xb7\x9eRW`[\xc7gt\x7f\xe3\xf2\xb0\xc0\x85)\xb3\x00\xc8\xb0\r\x10{\x8cD\xc6\x00\x00\x00\x00IEND\xaeB`\x82'
down_carret_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00TIDATx\x9c\xed\x91\xb1\x12\x00\x10\x0cCS\xff\xff\xcf5qJBM\x16\x99J\x9awU\xc0\xd7{\x19\x00\x9f\xce\x19\xf5LQF&\xcc\x00'\xc8\xe21\x80\x82Pp\x81~\xb7\x8bz\x94Y\xa2I\xc9\xda\x04\xe1\xe2&<\x03\xb2\x90\xd0\xc3\x96\xb8\x83,\x9e\xfa\x05\x06\xa1\xe0\nPm\x0b\x14\xaa\x93\x9f.\x00\x00\x00\x00IEND\xaeB`\x82"
layers_symbol_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00\x88IDATx\x9c\xdd\x94Q\x0e\xc0 \x08C\xd5\xfb\xdf\x99\xfd\x0c3\xb1\xd4\xea\xf65\x13\x13E\xf6V\x1a\xb4\x94|\xd8=\xb7F%05w\x99\xb4RE\xc1\xf1p\xa7D\x08~\x06\xb7\xfdB`\xdf\x9c\xc2&V\xfb\x126,^\x80\x87\x92[8\x90Z\x03\xc0\xba\x18/\xd9B\x92\x02\x86\xfe\xd7\x18\x000\xd6\xe4\x16\xf6\xd4\xc3\x0c\x9c\xc2\xd0G\n8\x83W\x0f\xc0?\x110U\xfa\x7f\x0f'Q\xac\xdf\x14\x0f\xa7\xb5\xd2\xc0\xab\xc76S+\x81\xb3\xfb\xde\xe3\x17\xc0\xce,\x11\xce3\xde\x16\x00\x00\x00\x00IEND\xaeB`\x82"
folder_options_symbol_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00dIDATx\x9c\xa5RA\x0e\xc0 \x08\x03\xb3\xff\x7f\x99\x1d\x16\x17m\xc0\x96\xd8\x0bQ\xda\xda n\x1f\xc2j\xf8\xa1g\x83\x88\x99\xb9\xf9B\xc8^\n\xe0\xb6\rh\x82qj21&`\xbc\xd4\x9c%\xa8\xc4?\x1e\x95XAIpm\x803\xda\xcej\x82\x80\xda2\x98\xb3I\xf7EM\xe0P\xdb\x06\xa9x^*\x8bT\xe2\xfa\x1b_\xdd\xf7\x10\x1a%V\x92.\x00\x00\x00\x00IEND\xaeB`\x82'

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
		
		self.frame_manager = FrameFrame(self, self.project, panes2)
		self.frame_manager.pack(side = "left", fill = "x", expand = True, pady = 0, anchor = "n")
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
		selection_menu.add_command(label = "New Layer from Selection", command = self.new_layer_image_from_selection)
		self.selections_options_menu_button = Label(self.tool_bar, image = self.selection_options_image, font = "bold")
		self.selections_options_menu_button.pack(side = "left")
		bind_popup("<Button-1>", self.selections_options_menu_button, selection_menu)

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

	def fill_selection(self):
		layer = self.project.selected_frame.selected_layer
		if layer.selection:
			ToolController.fill_selection(layer, ToolController.start_selection, ToolController.end_selection)
			self.refresh()
	def flip_selection_vertical(self):
		layer = self.project.selected_frame.selected_layer
		if layer.selection:
			ToolController.flip_selection_vertical(layer, ToolController.start_selection, ToolController.end_selection)
			self.refresh()
	def flip_selection_horizontal(self):
		layer = self.project.selected_frame.selected_layer
		if layer.selection:
			ToolController.flip_selection_horizontal(layer, ToolController.start_selection, ToolController.end_selection)
			self.refresh()
	def rotate_selection_right(self):
		layer = self.project.selected_frame.selected_layer
		if layer.selection:
			ToolController.rotate_selection_right(layer, ToolController.start_selection, ToolController.end_selection)
			self.refresh()
	def rotate_seletion_left(self):
		layer = self.project.selected_frame.selected_layer
		if layer.selection:
			ToolController.rotate_selection_left(layer, ToolController.start_selection, ToolController.end_selection)
			self.refresh()
	def export_selection(self):
		layer = self.project.selected_frame.selected_layer
		if layer.selection:
			image = ToolController.export_selection(layer, ToolController.start_selection, ToolController.end_selection)
			SaveMenu(self.controller, image)
			self.refresh()
	def export_selection_as_bytes(self):
		layer = self.project.selected_frame.selected_layer
		if layer.selection:
			image = ToolController.export_selection(layer, ToolController.start_selection, ToolController.end_selection)
			print(convert_tk_image_to_bytes_array(image))

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


class FrameFrame(ttk.LabelFrame):
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

class BaseTile:
	def __init__(self, manager):
		self.x, self.y, self.width, self.height = None, None, None, None
		self.manager = manager
		self.thumbnail = None
		self.references = []
		self.active = None
		self.active_references = []
		self.id = "BaseTile"

	def set_id(self, id): self.id = id

	def activate(self):
		self.active = True
		self.manager.activate_tile(self)

	def deactivate(self):
		self.active = False
		self.manager.deactivate_tile(self)

	def is_in_range(self, pointer_x, pointer_y):
		if pointer_x > self.x and pointer_x < self.x + self.width:
			if pointer_y > self.y and pointer_y < self.y + self.height:
				return True
	def is_in_row(self, pointer_y): 
		if pointer_y > self.y and pointer_y < self.y + self.height: return True

	def on_click(self, pointer_x, pointer_y): return self.check_click_regions(pointer_x, pointer_y)

	def check_click_regions(self, pointer_x, pointer_y): pass

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