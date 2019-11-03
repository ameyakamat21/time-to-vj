# Core python #
import os

# External #
import ffmpeg

# Library
from video import (
	VideoFile,
	StreamInfo
)

from effect.zoom_and_translate import ZoomAndTranslateRelative
from effect.culeidoscope.random_culeidoscope import RandomCuleidoscope
from effect.culeidoscope.vertical_culeidoscope import VerticalCuleidoscope

# Constants #
IN_VIDEO_DIR 	= "raw-video"
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
bike_1_dup = VideoFile(inpath("bike-1.mp4")).stream_info
bike_2 = VideoFile(inpath("bike-2.mp4")).stream_info

###

# universe_vid = ffmpeg.input(inpath("universe-footage.mp4"))
# bridge_vid = ffmpeg.input(inpath("wooden-bridge.mp4"))
# sun_vid = ffmpeg.input(inpath("transit.mov"))

# hector_1 = ffmpeg.input(inpath("hector-vertical-1.mp4"))
# hector_2 = ffmpeg.input(inpath("hector-vertical-2.mp4"))

# bike_1 = ffmpeg.input(inpath("bike-vertical-1.mp4"))
# bike_2 = ffmpeg.input(inpath("bike-vertical-2.mp4"))

# Overlay
(
	ffmpeg.
	concat(universe_vid.raw_stream.
	overlay(sun_vid, x=0, y=0).
	overlay(bridge_vid, x=500, y=100).
	output(outpath("overlay-try-2.mp4")).
	run()
)


# Concat #

# After the first 2 segments, this produces lag for some reason
(
	ffmpeg.
	concat(
		*[bike_1.raw_stream.trim(start_frame=0, end_frame=20),
		bike_2.raw_stream.trim(start_frame=0, end_frame=50),
		bike_1.raw_stream.trim(start_frame=20, end_frame=40),
		bike_2.raw_stream.trim(start_frame=50, end_frame=100),
		bike_1.raw_stream.trim(start_frame=40, end_frame=60),
		bike_2.raw_stream.trim(start_frame=100, end_frame=200)]).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("concat-try-2.mp4")).
	run()
)

# Try the above, but only using the first 2 segments to see if I'm calling something
# incorrectly
(
	ffmpeg.
	concat(
		*[bike_1.raw_stream.trim(start_frame=0, end_frame=50),
		bike_1.raw_stream.trim(start_frame=100, end_frame=150),
		bike_1.raw_stream.trim(start_frame=200, end_frame=250),
		bike_1.raw_stream.trim(start_frame=300, end_frame=350),
		bike_1.raw_stream.trim(start_frame=400, end_frame=450)]).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("concat-try-3.mp4")).
	run()
)


# I see this post describing using setpts in a similar trim/concat operation: 
# https://superuser.com/questions/1064184/trimming-and-joining-media-files-using-ffmpeg

## Working copy baby! ##
(
	ffmpeg.
	concat(
		*[bike_1.raw_stream.trim(start_frame=0, end_frame=100).setpts("PTS-STARTPTS"),
		bike_2.raw_stream.trim(start_frame=0, end_frame=100).setpts("PTS-STARTPTS"),
		bike_1.raw_stream.trim(start_frame=100, end_frame=200).setpts("PTS-STARTPTS"),
		bike_2.raw_stream.trim(start_frame=100, end_frame=200).setpts("PTS-STARTPTS"),
		bike_1.raw_stream.trim(start_frame=200, end_frame=300).setpts("PTS-STARTPTS"),
		bike_2.raw_stream.trim(start_frame=200, end_frame=300).setpts("PTS-STARTPTS")]).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("concat-try-5.mp4")).
	run()
)

# Concat in a loop
concat_list = []
for i in range(20):
	concat_list.append(bike_1.raw_stream.trim(start_frame=i*100, end_frame=(i*100 + 100)).setpts("PTS-STARTPTS"))
	concat_list.append(bike_2.raw_stream.trim(start_frame=i*100, end_frame=(i*100 + 100)).setpts("PTS-STARTPTS"))

print("Created concat list")

(	ffmpeg.
	concat(*concat_list).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("concat-try-6.mp4")).
	run()
)


# Pad
# Width and height are the total dimensions of the output
(
	sun_vid.raw_stream.
	filter_("pad", width=1000, height=700, x=50, y=50).
	output(outpath("pad-1.mp4")).
	run()
)

# Scale
(
	sun_vid.raw_stream.
	filter_("scale", width=200, height=150).
	filter_("pad", width=1000, height=700, x=50, y=50).
	output(outpath("scale-2.mp4")).
	run()
)


# Crop
(
	sun_vid.raw_stream.
	crop(x=int(sun_vid.width/2), y=int(sun_vid.height/2), width=int(sun_vid.width/2), height=int(sun_vid.height/2)).
	# filter_("pad", width=int(sun_vid.width/3), height=int(sun_vid.width/3), x=50, y=50).
	output(outpath("crop-1.mp4")).
	run()
)


