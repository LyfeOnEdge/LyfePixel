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