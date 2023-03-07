import pygame
from pygame.math import Vector2 as vector
from settings import *
from support import *

from pygame.image import load

from editor import Editor
from level import Level

from os import walk

class Main:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		self.imports()

		self.editor_active = True
		self.transition = Transition(self.toggle)
		self.editor = Editor(self.land_tiles, self.switch)

		# cursor 
		surf = load('C:/Users/Dhrumil/MPR/graphics/cursors/mouse.png').convert_alpha()
		cursor = pygame.cursors.Cursor((0,0), surf)
		pygame.mouse.set_cursor(cursor)

	def imports(self):
		# terrain
		self.land_tiles = import_folder_dict('C:/Users/Dhrumil/MPR/graphics/terrain/land')
		self.water_bottom = import_folder_dict('C:/Users/Dhrumil/MPR/graphics/terrain/water')
		self.water_top_animation = import_folder('C:/Users/Dhrumil/MPR/graphics/terrain/water/animation')

		# coins
		self.gold = import_folder('C:/Users/Dhrumil/MPR/graphics/items/gold')
		self.silver = import_folder('C:/Users/Dhrumil/MPR/graphics/items/silver')
		self.diamond = import_folder('C:/Users/Dhrumil/MPR/graphics/items/diamond')
		self.particle = import_folder('C:/Users/Dhrumil/MPR/graphics/items/particle')

		# palm trees
		self.palms = {folder: import_folder(f'C:/Users/Dhrumil/MPR/graphics/terrain/palm/{folder}') for folder in list(walk('C:/Users/Dhrumil/MPR/graphics/terrain/palm'))[0][1]}

		# enemies
		self.spikes = load('C:/Users/Dhrumil/MPR/graphics/enemies/spikes/spikes.png').convert_alpha()
		self.tooth = {folder: import_folder(f'C:/Users/Dhrumil/MPR/graphics/enemies/tooth/{folder}') for folder in list(walk('C:/Users/Dhrumil/MPR/graphics/enemies/tooth'))[0][1]}
		self.shell = {folder: import_folder(f'C:/Users/Dhrumil/MPR/graphics/enemies/shell_left/{folder}') for folder in list(walk('C:/Users/Dhrumil/MPR/graphics/enemies/shell_left/'))[0][1]}
		self.pearl = load('C:/Users/Dhrumil/MPR/graphics/enemies/pearl/pearl.png').convert_alpha()

		# player
		self.player_graphics = {folder: import_folder(f'C:/Users/Dhrumil/MPR/graphics/player/{folder}') for folder in list(walk('C:/Users/Dhrumil/MPR/graphics/player/'))[0][1]}

		# clouds
		self.clouds = import_folder('C:/Users/Dhrumil/MPR/graphics/clouds')

		# sounds
		self.level_sounds = {
			'coin': pygame.mixer.Sound('C:/Users/Dhrumil/MPR/audio/coin.wav'),
			'hit': pygame.mixer.Sound('C:/Users/Dhrumil/MPR/audio/hit.wav'),
			'jump': pygame.mixer.Sound('C:/Users/Dhrumil/MPR/audio/jump.wav'),
			'music': pygame.mixer.Sound('C:/Users/Dhrumil/MPR/audio/SuperHero.ogg'),
		}

	def toggle(self):
		self.editor_active = not self.editor_active
		
		#if self.editor_active:
			#self.editor.editor_music.play()
		

	def switch(self, grid = None):
		self.transition.active = True
		if grid:
			self.level = Level(
				grid, 
				self.switch,{
					'land': self.land_tiles,
					'water bottom': self.water_bottom,
					'water top': self.water_top_animation,
					'gold': self.gold,
					'silver': self.silver,
					'diamond': self.diamond,
					'particle': self.particle,
					'palms': self.palms,
					'spikes': self.spikes,
					'tooth': self.tooth,
					'shell': self.shell,
					'player': self.player_graphics,
					'pearl': self.pearl,
					'clouds': self.clouds},self.level_sounds)

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			
			if self.editor_active:
				self.editor.run(dt)
			else:	
				self.level.run(dt)
			self.transition.display(dt)
			pygame.display.update()


class Transition:
	def __init__(self, toggle):
		self.display_surface = pygame.display.get_surface()
		self.toggle = toggle
		self.active = False

		self.border_width = 0
		self.direction = 1
		self.center = (WINDOW_WIDTH /2, WINDOW_HEIGHT / 2)
		self.radius = vector(self.center).magnitude()
		self.threshold = self.radius + 100

	def display(self, dt):
		if self.active:
			self.border_width += 1000 * dt * self.direction
			if self.border_width >= self.threshold:
				self.direction = -1
				self.toggle()
			
			if self.border_width < 0:
				self.active = False
				self.border_width = 0
				self.direction = 1
			pygame.draw.circle(self.display_surface, 'black',self.center, self.radius, int(self.border_width))

if __name__ == '__main__':
	main = Main()
	main.run() 