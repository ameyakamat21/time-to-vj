# Core python #
import os
from time import time
from math import floor

# External #
import ffmpeg

# Library
from video import (
	VideoFile,
	StreamInfo
)

from zoom_and_translate import ZoomAndTranslate

INPUT_VIDEO_DIR = "/Users/ameya/side-projects/ffmpeg-video-editing/time-to-vj/raw-video/choreo-selection-1"
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

video_name_list = ["1.mp4", "8.mp4", "9.mp4", "10.mp4", "12.mp4", "15.mp4", "18.mp4", "19.mp4", "21.mp4", "24.mp4", "30.mp4", "31.mp4", "32.mp4", "36.mp4"]
input_stream_list = list(
	map(
		lambda filename: VideoFile(os.path.join(INPUT_VIDEO_DIR, filename)).stream_info,
		video_name_list
	)
)

# for i in range(NUM_VIDEOS):
# 	video_path_i = os.path.join(INPUT_VIDEO_DIR, "{}.mp4".format(i+1))
# 	print("Getting video from: {}.".format(video_path_i))
# 	input_stream_i = VideoFile(video_path_i).stream_info
# 	input_stream_list.append(input_stream_i)
# 	print("Duration: {}".format(input_stream_i.duration))

def timesplice_multiple_videos():
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
		output(outpath("salsa-5.mp4")).
		run()
	)


wh_ratio = 1.7777777
cell_video_height = 200
cell_video_width = cell_video_height * wh_ratio
vid_str = input_stream_list[0]

def one_matrix_cell():
	(
		vid_str.raw_stream.trim(
				start=10.0,
				end=30.0
		).
		setpts("PTS-STARTPTS").
		filter_("scale", width=cell_video_width, height=cell_video_height).
		filter_("pad", width=vid_str.width, height=vid_str.height, x=20, y=20).
		output(outpath("salsa-pad-try.mp4")).
		run()
	)


def video_matrix():
	# Attempt to display all 10 videos together

	overlay_filt = (
		input_stream_list[0].raw_stream.
		filter_("scale", width=cell_video_width, height=cell_video_height).
		filter_("pad", width=input_stream_list[0].width, height=input_stream_list[0].height, x=20, y=20)
	)

	for i in range(1, NUM_VIDEOS):
		top_x = floor(i % 2) * 960 + 20
		top_y = floor(i / 2) * 216 + 20
		print("Placing video {} at {},{}",i, top_x, top_y)
		scaled_input_vid = (
			input_stream_list[i].raw_stream.
			filter_("scale", width=cell_video_width, height=cell_video_height)
		)
		overlay_filt = overlay_filt.overlay(scaled_input_vid, x=top_x, y=top_y)

	overlay_filt.output(outpath("salsa-simultaneous-2.mp4")).run()


def timesplice_an_effect(video_stream_info, out_filename):
	splice_times = get_splice_times()
	concat_list = []
	prev_splice_time = 0.0

	for i in range(len(splice_times)):
		splice_time = splice_times[i]
		stream_segment = video_stream_info.trimmed_copy(
				start=prev_splice_time,
				end=splice_time
			)
		zat = ZoomAndTranslate(input_stream = stream_segment)
		zat.set_position(i % 9)
		output_stream = zat.output_stream
		concat_list.append(
			output_stream.raw_stream
		)
		prev_splice_time = splice_time
	# Works!
	print("Created concat list")
	(	ffmpeg.
		concat(*concat_list).
		output(outpath(out_filename)).
		run()
	)

timesplice_an_effect(bike_1, "effects_timesplicer-1.mp4")



# Try concating trimmed copiestimesplice_an_effect_2(bike_1, "timesplice-effect-1.mp4")


(
	ffmpeg.
	concat(
		*[bike_1.raw_stream.trim(start=0, end=5).setpts("PTS-STARTPTS"),
		bike_1.raw_stream.trim(start=20, end=25).setpts("PTS-STARTPTS"),
		bike_1.raw_stream.trim(start=40, end=45).setpts("PTS-STARTPTS")]).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("concat-try-4.mp4")).
	run()
)


(
	ffmpeg.
	concat(
		*[bike_1.raw_stream.split().stream().trim(start=0, end=5).setpts("PTS-STARTPTS"),
		bike_1.raw_stream.split().stream().trim(start=20, end=25).setpts("PTS-STARTPTS"),
		bike_1.raw_stream.split().stream().trim(start=40, end=45).setpts("PTS-STARTPTS")]).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("concat-try-5.mp4")).
	run()
)
