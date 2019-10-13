# Author: Ameya Kamat (ameyakamat21@gmail.com)

from dataclasses import dataclass
import ffmpeg

@dataclass
class VideoFile:
	path: str
	width: int
	height: int

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

		# Raise error if inorrect number of streams
		if(len(video_stream_list) != 1):
			raise ValueError(
				"File {} has {} video streams. Should be 1.".
				format(path, len(video_stream_list))
			)

		video_stream = video_stream_list[0]

		self.height = video_stream["height"]
		self.width = video_stream["width"]