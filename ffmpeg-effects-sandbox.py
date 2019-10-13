# Core python #
import os

# External #
import ffmpeg

# Library
from video import VideoFile

# Constants #
IN_VIDEO_DIR 	= "raw-video"
OUT_VIDEO_DIR	= "processed-video"

def inpath(video_path):
	return os.path.join(IN_VIDEO_DIR, video_path)

def outpath(video_path):
	return os.path.join(OUT_VIDEO_DIR, video_path)

universe_vid = VideoFile(inpath("universe-footage.mp4"))
bridge_vid = VideoFile(inpath("wooden-bridge.mp4"))
sun_vid = VideoFile(inpath("transit.mov"))

hector_1 = VideoFile(inpath("hector-vertical-1.mp4"))
hector_2 = VideoFile(inpath("hector-vertical-2.mp4"))

bike_1 = VideoFile(inpath("bike-1.mp4"))
bike_2 = VideoFile(inpath("bike-2.mp4"))

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
	concat(universe_vid.stream()).
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
		*[bike_1.stream().trim(start_frame=0, end_frame=20),
		bike_2.stream().trim(start_frame=0, end_frame=50),
		bike_1.stream().trim(start_frame=20, end_frame=40),
		bike_2.stream().trim(start_frame=50, end_frame=100),
		bike_1.stream().trim(start_frame=40, end_frame=60),
		bike_2.stream().trim(start_frame=100, end_frame=200)]).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("concat-try-2.mp4")).
	run()
)

# Try the above, but only using the first 2 segments to see if I'm calling something
# incorrectly
(
	ffmpeg.
	concat(
		*[bike_1.stream().trim(start_frame=0, end_frame=50),
		bike_1.stream().trim(start_frame=100, end_frame=150),
		bike_1.stream().trim(start_frame=200, end_frame=250),
		bike_1.stream().trim(start_frame=300, end_frame=350),
		bike_1.stream().trim(start_frame=400, end_frame=450)]).
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
		*[bike_1.stream().trim(start_frame=0, end_frame=100).setpts("PTS-STARTPTS"),
		bike_2.stream().trim(start_frame=0, end_frame=100).setpts("PTS-STARTPTS"),
		bike_1.stream().trim(start_frame=100, end_frame=200).setpts("PTS-STARTPTS"),
		bike_2.stream().trim(start_frame=100, end_frame=200).setpts("PTS-STARTPTS"),
		bike_1.stream().trim(start_frame=200, end_frame=300).setpts("PTS-STARTPTS"),
		bike_2.stream().trim(start_frame=200, end_frame=300).setpts("PTS-STARTPTS")]).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("concat-try-5.mp4")).
	run()
)

# Concat in a loop
concat_list = []
for i in range(20):
	concat_list.append(bike_1.stream().trim(start_frame=i*100, end_frame=(i*100 + 100)).setpts("PTS-STARTPTS"))
	concat_list.append(bike_2.stream().trim(start_frame=i*100, end_frame=(i*100 + 100)).setpts("PTS-STARTPTS"))

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
	sun_vid.stream().
	filter_("pad", width=1000, height=700, x=50, y=50).
	output(outpath("pad-1.mp4")).
	run()
)

# Scale
(
	sun_vid.stream().
	filter_("scale", width=200, height=150).
	filter_("pad", width=1000, height=700, x=50, y=50).
	output(outpath("scale-2.mp4")).
	run()
)


# Crop
(
	sun_vid.stream().
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
		bike_1.stream().trim(start_frame=0, end_frame=100).setpts("PTS-STARTPTS").
		crop(x=0, y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),
		bike_2.stream().trim(start_frame=0, end_frame=100).setpts("PTS-STARTPTS").
		crop(x=0, y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),
		bike_1.stream().trim(start_frame=100, end_frame=200).setpts("PTS-STARTPTS").
		crop(x=int(bike_1.width/3), y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),
		bike_2.stream().trim(start_frame=100, end_frame=200).setpts("PTS-STARTPTS").
		crop(x=int(bike_1.width/3), y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),
		bike_1.stream().trim(start_frame=200, end_frame=300).setpts("PTS-STARTPTS").
		crop(x=int(2*bike_1.width/3), y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),
		bike_2.stream().trim(start_frame=200, end_frame=300).setpts("PTS-STARTPTS").
		crop(x=int(2*bike_1.width/3), y=0, width=int(bike_1.width/3), height=int(bike_1.height/3)),
		]
	).
	filter_("pad", width=bike_1.width, height=bike_1.height, x=bike_1.width/3, y=bike_1.height/3).
	drawtext(text="the concatenation", x=100, y=100, fontsize=25).
	output(outpath("crop-pad-1.mp4")).
	run()
)


