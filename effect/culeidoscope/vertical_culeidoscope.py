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

DEFAULT_VBAND_WIDTH_RATIO = 0.1
DEFAULT_VBAND_SPACING_RATIO = 0.1

class VerticalCuleidoscope(VideoEffect):
	"""
	Rectangular kaleidoscope
	"""
	def __init__(self, 
		input_stream: StreamInfo, 
		intensity:int = 0.5, 
		vband_width_ratio : float = DEFAULT_VBAND_WIDTH_RATIO, 
		vband_spacing_ratio : float = DEFAULT_VBAND_SPACING_RATIO):

		super().__init__(input_stream)
		# defines motion
		self.intensity = intensity
		self.vband_width_ratio = vband_width_ratio
		self.vband_spacing_ratio = vband_spacing_ratio

	def get_mirrored_vband_rectangles(self, 
		vband_width_ratio : float = DEFAULT_VBAND_WIDTH_RATIO,
		vband_spacing_ratio : float = DEFAULT_VBAND_SPACING_RATIO,
		mirror_position_ratio : float = 0.5):
		"""
		Create mirrored vertical bands with :mirror_postion_ratio: as the axis of symmetry 
		Return a tuple (rect_l, rect_r) with the bands
		"""
		assert vband_width_ratio >= 0 and vband_width_ratio <= 1
		assert vband_spacing_ratio >= 0 and vband_spacing_ratio <= 1
		assert mirror_position_ratio >= 0 and mirror_position_ratio <= 1

		vband_spacing = (self.input_stream.width / 2) * vband_spacing_ratio
		vband_width = (self.input_stream.width / 2) * vband_width_ratio
		mirror_postion = self.input_stream.width * mirror_position_ratio

		rectangle_left = Rectangle(
			top_x = mirror_postion - vband_spacing - vband_width,
			top_y = 0,
			width = vband_width,
			height = self.input_stream.height
		)

		rectangle_right = Rectangle(
			top_x = mirror_postion + vband_spacing,
			top_y = 0,
			width = vband_width,
			height = self.input_stream.height
		)

		return (rectangle_left, rectangle_right)

	def set_effect_params(self, 
		vband_width_ratio : float = DEFAULT_VBAND_WIDTH_RATIO, 
		vband_spacing_ratio : float = DEFAULT_VBAND_SPACING_RATIO, 
		mirror_postion : float = 0.5
	):
		"""
		:vband_width_ratio: <float> Width of the vertical band, expressed as a ratio of input width. Should be in the range (0,1)
		:vband_spacing_ratio: <float> Spacing of vertcal bands, expressed as a ratio of input width. Should be in the range (0,1)
		:mirror_position: <float> Position of the axis of symmetry, expressed as a ratio of input width. Should be in the range (0,1)
		"""
		rectangle_left,rectangle_right = self.get_mirrored_vband_rectangles(vband_width_ratio, vband_spacing_ratio, mirror_postion)
		self.output_stream = swap_rectangles(self.input_stream, rectangle_left, rectangle_right)

	def next_effect(self):
		self.vband_spacing_ratio = (self.vband_spacing_ratio + 0.1) % 1
		return self.set_effect_params(
			self.vband_width_ratio, self.vband_spacing_ratio
			)

class WideningVerticalCuleidoscope(VerticalCuleidoscope):

	def next_effect(self):
		self.vband_width_ratio = (self.vband_width_ratio + 0.1) % 1
		return self.set_effect_params(
			self.vband_width_ratio, self.vband_spacing_ratio
			)

class MultiplyingVerticalCuleidoscope(VerticalCuleidoscope):
	def __init__(self,   
			input_stream: StreamInfo, 
			num_mirrored_bands : int =0,
			intensity : int = 0.5, 
			vband_width_ratio : float = 0.05, 
			vband_spacing_ratio : float = 0.07
		):

		self.num_mirrored_bands = num_mirrored_bands
		super().__init__(
			input_stream=input_stream, 
			intensity=intensity, 
			vband_width_ratio=vband_width_ratio, 
			vband_spacing_ratio=vband_spacing_ratio
		)

	def next_effect(self):
		self.num_mirrored_bands += 1

		# Initialize output stream
		for i in range(self.num_mirrored_bands):
			self.set_effect_params( 
				vband_width_ratio=self.vband_width_ratio, 
				vband_spacing_ratio=(self.vband_spacing_ratio*(i+1)) % 1, 
				mirror_postion=0.4
			)
			self.input_stream = self.output_stream