# Crop, concat, pad
(
	ffmpeg.
	concat(
		*[
		bike_1.raw_stream.trim(start_frame=0, end_frame=100).setpts("PTS-STARTPTS").
			crop(x=0, y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),

		bike_2.raw_stream.trim(start_frame=0, end_frame=100).setpts("PTS-STARTPTS").
			crop(x=0, y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),

		bike_1.raw_stream.trim(start_frame=100, end_frame=200).setpts("PTS-STARTPTS").
			crop(x=int(bike_1.width/3), y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),

		bike_2.raw_stream.trim(start_frame=100, end_frame=200).setpts("PTS-STARTPTS").
			crop(x=int(bike_1.width/3), y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),

		bike_1.raw_stream.trim(start_frame=200, end_frame=300).setpts("PTS-STARTPTS").
			crop(x=int(2*bike_1.width/3), y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),

		bike_2.raw_stream.trim(start_frame=200, end_frame=300).setpts("PTS-STARTPTS").
			crop(x=int(2*bike_1.width/3), y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),
		]
	).
	filter_("pad", width=bike_1.width, height=bike_1.height, x=bike_1.width/3, y=bike_1.height/3).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("crop-pad-3.mp4")).
	run()
)

# Totally broken out working example - pad and scale
original_stream = sun_vid.stream

scaled_stream = original_stream.filter_("scale", width=200, height=150)

padded_stream = original_stream.filter_("pad", width=1000, height=700, x=50, y=50)

scaled_padded_stream = scaled_stream.filter_("pad", width=1000, height=700, x=50, y=50)

final_stream = scaled_padded_stream.output(outpath("breakdown-1.mp4"))

final_raw_stream.run()


# Using VideoEffect local library!
# bike_1.trimmed_copy(start_frame=0, end_frame=500)

zat = ZoomAndTranslateRelative(input_stream = bike_1.trimmed_copy(start_frame=100, end_frame=300))
zat.enable_effect()
zat.set_effect_params(0)
output_stream = zat.output_stream
output_stream.raw_stream.output(outpath("trimmed-copy-2.mp4")).run()

# Try specifying time instead of frame number

zat = ZoomAndTranslateRelative(input_stream = bike_1.trimmed_copy(start=10, end=20.33333))
zat.enable_effect()
zat.set_effect_params(0)
output_stream = zat.output_stream
output_stream.raw_stream.output(outpath("timed-trim-1.mp4")).run()

# Introducing the bi-player

# Crop
bot_stream = (
	bike_1.
	trimmed_copy(start=10, end=20.33333).raw_stream.
	crop(
		x=int(bike_1.width/4), 
		y=0, 
		width=int(bike_1.width/2), 
		height=int(bike_1.height/2)
	)
)

top_stream = (
	bike_2.
	trimmed_copy(start=10, end=20.33333).raw_stream.
	crop(
		x=int(bike_1.width/4), 
		y=int(bike_1.height/2), 
		width=int(bike_1.width/2), 
		height=int(bike_1.height/2)
	)
) 

(
	top_stream.
		filter_(
			filter_name = "pad", 
			width = bike_1.width,
			height = bike_1.height, 
			x = int(bike_1.width/4), 
			y = 0
		).
		overlay(
			overlay_parent_node=bot_stream, 
			x=int(bike_1.width/4), 
			y=int(bike_1.height/2)
		).
		output(outpath("biplayer-1.mp4")).
		run()
)


# Seeing what split() does
zat = ZoomAndTranslateRelative(input_stream = bike_1.trimmed_copy(start=10, end=20.33333))
zat.set_effect_params(0)
output_stream = zat.output_stream
output_stream.raw_stream.split().stream().output(outpath("timed-trim-1.mp4")).run()


# Swaprect
(
	bike_1.
		trimmed_copy(start=10, end=20.33333).raw_stream.
		filter_(filter_name = "swaprect",
			w = int(bike_1.width / 2),
			h = int(bike_1.height / 2),
			x1 = 0, 
			y1 = 0,
			x2 = int(bike_1.width / 2),
			y2 = int(bike_1.height / 2)
		).
		output(outpath("swaprect-1.mp4")).
		run()
)

# RandomCuleidoscope
# Swaprect

culeidoscope_bike = RandomCuleidoscope(input_stream = bike_2.trimmed_copy(start=0, end=60))
culeidoscope_bike.set_effect_params(0)
culeidoscope_bike.output_stream.raw_stream.output(outpath("RandomCuleidoscope-3.mp4")).run()


vculeidoscope_bike = VerticalCuleidoscope(input_stream = bike_1.trimmed_copy(start=0, end=10))
vculeidoscope_bike.set_effect_params(vband_width_ratio=0.2, vband_spacing_ratio=0.2)
vculeidoscope_bike.output_stream.raw_stream.output(outpath("vculeidoscope.mp4")).run()

# test getattr
