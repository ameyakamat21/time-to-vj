# Author: Ameya Kamat (ameyakamat21@gmail.com)
# Python imports
from abc import (
	ABC,
	abstractmethod
)

# External imports
from ffmpeg.nodes import Stream

class VideoEffect(ABC):
	"""
	Interface for all video effects
	"""

	def __init__(self, input_stream: Stream, output_stream: Stream):
		self.input_stream = input_stream
		self.output_stream = output_stream

	def set_input(self, input_stream: Stream):
		"""
		Set input
		"""
		self.input_stream = input_stream

	def set_output(self, output_stream: Stream):
		"""
		Set output
		"""
		self.output_stream = output_stream

	@abstractmethod
	def set_effect(self):
		"""
		Connect input -> effect -> output
		"""
		raise NotImplementedError

	@abstractmethod
	def unset_effect(self):
		"""
		Connect input -> output (without effect)
		"""
		raise NotImplementedError


	@abstractmethod
	def set_intensity(self, intensity: int):
		"""
		What 'intensity' exactly means is TBA
		"""
		raise NotImplementedError
