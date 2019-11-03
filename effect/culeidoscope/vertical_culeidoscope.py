# Python
from math import floor
from random import randint

# External
from ffmpeg.nodes import Stream

# Local library
from effect.effect import VideoEffect
from video import StreamInfo
from utils import Rectangle
from effect.culeidoscope.util import swap_rectangles

class VerticalCuleidoscope(VideoEffect):
	"""
	Rectangular kaleidoscope
	"""
	def __init__(self, input_stream: StreamInfo, intensity:int = 0.5):
		super().__init__(input_stream)
		# defines motion
		self.intensity = intensity
		# num_divisions in the range [1,8]
		self.num_divisions = max(1, round(intensity * 8))

	def set_effect_params(self, vband_width_ratio=0.1, vband_spacing_ratio=0.1):
		"""
		:vband_width_ratio: <float> Width of the vertical band, expressed as a ratio of input width. Should be in the range (0,1)
		:vband_spacing_ratio: <float> Spacing of vertcal bands, expressed as a ratio of input width. Should be in the range (0,1)
		"""

		assert vband_width_ratio >= 0 and vband_width_ratio <= 1
		assert vband_spacing_ratio >= 0 and vband_spacing_ratio <= 1

		vband_spacing = (self.input_stream.width / 2) * vband_spacing_ratio
		vband_width = (self.input_stream.width / 2) * vband_width_ratio

		rectangle_left = Rectangle(
			top_x = (self.input_stream.width/2) - vband_spacing - vband_width,
			top_y = 0,
			width = vband_width,
			height = self.input_stream.height
		)

		rectangle_right = Rectangle(
			top_x = (self.input_stream.width/2) + vband_spacing,
			top_y = 0,
			width = vband_width,
			height = self.input_stream.height
		)

		self.output_stream = swap_rectangles(self.input_stream, rectangle_left, rectangle_right)
