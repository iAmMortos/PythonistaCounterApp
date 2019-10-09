import ui
import sharedlibs
import dialogs
import threading

sharedlibs.add_path_for('brightness', 'ui_drag', 'hold_button', 'view_swap')
from brightness import Brightness
from draggable import Draggable
from hold_button import HoldButton
from view_swap import ViewSwap

class SingleCounter (Draggable):
	
	MARGIN = 6
	MAX_FONT_SIZE = 60
	
	def __init__(self):
		super().__init__()
		self._value = 0
		self._color = '#fff'
		self._title = ''
		self._swapper = ViewSwap(self)
	
	def did_load(self):
		self.corner_radius = 10
		
		self.opt_btn = self['opt']
		self.opt_btn.action = self.show_picker
		
		self.del_btn = self['del']
		self.del_btn.action = self.remove_me
		
		self.add1_btn = HoldButton(image='iob:ios7_arrow_up_32')
		self.add1_btn.repeat_action = self.add1
		self.add1_btn.hold = self.counting_started
		self.add1_btn.unhold = self.counting_stopped
		self.add1_btn.alpha = 0.3
		self._swapper.swap('add', self.add1_btn)
		
		self.add10_btn = HoldButton(image='iob:arrow_up_b_32')
		self.add10_btn.repeat_action = self.add10
		self.add10_btn.hold = self.counting_started
		self.add10_btn.unhold = self.counting_stopped
		self.add10_btn.alpha = 0.3
		self._swapper.swap('add10', self.add10_btn)
		
		self.sub1_btn = HoldButton(image='iob:ios7_arrow_down_32')
		self.sub1_btn.repeat_action = self.sub1
		self.sub1_btn.hold = self.counting_started
		self.sub1_btn.unhold = self.counting_stopped
		self.sub1_btn.alpha = 0.3
		self._swapper.swap('sub', self.sub1_btn)
		
		self.sub10_btn = HoldButton(image='iob:arrow_down_b_32')
		self.sub10_btn.repeat_action = self.sub10
		self.sub10_btn.hold = self.counting_started
		self.sub10_btn.unhold = self.counting_stopped
		self.sub10_btn.alpha = 0.3
		self._swapper.swap('sub10', self.sub10_btn)
		
		self.reset_btn = self['reset_btn']
		self.reset_btn.action = self.reset
		
		self.title_btn = self['title_btn']
		self.title_btn.action = self.handle_title_changed

		self.val_lbl = self['output']
		
		self.handle = self['handle']
		self.handle.enabled = False
		super().did_load()
		
	def add1(self, sender):
		self.value = self.value + 1
		self.parent.update(self)
		
	def add10(self, sender):
		self.value = self.value + 10
		self.parent.update(self)
		
	def sub1(self, sender):
		self.value = self.value - 1
		self.parent.update(self)
		
	def sub10(self, sender):
		self.value = self.value - 10
		self.parent.update(self)
		
	def reset(self, sender):
		self.value = 0
		self.parent.update(self)
		
	def show_picker(self, sender):
		self.parent.show_color_picker(self)
		
	def remove_me(self, sender):
		self.parent.remove(self)
		
	def update_background_color(self, color):
		r,g,b,a = ui.parse_color(color)
		fg_color = 'black' if Brightness.is_light(r,g,b) else 'white'
		
		self.background_color = color
		
		self.opt_btn.tint_color = fg_color
		self.del_btn.tint_color = fg_color
		self.add1_btn.tint = fg_color
		self.add10_btn.tint = fg_color
		self.sub1_btn.tint = fg_color
		self.sub10_btn.tint = fg_color
		self.reset_btn.tint_color = fg_color
		self.title_btn.tint_color = fg_color
		self.val_lbl.text_color = fg_color
		self.handle.tint_color = fg_color
		
	def get_save_str(self):
		return '%s|%s|%s' % (self.title, self.value, self.color)
		
	def initialize(self, parent, index, view_size, st=None):
		self.view_size = view_size
		self.parent = parent
		# property setters
		self.index = index
		if st != None:
			t,v,c = st.split('|')
			self.title = t
			self.value = int(v)
			self.color = c
		else:
			self.title = 'New Counter'
			self.value = 0
			self.color = '#fff'
			
	def handle_title_changed(self, sender):
		this = self
		def verify_title_changed():
			response = None
			try:
				response = dialogs.input_alert('Change title to: ')
			except KeyboardInterrupt:
				pass # standard cancel
			if response != None:
				this.title = response
				this.parent.update(this)
		threading.Thread(target=verify_title_changed).start()
		
	def resize_text(self):
		lw = self.val_lbl.width
		fn,fs = self.val_lbl.font
		al = self.val_lbl.alignment
		tx = str(self._value)
		cs = SingleCounter.MAX_FONT_SIZE
		while True:
			w,h = ui.measure_string(tx, font=(fn,cs))
			if w <= lw:
				break
			cs -= 1
		self.val_lbl.font = (fn,cs)
		
	def get_handles(self):
		return self.handle
		
	def picked_up(self):
		self.parent.picked_up(self)
		self.bring_to_front()
		
	def dragged(self):
		self.parent.dragged(self)
		
	def dropped(self):
		self.parent.dropped(self)
		
	def counting_started(self, sender):
		self.parent.counting_started(sender)
		
	def counting_stopped(self, sender):
		self.parent.counting_stopped(sender)
		
	@property
	def index(self):
		return self.idx
		
	@index.setter
	def index(self, val):
		sw,sh = self.view_size
		m = SingleCounter.MARGIN 
		x,y,w,h = self.frame
		f = [(w + m) * val + m,0,w,sh - m]
		self.idx = val
		self.frame = f
		
	@property
	def value(self):
		return self._value
		
	@value.setter
	def value(self, val):
		self._value = val
		self.resize_text()
		self.val_lbl.text = str(val)
		
	@property
	def color(self):
		return self._color
		
	@color.setter
	def color(self, val):
		self._color = val
		self.update_background_color(val)
		
	@property
	def title(self):
		return self._title
		
	@title.setter
	def title(self, val):
		self._title = val
		self.title_btn.title = val
		
	@staticmethod
	def load_view():
		return ui.load_view()
