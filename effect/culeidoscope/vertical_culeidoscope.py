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
DEFAULT_MIRROR_POSITION_RATIO = 0.5

class VerticalCuleidoscope(VideoEffect):
	"""
	Rectangular kaleidoscope
	"""
	def __init__(self, 
		input_stream: StreamInfo, 
		intensity:int = 0.5, 
		vband_width_ratio : float = DEFAULT_VBAND_WIDTH_RATIO, 
		vband_spacing_ratio : float = DEFAULT_VBAND_SPACING_RATIO,
		mirror_position_ratio : float = DEFAULT_MIRROR_POSITION_RATIO
	):

		super().__init__(input_stream)
		# defines motion
		self.intensity = intensity
		self.vband_width_ratio = vband_width_ratio
		self.vband_spacing_ratio = vband_spacing_ratio
		self.mirror_position_ratio = mirror_position_ratio

	def get_mirrored_vband_rectangles(self, 
		vband_width_ratio : float = DEFAULT_VBAND_WIDTH_RATIO,
		vband_spacing_ratio : float = DEFAULT_VBAND_SPACING_RATIO,
		mirror_position_ratio : float = 0.5):
		"""
		Create mirrored vertical bands with :mirror_position_ratio: as the axis of symmetry 
		Return a tuple (rect_l, rect_r) with the bands
		"""
		assert vband_width_ratio >= 0 and vband_width_ratio <= 1
		assert vband_spacing_ratio >= 0 and vband_spacing_ratio <= 1
		assert mirror_position_ratio >= 0 and mirror_position_ratio <= 1

		vband_spacing = (self.input_stream.width / 2) * vband_spacing_ratio
		vband_width = (self.input_stream.width / 2) * vband_width_ratio
		mirror_position = self.input_stream.width * mirror_position_ratio

		rectangle_left = Rectangle(
			top_x = mirror_position - vband_spacing - vband_width,
			top_y = 0,
			width = vband_width,
			height = self.input_stream.height
		)

		rectangle_right = Rectangle(
			top_x = mirror_position + vband_spacing,
			top_y = 0,
			width = vband_width,
			height = self.input_stream.height
		)

		return (rectangle_left, rectangle_right)

	def set_effect_params(self, 
		vband_width_ratio : float = DEFAULT_VBAND_WIDTH_RATIO, 
		vband_spacing_ratio : float = DEFAULT_VBAND_SPACING_RATIO, 
		mirror_position_ratio : float = 0.5
	):
		"""
		:vband_width_ratio: <float> Width of the vertical band, expressed as a ratio of input width. Should be in the range (0,1)
		:vband_spacing_ratio: <float> Spacing of vertcal bands, expressed as a ratio of input width. Should be in the range (0,1)
		:mirror_position_ratio: <float> Position of the axis of symmetry, expressed as a ratio of input width. Should be in the range (0,1)
		"""
		rectangle_left,rectangle_right = self.get_mirrored_vband_rectangles(
			vband_width_ratio = vband_width_ratio,
			vband_spacing_ratio = vband_spacing_ratio,
			mirror_position_ratio = mirror_position_ratio
			)

		self.output_stream = swap_rectangles(self.input_stream, rectangle_left, rectangle_right)

	def next_effect(self):
		self.vband_spacing_ratio = (self.vband_spacing_ratio + 0.1) % 1
		return self.set_effect_params(
			self.vband_width_ratio, self.vband_spacing_ratio, self.mirror_position_ratio
		)

	def kick_drum_effect(self, **kwargs):
		return self.set_effect_params(
			vband_width_ratio = 0.1,
			vband_spacing_ratio = 0.05,
			mirror_position_ratio = self.mirror_position_ratio
		)

	def snare_drum_effect(self, **kwargs):
		return self.set_effect_params(
			vband_width_ratio = 0.4,
			vband_spacing_ratio = 0.2,
			mirror_position_ratio = self.mirror_position_ratio
		)

	def hihat_drum_effect(self, **kwargs):
		self.mirror_position_ratio = (self.mirror_position_ratio + 0.07) % 0.8
		self.kick_drum_effect()

class WideningVerticalCuleidoscope(VerticalCuleidoscope):

	def next_effect(self):
		self.vband_width_ratio = (self.vband_width_ratio + 0.1) % 1
		return self.set_effect_params(
			self.vband_width_ratio, self.vband_spacing_ratio, self.mirror_position_ratio
			)

	def kick_drum_effect(self, **kwargs):
		return self.set_effect_params(
			0.1, self.vband_spacing_ratio, self.mirror_position_ratio
		)

	def snare_drum_effect(self, **kwargs):
		return self.set_effect_params(
			0.5, self.vband_spacing_ratio, self.mirror_position_ratio
		)

class MultiplyingVerticalCuleidoscope(VerticalCuleidoscope):
	def __init__(self,   
			input_stream: StreamInfo, 
			num_mirrored_bands : int =0,
			intensity : int = 0.5, 
			vband_width_ratio : float = 0.05, 
			vband_spacing_ratio : float = 0.07,
			mirror_position_ratio:float = DEFAULT_MIRROR_POSITION_RATIO
		):

		self.num_mirrored_bands = num_mirrored_bands
		super().__init__(
			input_stream=input_stream, 
			intensity=intensity, 
			vband_width_ratio=vband_width_ratio, 
			vband_spacing_ratio=vband_spacing_ratio,
			mirror_position_ratio=mirror_position_ratio
		)

	def create_n_mirrored_vbands(self, num_vbands:int = 0):
		for i in range(num_vbands):
			self.set_effect_params(
				vband_width_ratio=self.vband_width_ratio, 
				vband_spacing_ratio=(self.vband_spacing_ratio*i) % 1, 
				mirror_position_ratio=self.mirror_position_ratio
			)
			self.input_stream = self.output_stream

	def next_effect(self):
		self.create_n_mirrored_vbands(self.num_mirrored_bands)
		self.num_mirrored_bands += 1

	def kick_drum_effect(self, **kwargs):
		return self.create_n_mirrored_vbands(10)

	def snare_drum_effect(self, **kwargs):
		return self.create_n_mirrored_vbands(20)

