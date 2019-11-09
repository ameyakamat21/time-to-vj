
from effect.effect import VideoEffect
from video import StreamInfo

class PassThrough(VideoEffect):
	"""
	Do nothing
	"""

	def set_effect_params(self, **kwargs):
		self.output_stream = StreamInfo(
			raw_stream=self.input_stream.raw_stream,
			width=self.input_stream.width,
			height=self.input_stream.height
		)
		
	def kick_drum_effect(self, **kwargs):
		self.set_effect_params()
		pass

	def snare_drum_effect(self, **kwargs):
		self.set_effect_params()
		pass

	def hihat_drum_effect(self, **kwargs):
		self.set_effect_params()
		pass

	def next_effect(self, **kwargs):
		self.set_effect_params()
		pass

