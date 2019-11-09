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

from effect.zoom_and_translate import (
	ZoomAndTranslateFixed,
	ZoomAndTranslateRelative
)

from effect.culeidoscope.random_culeidoscope import RandomCuleidoscope

from splice import (
	SpliceInfo,
	get_splices_from_input,
	get_splices_from_readchar
)

from constants import (
	FINAL_OUTPUT_WIDTH,
	FINAL_OUTPUT_HEIGHT
)

# Constants #
IN_VIDEO_DIR 	= "raw-video"
OUT_VIDEO_DIR	= "processed-video"

INPUT_VIDEO_DIR = "/Users/ameya/side-projects/ffmpeg-video-editing/time-to-vj/raw-video/choreo-selection-1"
NUM_VIDEOS = 10

# Define input streams

OUT_VIDEO_DIR	= "processed-video"

def inpath(video_path):
	return os.path.join(IN_VIDEO_DIR, video_path)

def outpath(video_path):
	return os.path.join(OUT_VIDEO_DIR, video_path)


universe_vid = VideoFile(inpath("universe-footage.mp4")).stream_info
bridge_vid = VideoFile(inpath("wooden-bridge.mp4")).stream_info
sun_vid = VideoFile(inpath("transit.mov")).stream_info

hector_1 = VideoFile(inpath("hector-vertical-1.mp4")).stream_info
hector_2 = VideoFile(inpath("hector-vertical-2.mp4")).stream_info

bike_1 = VideoFile(inpath("bike-1.mp4")).stream_info
bike_2 = VideoFile(inpath("bike-2.mp4")).stream_info


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


def get_splice_time_deltas():
	time_diff_list = []
	start_time = time()
	prev_time = 0
	while True:
		# Wait for user input
		inp = input("enter for next splice time. q to quit.")
		time_since_start = time() - start_time
		time_diff_list.append(time_since_start - prev_time)
		print("Time diff: {}".format(time_since_start - prev_time))
		prev_time = time_since_start
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
		zat = ZoomAndTranslateRelative(input_stream = stream_segment, intensity = 0.8)
		zat.set_effect_params(i % 9)
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

timesplice_an_effect(bike_1, "effects_timesplicer-5.mp4")


def timesplice_an_effect_with_deltas(video_stream_info, out_filename):
	splice_times = get_splice_time_deltas()
	concat_list = []
	prev_splice_time = 0.0
	for i in range(len(splice_times)):
		splice_time_delta = splice_times[i]
		stream_segment = video_stream_info.trimmed_copy(
				start=prev_splice_time,
				end=prev_splice_time + splice_time_delta
			)
		zat = ZoomAndTranslateRelative(input_stream = stream_segment, intensity = 0)
		zat.set_effect_params(i % 9)
		output_stream = zat.output_stream
		concat_list.append(
			output_stream.raw_stream
		)
		prev_splice_time = prev_splice_time + splice_time_delta + 2
	# Works!
	print("Created concat list")
	(	ffmpeg.
		concat(*concat_list).
		output(outpath(out_filename)).
		run()
	)

timesplice_an_effect_with_deltas(bike_1, "effects_timesplicer-delta-1.mp4")

# Works
def timesplice_an_effect(video_stream_info, out_filename):
	splices = get_splices_from_input()
	concat_list = []
	prev_splice_time = 0.0
	for i in range(len(splices)):
		splice_time_delta = splices[i].time_delta
		stream_segment = video_stream_info.trimmed_copy(
				start=prev_splice_time,
				end=prev_splice_time + splice_time_delta
			)
		zat = ZoomAndTranslateRelative(input_stream = stream_segment, intensity = 0)
		zat.set_effect_params(i % 9)
		output_stream = zat.output_stream
		concat_list.append(
			output_stream.raw_stream
		)
		prev_splice_time = prev_splice_time + splice_time_delta + 2
	# Works!
	print("Created concat list")
	(	ffmpeg.
		concat(*concat_list).
		output(outpath(out_filename)).
		run()
	)

timesplice_an_effect(bike_1, "effects-splice-1.mp4")

# Culeidoscope timesplice
def timesplice_an_effect(video_stream_info, out_filename):
	splices = get_splices_from_input()
	concat_list = []
	prev_splice_time = 0.0
	for i in range(len(splices)):
		splice_time_delta = splices[i].time_delta
		stream_segment = video_stream_info.trimmed_copy(
				start=prev_splice_time,
				end=prev_splice_time + splice_time_delta
			)
		cul = RandomCuleidoscope(input_stream = stream_segment)
		cul.set_effect_params(i % 9)
		output_stream = cul.output_stream
		concat_list.append(
			output_stream.raw_stream
		)
		prev_splice_time = prev_splice_time + splice_time_delta
	# Works!
	print("Created concat list")
	(	ffmpeg.
		concat(*concat_list).
		output(outpath(out_filename)).
		run()
	)
	
timesplice_an_effect(bike_1, "culeidoscope-splice-1.mp4")

# Get effect from readchar!
def timesplice_an_effect_readchar(video_stream_info, out_filename):
	splices = get_splices_from_readchar()
	concat_list = []
	# Maps a effect class name to the effect object, so a single object
	# can be used
	effect_map = {}
	prev_splice_time = 0.0
	for splice in splices:
		splice_time_delta = splice.time_delta
		stream_segment = video_stream_info.trimmed_copy(
				start=prev_splice_time,
				end=prev_splice_time + splice_time_delta
			)
		# See if effect is already used before
		if splice.effect in effect_map.keys():
			effect = effect_map[splice.effect]
			effect.input_stream = stream_segment
		else:
			# Initialize effect class with input stream
			effect = splice.effect(input_stream = stream_segment)
			# Store in dict to be used later
			effect_map[splice.effect] = effect
		getattr(effect, splice.action)()
		output_stream = effect.output_stream
		concat_list.append(
			output_stream.raw_stream
		)
		prev_splice_time = prev_splice_time + splice_time_delta
	
	print("Created concat list")
	(	ffmpeg.
		concat(*concat_list).
		output(outpath(out_filename)).
		run()
	)

timesplice_an_effect_readchar(bike_1, "drum-effects-2.mp4")

