# Python
from math import (
	floor
)

# External
from ffmpeg.nodes import Stream

# Local library
from effect import VideoEffect
from video import StreamInfo

class ZoomAndTranslateFixed(VideoEffect):
	"""
	Crop to center of the video, moving around
	"""

	def set_intensity(self, set_intensity: int = 0):
		# TBA for now
		pass

	def set_position(self, position:int = 0):
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
		
class ZoomAndTranslateRelative(VideoEffect):
	"""
	The extent of translation can vary depending on intensity
	"""
	def __init__(self, input_stream: StreamInfo, intensity:int = 0.2):
		super().__init__(input_stream)
		# defines motion
		self.intensity = intensity
		self.zoom_level = 1

	def set_intensity(self, set_intensity: int = 0):
		# from 0 - 1
		pass

	def center_to_topleft_coords(self, center_x: float, center_y: float, width: float, height: float, zoom_level: float):
		x_topleft = center_x - (width/2) / zoom_level
		y_topleft = center_y - (height/2) / zoom_level


	def set_position(self, position:int = 0):
		"""
		Chooses one of 9 positions: 0-8
		"""
		# Ensure position is in the range 0-8
		position 	= floor(abs(position)) % 9

		# The following variables define the center x,y coordinates of the cropped section

		# direction values are -1, 0 or 1
		x_direction = floor(position / 3) - 1
		y_direction = floor(position % 3) - 1

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
		