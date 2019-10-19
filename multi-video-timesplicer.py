# Core python #
import os
from time import time

# External #
import ffmpeg

# Library
from video import (
	VideoFile,
	StreamInfo
)

INPUT_VIDEO_DIR = "/Users/ameya/side-projects/ffmpeg-video-editing/time-to-vj/raw-video/trimmed-choreo"
NUM_VIDEOS = 10

# Define input streams

OUT_VIDEO_DIR	= "processed-video"

def inpath(video_path):
	return os.path.join(IN_VIDEO_DIR, video_path)

def outpath(video_path):
	return os.path.join(OUT_VIDEO_DIR, video_path)

def get_splice_times():
	time_diff_list = []
	start_time = time()
	while True:
		# Wait for user input
		inp = input("enter for next splice time. q to quit.")
		time_diff = time() - start_time
		time_diff_list.append(time_diff)
		print("Time diff: {}".format(time_diff))
		if(inp == "q"):
			print("Got quit request.")
			break
	return time_diff_list

input_stream_list = []

for i in range(NUM_VIDEOS):
	video_path_i = os.path.join(INPUT_VIDEO_DIR, "{}.mp4".format(i+1))
	print("Getting video from: {}.".format(video_path_i))
	input_stream_i = VideoFile(video_path_i).stream_info
	input_stream_list.append(input_stream_i)
	print("Duration: {}".format(input_stream_i.duration))


splice_times = get_splice_times()

concat_list = []
prev_splice_time = 0.0
for i in range(len(splice_times)):
	splice_time = splice_times[i]
	current_stream = input_stream_list[i % len(input_stream_list)]
	concat_list.append(
		current_stream.raw_stream.trim(
			start=prev_splice_time,
			end=splice_time
		).
		setpts("PTS-STARTPTS")
	)
	prev_splice_time = splice_time


# Works!
print("Created concat list")

(	ffmpeg.
	concat(*concat_list).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("salsa-3.mp4")).
	run()
)

