import ui
import os
import dialogs
import math
import threading
import time
from color_picker import ColorPicker
from single_counter import SingleCounter

save_file = 'data.txt'

class Counter(ui.View):
	
	SAVE_INTERVAL = 10 # seconds
	
	def __init__(self):
		self.counters = []
		self._is_dragging = False
		self._running = True
		self._needs_save = False
		threading.Thread(target= self.save_loop).start()
		
	def did_load(self):
		self.background_color = '#a4a5af'
		self.scroll_view = self['scrl']
		
		self.add_btn = self['add_btn']
		self.add_btn.action = self.add_counter
		
		self.reset_btn = self['reset_btn']
		self.reset_btn.action = self.reset
		
		self.close_btn = self['close_btn']
		self.close_btn.action = self.exit
		
		self._sized = False
		
	def will_close(self):
		self._running = False
		if self._needs_save:
			self.save()
		
	def add_counter(self, sender):
		sc = SingleCounter.load_view()
		sc.initialize(self, len(self.counters), self.get_scroll_view_size())
		self.counters += [sc]
		self.scroll_view.add_subview(sc)
		self.resize_scroll_area()
		self._needs_save = True
		
	def reset(self, sender):
		this = self
		def verify_reset():
			result = None
			try:
				result = dialogs.alert('Reset?', 'Delete all counters?', 'Yes')
			except KeyboardInterrupt:
				pass # standard cancel
			if result == 1:
				for c in this.counters:
					this.scroll_view.remove_subview(c)
				this.counters = []
				this.add_counter(None)
				self._needs_save = True
				self.resize_scroll_area()
		# without the thread, this consistantly causes the application to completely freeze
		threading.Thread(target=verify_reset).start()
		
	def exit(self, sender):
		self.close()
			
	def layout(self):
		if not self._sized:
			if not self.load():
				self.add_counter(None)
			self._sized = True
			
	def remove(self, sender):
		if sender in self.counters:
			self.scroll_view.remove_subview(sender)
			self.counters.remove(sender)
			for i,c in enumerate(self.counters):
				c.index = i
			self.resize_scroll_area()
			self._needs_save = True
			
	def show_color_picker(self, sender):
		self._selected_counter = sender
		cp = ColorPicker.load_view()
		cp.initialize(self, sender.color)
		w,h = ui.get_screen_size()
		cp.frame = (0,0,w,h)
		self.add_subview(cp)
	
	def close_color_picker(self, sender):
		result = sender.result
		if result:
			self._selected_counter.color = result
			self._needs_save = True
		self.remove_subview(sender)
		
	def counting_started(self, sender):
		self.scroll_view.scroll_enabled = False
		
	def counting_stopped(self, sender):
		self.scroll_view.scroll_enabled = True
		
	def picked_up(self, sender):
		self._is_dragging = True
		self._drag_start_idx = self.counters.index(sender)
		self.scroll_view.scroll_enabled = False
		
	def dragged(self, sender):
		drag_idx = self.get_counter_location_index(sender)
		# show the other counters moving around when you drag yours
		for i,c in enumerate(self.counters):
			if i != self._drag_start_idx:
				if drag_idx < self._drag_start_idx and i >= drag_idx and i < self._drag_start_idx:
					c.index = i + 1
				elif drag_idx > self._drag_start_idx and i <= drag_idx and i > self._drag_start_idx:
					c.index = i - 1
				else:
					c.index = i			
		
	def dropped(self, sender):
		self._is_dragging = False
		self.scroll_view.scroll_enabled = True
		drag_idx = self.get_counter_location_index(sender)
		self.counters.remove(sender)
		self.counters = self.counters[:drag_idx] + [sender] + self.counters[drag_idx:]
		for i,c in enumerate(self.counters):
			c.index = i
		self._needs_save = True
				
	def update(self, sender):
		self._needs_save = True
		
	def save(self):
		lines = [c.get_save_str() for c in self.counters]
		with open(save_file, 'w') as f:
			f.write('\n'.join(lines))
		self._needs_save = False
			
	def load(self):
		if os.path.exists(save_file):
			with open(save_file, 'r') as f:
				lines = [line.strip() for line in f.readlines()]
				for i,line in enumerate(lines):
					c = SingleCounter.load_view()
					c.initialize(self, i, self.get_scroll_view_size(), st=line)
					self.scroll_view.add_subview(c)
					self.counters += [c]
			self.resize_scroll_area()
			return True
		else:
			return False
			
	def get_counter_location_index(self, counter):
		x,y = counter.center
		return min(math.floor(x / (counter.width + SingleCounter.MARGIN)), len(self.counters) - 1)
			
	def resize_scroll_area(self):
		sc = SingleCounter.load_view()
		self.scroll_view.content_size = ((sc.width + SingleCounter.MARGIN) * len(self.counters) + 60, 0)
			
	def get_scroll_view_size(self):
		x,y,w,h = self.scroll_view.frame
		return (w,h)
		
	def save_loop(self):
		while(self._running):
			if self._needs_save:
				self.save()
			time.sleep(Counter.SAVE_INTERVAL)
		
	@staticmethod
	def load_view():
		return ui.load_view()

if __name__ == '__main__':
	Counter.load_view().present(style='full_screen', orientations=['landscape'], hide_title_bar=True)
