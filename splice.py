from dataclasses import dataclass
from time import time

@dataclass
class SpliceInfo():
	time_delta: float = 0
	effect_config: str = None

	def __str__(self):
		return "Splice<{}, {}>".format(self.time_delta, self.effect_config)


def get_splices_from_input():
	splice_info_list = []
	start_time = time()
	prev_time = 0
	while True:
		# Wait for user input
		inp = input("enter for next splice time. q to quit.")
		time_since_start = time() - start_time
		splice_info = SpliceInfo(time_delta=time_since_start - prev_time, effect_config=inp)
		splice_info_list.append(splice_info)
		print("Time diff: {}".format(time_since_start - prev_time))
		prev_time = time_since_start
		if(inp == "q"):
			print("Got quit request.")
			break
	return splice_info_list

