from dataclasses import dataclass
from time import time

# Internal libraries
from effect.effect import (
	VideoEffect,
)

from effect.mapping import (
	character_effect_map,
	character_action_map
)

from effect.culeidoscope.vertical_culeidoscope import VerticalCuleidoscope
from effect.culeidoscope.random_culeidoscope import RandomCuleidoscope
from effect.pass_through import PassThrough

# External libraries
from readchar import readchar

# Constants
DEFAULT_ACTION = "hihat_drum_effect"
DEFAULT_EFFECT = PassThrough

@dataclass
class SpliceInfo():
	time_delta: float = 0
	effect_config: str = None
	effect: VideoEffect = None
	action: str = "next_effect"
	time_jump: float = 0

	def __str__(self):
		return "Splice<{}, {}, jump={}>".format(self.time_delta, self.effect, self.time_jump)

	def __repr__(self):
		return str(self)


def get_splices_from_input():
	splice_info_list = []
	start_time = time()
	prev_time = 0
	while True:
		# Wait for user input
		print("Enter for next splice time. q to quit.")
		inp = input()
		time_since_start = time() - start_time
		splice_info = SpliceInfo(
			time_delta=time_since_start - prev_time, 
			effect_config=inp,
		)
		splice_info_list.append(splice_info)
		print("Time diff: {}".format(time_since_start - prev_time))
		prev_time = time_since_start
		if(inp == "q"):
			print("Got quit request.")
			break
	return splice_info_list

def get_time_jump(inp_char):
	if inp_char == "t":
		return 1
	elif inp_char == "y":
		return 0.5
	else:
		return 0

def get_splices_from_readchar():
	splice_info_list = []
	print("Enter video splice data. Enter to start:")
	input()
	start_time = time()
	prev_time = 0

	current_effect = DEFAULT_EFFECT
	current_action = DEFAULT_ACTION
	while True:
		# Wait for user input
		inp = readchar()
		time_since_start = time() - start_time

		if inp in character_effect_map.keys():
			current_effect = character_effect_map[inp]
			current_action = DEFAULT_ACTION
		elif inp in character_action_map.keys():
			current_action = character_action_map[inp]

		splice_info = SpliceInfo(
			time_delta = time_since_start - prev_time,
			effect_config = inp,
			effect = current_effect,
			action = current_action,
			time_jump = get_time_jump(inp)
		)
		splice_info_list.append(splice_info)
		print("Time diff: {}".format(time_since_start - prev_time))
		prev_time = time_since_start
		if(inp == "q"):
			print("Got quit request.")
			break
	print("Splice list: {}", splice_info_list)
	return splice_info_list

