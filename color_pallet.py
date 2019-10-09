import ui
import math

class ColorPallet(ui.View):
	
	DEFAULT = ['#00000c','#6a757b','#b2b7bb','#fff','#f195be','#e73d96','#b2015c','#771d7e','#7f3e98','#1b3f95','#082466','#4963ae','#009ac8','#00a2b1','#006a5e','#949ba1','#d0d3d8','#f3f3f3','#f5c5dd','#f8b9d4','#d13c5a','#b96a6d','#9a5aa4','#b9b3d9','#8ca4d4','#b0cbe9','#cdebeb','#572500','#9c5f0c','#f0d8be','#f9efe3','#fcd2c2','#f89d88','#b32018','#cd6619','#f28820','#e5b539','#ffe292','#669044','#477f40','#356639','#007386','#bd854a','#e7c39f','#f7e5d1','#f9b6a6','#ee2d24','#faa634','#dc9a1f','#fed24d','#ffe292','#d3e27d','#65b560','#97ce8a','#008aae']
	MIN_BUTTON_WIDTH = 36
	BUTTON_HEIGHT = 32
	PADDING = 6
	
	def __init__(self):
		self.button_width = None
		self.btns = []
	
	def did_load(self):
		self.sv = self['sv']
		
	def layout(self):
		nbx = (self.sv.width - ColorPallet.PADDING) // (ColorPallet.MIN_BUTTON_WIDTH + ColorPallet.PADDING)
		self.button_width = ((self.sv.width - ColorPallet.PADDING) / nbx) - ColorPallet.PADDING
		x,y = (0,0)
		for n,btn in enumerate(self.btns):
			self.position_button(btn, x, y)
			x += 1
			while x >= nbx:
				x -= nbx
				y += 1
		w,h = self.sv.content_size
		self.sv.content_size = (w, ColorPallet.PADDING + math.ceil(len(self.btns) / nbx) * (ColorPallet.BUTTON_HEIGHT + ColorPallet.PADDING))
		
	def action(self, sender):
		pass
		
	def initialize(self, colors=None):
		self.colors = colors if colors is not None else ColorPallet.DEFAULT
		for color in self.colors:
			b = self.make_button(color)
			self.btns += [b]
			self.sv.add_subview(b)
			
	def make_button(self, color):
		this = self
		b = ui.Button()
		b.title = ''
		b.corner_radius = 5
		b.border_width = 1
		b.background_color = color
		b.action = lambda s: this.action(b)
		return b
		
	def position_button(self, btn, x, y):
		bx = ColorPallet.PADDING + x * (self.button_width + ColorPallet.PADDING)
		by = ColorPallet.PADDING + y * (ColorPallet.BUTTON_HEIGHT + ColorPallet.PADDING)
		bw = self.button_width
		bh = ColorPallet.BUTTON_HEIGHT
		btn.frame = (bx,by,bw,bh)
		
	@staticmethod
	def load_view():
		return ui.load_view()

if __name__ == '__main__':
	pass
