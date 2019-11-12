# Python
from math import (
	floor
)

# External
from ffmpeg.nodes import Stream

# Local library
from effect.effect import VideoEffect
from video import StreamInfo

class ZoomAndTranslateFixed(VideoEffect):
	"""
	Crop to center of the video, moving around
	"""

	def set_intensity(self, set_intensity: int = 0):
		# TBA for now
		pass

	def set_effect_params(self, position:int = 0):
		"""
		Chooses one of 9 positions: 0-8
		"""
		# Ensure position is in the range 0-8
		position 	= floor(abs(position)) % 9
		x_start 	= floor(position / 3) * self.input_stream.width
		y_start 	= floor(position % 3) * self.input_stream.height
		width 		= self.input_stream.width / 2
		height 		= self.input_stream.height / 2

		raw_output_stream = (
			self.input_stream.raw_stream.
			crop(
				x=x_start, 
				y=y_start,
				width=width, 
				height=height
			).
			filter_("pad", 
				width=self.input_stream.width, 
				height=self.input_stream.height, 
				x=int(self.input_stream.width/4), 
				y=int(self.input_stream.height/4)
			)
		)

		self.output_stream = StreamInfo(
			raw_stream=raw_output_stream,
			width=self.input_stream.width,
			height=self.input_stream.height
		)
		
class ZoomAndTranslateRelativeRectangular(VideoEffect):
	"""
	The extent of translation can vary depending on intensity
	"""
	def __init__(self, input_stream: StreamInfo = None, intensity:int = 0.2):
		super().__init__(input_stream)
		# defines motion
		self.intensity = intensity
		self.zoom_level = 1
		self.kick_drum_possibilities_index = 0
		self.snare_drum_possibilities_index = 0
		self.x_direction = 0
		self.y_direction = 0

	def set_intensity(self, set_intensity: int = 0):
		# from 0 - 1
		pass

	def center_to_topleft_coords(self, center_x: float, center_y: float, width: float, height: float, zoom_level: float):
		x_topleft = center_x - (width/2) / zoom_level
		y_topleft = center_y - (height/2) / zoom_level

	def crop(self,
	 	x_center: float,
	 	y_center: float,
	 	width: float,
	 	height: float,
	 ):
		x_topleft = x_center - (self.input_stream.width/4) / self.zoom_level
		y_topleft = y_center - (self.input_stream.height/4) / self.zoom_level

		raw_output_stream = (
			self.input_stream.raw_stream.
			crop(
				x=x_topleft, 
				y=y_topleft,
				width=width, 
				height=height
			)
		)

		return StreamInfo(
			raw_stream=raw_output_stream,
			width=self.input_stream.width,
			height=self.input_stream.height
		)


	def set_previous_effect_params(self):
		return self.set_effect_params(self.x_direction, self.y_direction)

	def set_effect_params(self, x_direction, y_direction):
		"""
		:x_direction: x Direction to move the frame from the center. In the range (-1, 1)
		:y_direction: y Direction to move the frame from the center. In the range (-1, 1)
		"""
	
		# The following variables define the center x,y coordinates of the cropped section

		# direction values are -1, 0 or 1
		# x_direction = floor(position / 3) - 1
		# y_direction = floor(position % 3) - 1

		self.x_direction = x_direction
		self.y_direction = y_direction

		x_magnitude = (self.input_stream.width/8) * self.intensity
		y_magnitude = (self.input_stream.height/8) * self.intensity

		x_original_center 	= self.input_stream.width / 2
		y_original_center	= self.input_stream.height / 2

		x_new_center = x_original_center + (x_magnitude * x_direction)
		y_new_center = y_original_center + (y_magnitude * y_direction)

		x_topleft = x_new_center - (self.input_stream.width/4) / self.zoom_level
		y_topleft = y_new_center - (self.input_stream.height/4) / self.zoom_level

		width		= (self.input_stream.width / 2) / self.zoom_level
		height		= (self.input_stream.height / 2) / self.zoom_level

		raw_output_stream = (
			self.input_stream.raw_stream.
			crop(
				x=x_topleft, 
				y=y_topleft,
				width=width, 
				height=height
			)
		)

		self.output_stream = StreamInfo(
			raw_stream=raw_output_stream,
			width=self.input_stream.width,
			height=self.input_stream.height
		)


	def kick_drum_effect(self, **kwargs):
		# Can be the bottom left 3 rects
		xy_direction_possibilities = [(-1, 0), (-1, 1), (0, 1)]
		x_dir, y_dir = xy_direction_possibilities[self.kick_drum_possibilities_index % 3]
		self.kick_drum_possibilities_index += 1
		return self.set_effect_params(x_direction=x_dir, y_direction=y_dir)

	def snare_drum_effect(self, **kwargs):
		# Can be the bottom left 3 rects
		xy_direction_possibilities = [(0,-1), (1, -1), (1, 0)]
		x_dir, y_dir = xy_direction_possibilities[self.snare_drum_possibilities_index % 3]
		self.snare_drum_possibilities_index += 1
		return self.set_effect_params(x_direction=x_dir, y_direction=y_dir)

	def hihat_drum_effect(self, **kwargs):
		# Can be the bottom left 3 rects
		xy_direction_possibilities = [(-1,-1), (0, 0), (0, 0)]
		x_dir, y_dir = xy_direction_possibilities[self.snare_drum_possibilities_index % 3]
		self.snare_drum_possibilities_index += 1
		return self.set_effect_params(x_direction=x_dir, y_direction=y_dir)

	def next_effect(self, **kwargs):
		raise NotImplementedError
		