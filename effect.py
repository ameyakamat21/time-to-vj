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

	def set_input(self, input_stream: Stream):
		"""
		Set input
		"""
		self.input_stream = input_stream

	def get_output(self):
		"""
		Set output
		"""
		return self.output_stream

	@abstractmethod
	def enable_effect(self):
		"""
		Connect input -> effect -> output
		"""
		raise NotImplementedError

	def unset_effect(self):
		"""
		Connect input -> output (without effect)
		"""
		self.output_stream = self.input_stream


	@abstractmethod
	def set_intensity(self, intensity: int):
		"""
		What 'intensity' exactly means is TBA
		"""
		raise NotImplementedError

	@abstractmethod
	def set_position(self, position:int = 0):
		"""
		What 'position' exactly means is TBA
		"""
		raise NotImplementedError

	def set_next_effect(self, next_effect: "VideoEffect"):
		"""
		Connect next effect in chain
		"""
		next_effect.set_input(self.output_stream)
