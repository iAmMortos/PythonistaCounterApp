import ui
from number_slider import NumberSlider
from color_pallet import ColorPallet
from recent_colors import RecentColors
import sharedlibs

sharedlibs.add_path_for('brightness', 'view_swap')
from brightness import Brightness
from view_swap import ViewSwap

class ColorPicker (ui.View):
	
	EDGE_PADDING = 6
	COMPONENT_PADDING = 8
	
	def __init__(self):
		self.recent_colors = RecentColors()
		self.result = None
		
	def did_load(self):
		self.background_color = (0.5, 0.5, 0.5, 0.5)
		self.window = self['window']
		
		self.close_btn = self.window['close_btn']
		self.close_btn.action = self.close_popup
		
		self.select_btn = self.window['select_btn']
		self.select_btn.action = self.select_and_close
		
		self.demo_lbl = self.window['demo_lbl']
		self.title_lbl = self.window['title_lbl']
		self.preset_lbl = self.window['preset_lbl']
		self.recent_lbl = self.window['recent_lbl']
		
		# custom views
		self.cpr = NumberSlider.load_view()
		self.cpr.initialize(scale=(0,255), value=255, color='#f00')
		self.cpr.action = self.handle_color_slider_change
		
		self.cpg = NumberSlider.load_view()
		self.cpg.initialize(scale=(0,255), value=255, color='#0f0')
		self.cpg.action = self.handle_color_slider_change
		
		self.cpb = NumberSlider.load_view()
		self.cpb.initialize(scale=(0,255), value=255, color='#00f')
		self.cpb.action = self.handle_color_slider_change
		
		self.preset_pallet = ColorPallet.load_view()
		self.preset_pallet.initialize()
		self.preset_pallet.action = self.handle_pallet_selection
		
		self.recent_pallet = ColorPallet.load_view()
		self.recent_pallet.initialize(colors = self.recent_colors.colors)
		self.recent_pallet.action = self.handle_pallet_selection
		
		# swap placeholders for custom views
		view_swapper = ViewSwap(self.window)
		view_swapper.swap('cp1', self.cpr)
		view_swapper.swap('cp2', self.cpg)
		view_swapper.swap('cp3', self.cpb)
		view_swapper.swap('presets', self.preset_pallet)
		view_swapper.swap('recent', self.recent_pallet)
		
	def close_popup(self, sender):
		self.parent.close_color_picker(self)
		
	def select_and_close(self, sender):
		rf,gf,bf,a = self.color
		r = round(rf * 255)
		g = round(gf * 255)
		b = round(bf * 255)
		self.result = self.get_hex_color(r,g,b)
		self.recent_colors.add(self.result)
		self.parent.close_color_picker(self)
		
	def initialize(self, parent, color='#fff'):
		self.color = ui.parse_color(color)
		self.parent = parent
		r,g,b,a = self.color
		self.cpr.value = r*255
		self.cpg.value = g*255
		self.cpb.value = b*255
		
	def handle_color_slider_change(self, sender):
		c = (self.cpr.value/255, self.cpg.value/255, self.cpb.value/255, 1)
		self.color = c
		self.demo_lbl.background_color = c
		self.demo_lbl.text_color = 'black' if Brightness.is_light(*(c[:3])) else 'white'
		self.demo_lbl.text = self.get_hex_color(self.cpr.value, self.cpg.value, self.cpb.value)
		
	def handle_pallet_selection(self, sender):
		color = sender.background_color
		self.color = color
		r,g,b,a = color
		r = round(r*255)
		g = round(g*255)
		b = round(b*255)
		self.cpr.value = r
		self.cpg.value = g
		self.cpb.value = b
		
	def layout(self):
		ep = ColorPicker.EDGE_PADDING
		cp = ColorPicker.COMPONENT_PADDING
		x,y,w,h = self.window.frame
		half_width = (w - 2*ep - cp) / 2
		half_x = cp + ep + half_width
		pallet_height = (h - ep - 3*cp - self.title_lbl.height - self.preset_lbl.height - self.recent_lbl.height) / 2
		
		self.preset_pallet.frame = (ep, self.preset_lbl.y + self.preset_lbl.height + cp, half_width, pallet_height)
		
		lx,ly,lw,lh = self.recent_lbl.frame
		self.recent_lbl.frame = (lx, self.preset_pallet.y + self.preset_pallet.height + cp, lw, lh)
		
		self.recent_pallet.frame = (ep, self.recent_lbl.y + self.recent_lbl.height + cp, half_width, pallet_height)
		
		cx,cy,cw,ch = self.cpr.frame
		self.cpr.frame = (half_x, cy, half_width, ch)
		cx,cy,cw,ch = self.cpg.frame
		self.cpg.frame = (half_x, cy, half_width, ch)
		cx,cy,cw,ch = self.cpb.frame
		self.cpb.frame = (half_x, cy, half_width, ch)
		cx,cy,cw,ch = self.demo_lbl.frame
		self.demo_lbl.frame = (half_x, cy, half_width, ch)
		
	def front_fill(self, s, l, c):
		return c*(l - len(s)) + s
			
	def get_hex_color(self, r, g, b):
		def gh(d):
			return hex(d).split('x')[-1]
		def ff(s):
			return self.front_fill(s, 2, '0')
		return ('#%s%s%s' % (ff(gh(r)), ff(gh(g)), ff(gh(b)))).upper()
		
	@staticmethod
	def load_view():
		return ui.load_view()
