# Python
from math import (
	floor
)

# External
from ffmpeg.nodes import Stream

# Local library
from effect import VideoEffect
from video import StreamInfo

class ZoomAndTranslate(VideoEffect):
	"""
	Crop to center of the video, moving around
	"""

	def enable_effect(self):
		"""
		Connect input -> effect -> output
		"""

		# Center crop
		raw_output_stream = (
			self.input_stream.raw_stream.
			crop(
				x=int(self.input_stream.width/4), 
				y=int(self.input_stream.height/4),
				width=int(self.input_stream.width/2), 
				height=int(self.input_stream.height/2)
			)
		)

		self.output_stream = StreamInfo(
			raw_stream=raw_output_stream,
			width=self.input_stream.width,
			height=self.input_stream.height
		)

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
		
