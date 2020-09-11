def reduce(v): return max(0, min(v, 255))
def rgb_to_hex(rgb): return "#{0:02x}{1:02x}{2:02x}".format(reduce(rgb[0]), reduce(rgb[1]), reduce(rgb[2]))
def rgba_to_hex(rgba): return "#{0:02x}{1:02x}{2:02x}{3:02x}".format(reduce(rgba[0]), reduce(rgba[1]), reduce(rgba[2]), reduce(rgba[3]))
def single_rgb_to_hex(rgb): return "#{0:02x}".format(rgb)
def hex_to_rgb(hex): return [int(hex[i:i+2], 16) for i in range(1,6,2)]
def hex_to_rgba(hex):
	try:
		return [int(hex[i:i+2], 16) for i in range(1,8,2)]
	except ValueError as e:
		rgba = hex_to_rgb(hex)
		rgba.append(255)
		return rgba
def get_gradient(steps): return [rgb_to_hex(v) for v in reversed(linear_gradient("#FFFFFF", "#000000", steps))]
def rgb_to_scalar(list): return [int(x / 255.0) for x in list]
def scalar_to_rgb(list): return [int(x * 255.0) for x in list]
def linear_gradient(start_hex = "#000000", finish_hex="#FFFFFF", n=10):
	s = hex_to_rgb(start_hex)
	f = hex_to_rgb(finish_hex)
	rgb = [s]
	# Calcuate a color at each evenly spaced value of t from 1 to n
	for t in range(1, n):
		rgb.append([int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)])
	return rgb
def get_rainbow(steps):
	assert steps % 4 == 0, "Steps should be divisible by 4"
	rainbow = []
	step = int(steps / 4)
	rainbow.extend(linear_gradient("#FF0000", "#FFFF00", step))
	rainbow.extend(linear_gradient("#7FFF00", "#00FF7F", step))
	rainbow.extend(linear_gradient("#00FFF", "#0000FF", step))
	rainbow.extend(linear_gradient("#7F00FF", "#FF007f", step))
	return [rgb_to_hex(v) for v in reversed(rainbow)]