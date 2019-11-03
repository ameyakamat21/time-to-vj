# Python
from math import floor
from random import randint

# External
from ffmpeg.nodes import Stream

# Local library
from effect.effect import VideoEffect
from video import StreamInfo
from utils import Rectangle

class RandomCuleidoscope(VideoEffect):
	"""
	Rectangular kaleidoscope
	"""
	def __init__(self, input_stream: StreamInfo, intensity:int = 0.5):
		super().__init__(input_stream)
		# defines motion
		self.intensity = intensity
		# num_divisions in the range [1,8]
		self.num_divisions = max(1, round(intensity * 8))

	def set_intensity(self, set_intensity: int = 0):
		# TBA for now
		pass

	def set_effect_params(self, position:int = 0):
		"""
		Description TBA
		"""
		# divisions along the horizontal plane
		num_x_divisions = 8
		# divisions along the vertical plane
		num_y_divisions = 6

		cell_width = self.input_stream.width / num_x_divisions
		cell_height = self.input_stream.height / num_y_divisions
		
		cell_list = []
		for i in range(num_x_divisions):
			for j in range(num_y_divisions):
				new_cell = Rectangle(
					top_x = i * cell_width,
					top_y = j * cell_height,
					width = cell_width,
					height = cell_height
				)
				cell_list.append(new_cell)

		print("Got cell list (length {}): {}".format(len(cell_list), cell_list))

		raw_output_stream = self.input_stream.raw_stream
		# Select random 2 rectangles to swap
		while len(cell_list) > 0:
			rand_cell_1 = cell_list.pop(randint(0, len(cell_list)-1))
			rand_cell_2 = cell_list.pop(randint(0, len(cell_list)-1))

			raw_output_stream = (
				raw_output_stream.
					filter_(filter_name = "swaprect",
						w = rand_cell_1.width,
						h = rand_cell_1.height,
						x1 = rand_cell_1.top_x, 
						y1 = rand_cell_1.top_y,
						x2 = rand_cell_2.top_x,
						y2 = rand_cell_2.top_y
					)
			)

		self.output_stream = StreamInfo(
			raw_stream=raw_output_stream,
			width=self.input_stream.width,
			height=self.input_stream.height
		)

	def next_effect(self):
		return self.set_effect_params(0)
