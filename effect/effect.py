# Author: Ameya Kamat (ameyakamat21@gmail.com)
# Python imports
from abc import (
	ABC,
	abstractmethod
)
from dataclasses import dataclass

# External imports
from ffmpeg.nodes import Stream

# Internal imports
from video import StreamInfo

@dataclass
class VideoEffect(ABC):
	"""
	Interface for all video effects
	"""
	input_stream: StreamInfo = None
	output_stream: StreamInfo = None

	def __init__(self, input_stream: StreamInfo):
		self.input_stream = input_stream
		# Initially, effect is not applied
		self.output_stream = input_stream

	def unset_effect(self):
		"""
		Connect input -> output (without effect)
		"""
		self.output_stream = self.input_stream

	def set_intensity(self, intensity: int):
		"""
		What 'intensity' exactly means is TBA
		"""
		raise NotImplementedError

	@abstractmethod
	def set_effect_params(self, **kwargs):
		"""
		What 'position' exactly means is TBA
		"""
		raise NotImplementedError

	def kick_drum_effect(self, **kwargs):
		raise NotImplementedError

	def snare_drum_effect(self, **kwargs):
		raise NotImplementedError

	def hihat_drum_effect(self, **kwargs):
		raise NotImplementedError

	def next_effect(self, **kwargs):
		raise NotImplementedError
