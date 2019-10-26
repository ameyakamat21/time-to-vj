# Author: Ameya Kamat (ameyakamat21@gmail.com)

from dataclasses import dataclass
import ffmpeg

@dataclass
class StreamInfo:
	raw_stream 	: ffmpeg.nodes.Stream = None
	width 		: int = 0
	height 		: int = 0
	duration	: float = 0.0

	def trim(self, **kwargs):
		"""
		:start_frame: <int> frame of start of trim
		:end_frame: <int> frame of end of trim
		"""
		self.raw_stream = self.raw_stream.trim(**kwargs).setpts("PTS-STARTPTS")


	def trimmed_copy(self, **kwargs):
		"""
		:start_frame: <int> frame of start of trim
		:end_frame: <int> frame of end of trim
		"""
		return StreamInfo(
			raw_stream = (
				self.raw_stream.
				trim(**kwargs).setpts("PTS-STARTPTS")
			),
			width=self.width,
			height=self.height
		)

	
@dataclass
class VideoFile:
	path 		: str
	width 		: int
	height 		: int
	duration	: float
	stream 		: ffmpeg.nodes.Stream
	stream_info	: StreamInfo
	probe_info	: dict

	def __init__(self, path: str):
		self.path = path
		probe_info = ffmpeg.probe(path)
		# Get the video stream - should be a list with a single element
		video_stream_list = list(
			filter(
				lambda stream: stream["codec_type"] == "video",  
				probe_info["streams"]
			)
		)
		self.probe_info = probe_info

		# Raise error if inorrect number of streams
		if(len(video_stream_list) != 1):
			raise ValueError(
				"File {} has {} video streams. Should be 1.".
				format(path, len(video_stream_list))
			)

		video_stream = video_stream_list[0]

		self.height 		= video_stream["height"]
		self.width 			= video_stream["width"]
		self.duration		= video_stream["duration"]
		self.stream 		= ffmpeg.input(path)
		self.stream_info 	= StreamInfo(
			raw_stream=self.stream, 
			width=self.width, 
			height=self.height,
			duration=self.duration
		)

		
