import re

def calculate_time(start,end):
	if end < start:
		end += 1200
	#slope = 10/6 
	start_minute = start%100
	end_minute = end%100
	start = start - start_minute + (start_minute * (10/6))
	end = end - end_minute + (end_minute * (10/6))
	return round((end-start)/100,2)
	
def token_times_from_string(string):
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
			tokens.append(int(item))
		else:
			raise UnknownTokenError("{} is not a recognizable token".format(item))
	return tokens
	
	
class UnknownTokenError(Exception):
	pass
	
	
def parse_times(tokens, match_type = None):
	if tokens == []: return 0
	total_time = 0
	index = 0
	start_time = None
	while index < len(tokens):
		if type(tokens[index]) == bool:
			start_time = tokens[index-1]
		if type(tokens[index]) == int:
			if start_time == None: start_time = tokens[index]
			else: 
				if match_type == None or tokens[index-1] == match_type:
					total_time += calculate_time(start_time,tokens[index])
				start_time = None
		index += 1
	return total_time
	
