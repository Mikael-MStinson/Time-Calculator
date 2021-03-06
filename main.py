import re
import math

class Timestamp:
	def __init__(self, timestamp):
		_timestamp = timestamp
		if type(_timestamp) in [str, float]:
			_timestamp = int(_timestamp)
		if type(_timestamp) != int:
			raise TypeError("Timestamp argument must by type int or str, not type {}".format(type(timestamp)))
		if _timestamp < 100 or _timestamp > 1259:
			raise ValueError("{} is not an acceptable time".format(_timestamp))
		self.hour = int(_timestamp/100)
		self.minute = _timestamp%100
	
	def __repr__(self):
		return "{}{:02d}".format(self.hour,self.minute)
		
	def time(self):
		return self.hour * 100 + self.minute
	
	def __add__(self, hours):
		''' adds n number of hours to a timestamp '''
		hours_offset = hours
		hours_offset *= 100
		minutes = (hours_offset % 100)
		hours_offset -= minutes 
		minutes = math.ceil(minutes * (6/10))
		while self.minute + minutes > 59:
			minutes -= 60
			hours_offset += 100
		hours_offset = hours_offset + minutes 
		if self.hour * 100 + self.minute + hours_offset > 1259:
			return Timestamp(self.hour * 100 + self.minute + hours_offset - 1200)
		return Timestamp(self.hour * 100 + self.minute + hours_offset)
		
	def __sub__(self, other):
		''' returns the difference between two timestamps in hours '''
		# sub the hours
		hour = self.hour - other.hour
		if hour < 0:
			hour += 12
		# sub the minutes
		minute = self.minute - other.minute
		if minute < 0:
			minute += 60
			hour -= 1
		minute *= 10/6
		return hour + (minute/100)
		

class TimeBlock:
	def __init__(self, start, end, billable):
		self.start = start
		self.end = end
		self.billable = billable
		
	def hours(self, billable = None):
		if billable == None or self.billable == billable:
			return self.end-self.start
		else:
			return 0
				
	
def tokenize_times_from_string(string):
	if string == "":
		return []
	int_pattern = re.compile(r"\d{3,4}")
	tokens = []
	items = string.split(" ")
	for item in items:
		if item == "on":
			tokens.append(True)
		elif item == "off":
			tokens.append(False)
		elif int_pattern.search(item) != None:
			tokens.append(Timestamp(item))
		else:
			raise UnknownTokenError("{} is not a recognizable token".format(item))
	return tokens
	
	
class UnknownTokenError(Exception):
	pass
	
	
def parse_times_from_tokens(tokens):
	if tokens == []: return []
	blocks = []
	index = 0
	while index < len(tokens) - 2:
		if type(tokens[index]) == Timestamp and type(tokens[index+1]) == bool and type(tokens[index+2]) == Timestamp:
				blocks.append(TimeBlock(tokens[index], tokens[index+2], tokens[index+1]))
		index += 1
	return blocks


def add_blocks(blocks, billable=None):
	hours = 0
	for block in blocks:
		hours += block.hours(billable)
	return round(hours,2)

def combine_and_deduct_time_entries(time_entries):
	tokens = tokenize_times_from_string(time_entries)
	blocks = parse_times_from_tokens(tokens)
	if blocks == []:
		raise Exception("Please enter a time")
	start_time = blocks[0].start
	total_time =  add_blocks(blocks)
	deductable_time = add_blocks(blocks, billable =  False)
	end_time = start_time + total_time
	return start_time.time(), end_time.time(), deductable_time, round(total_time-deductable_time,2)

	
if __name__ == "__main__":
	while True:
		try:
			time_entries = input(">")
			time_values = combine_and_deduct_time_entries(time_entries)
			print("start time: {}, end time: {}, deduct: {}, total: {}".format(*time_values))
			
		except Exception as e:
			print(e)