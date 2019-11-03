from video import StreamInfo
from utils import Rectangle

def swap_rectangles(input_stream: StreamInfo, rect_1: Rectangle, rect_2: Rectangle):
	"""
	Swaps rectangles in the input stream using the swaprect filter
	:input_stream: <StreamInfo> Input stream where rectangles need to be swapped
	:rect_1:, :rect_2: <Rectangle> Rectangles that need to be swapped
	:return: <StreamInfo> output stream with swapped rectangles
	"""

	assert (rect_1.width, rect_1.height) == (rect_2.width, rect_2.height)

	raw_output_stream = (
		input_stream.raw_stream.
			filter_(filter_name = "swaprect",
				w = rect_1.width,
				h = rect_1.height,
				x1 = rect_1.top_x, 
				y1 = rect_1.top_y,
				x2 = rect_2.top_x,
				y2 = rect_2.top_y
			)
	)

	output_stream = StreamInfo(
		raw_stream=raw_output_stream,
		width=input_stream.width,
		height=input_stream.height
	)

	return output_stream