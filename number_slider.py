import ui

class NumberSlider(ui.View):
	def did_load(self):
		self.num = self['num']
		self.num.action = self.handle_num_changed
		self.slider = self['slider']
		self.slider.action = self.handle_slider_changed
	
	def initialize(self, scale=(0,10), value=0, color=None, precision=0):
		if color:
			self.slider.tint_color = color
		self._scale = scale
		self._precision = precision
		self.value = value
			
	@property
	def value(self):
		return self._value
		
	@value.setter
	def value(self, val):
		self._value = self.truncate(val, self._precision)
		self.num.text = str(self.value) if self._precision != 0 else str(round(self.value))
		self.slider.value = self.num_to_slider(self._scale, self.value)
		self.action(self)
		
	def slider_to_num(self, scale, slider):
		a,b = scale
		return (b - a) * slider + a
	
	def num_to_slider(self, scale, num):
		a,b = scale
		return (num - a) / (b - a)
		
	def handle_num_changed(self, sender):
		v = None
		try:
			v = float(sender.text)
		except Exception as ex:
			v = self._scale[0]
		v = max(v, self._scale[0])
		v = min(v, self._scale[1])
		
		self.value = v
		sender.value = self._value
		#self.slider.value = self.num_to_slider(self._scale, self._value)
		
	def handle_slider_changed(self, sender):
		self.value = self.slider_to_num(self._scale, sender.value)
		#self.num.text = str(self._value)
		
	def truncate(self, num, precision):
		v = round(num * (10**precision)) / (10**precision)
		if precision <= 0:
			return round(v)
		return v
		
	def action(self, sender):
		pass
		
	@staticmethod
	def load_view():
		return ui.load_view()
		
if __name__ == '__main__':
	v = ui.View()
	ns = NumberSlider.load_view()
	ns.initialize(scale=(0, 255), value=100, color='red')
	ns.flex = 'WTB'
	ns.frame = (5,5,80,50)
	v.add_subview(ns)
	v.present()
