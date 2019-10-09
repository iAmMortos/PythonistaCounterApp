
import os

class RecentColors (object):
	
	FILE = 'recent_colors.txt'
	MAX_RECENT = 24
	
	def __init__(self):
		self._colors = []
		if os.path.exists(RecentColors.FILE):
			with open(RecentColors.FILE) as f:
				self._colors = [line.strip() for line in f.readlines()]
				
	def add(self, new_color):
		if new_color not in self.colors:
			self._colors = [new_color] + self._colors
			if len(self.colors) > RecentColors.MAX_RECENT:
				self._colors = self._colors[:RecentColors.MAX_RECENT]
		else:
			self._colors.remove(new_color)
			self._colors = [new_color] + self.colors
			
		with open(RecentColors.FILE, 'w') as f:
			f.write('\n'.join(self.colors))
		
	@property
	def colors(self):
		return self._colors
