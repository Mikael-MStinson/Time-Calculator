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
	return round(total_time,2)

	
def add_hours_to_time(time, hours):
	hours *= 100
	minutes = (hours % 100)
	hours -= minutes 
	minutes *= (6/10)#by this point, hours has the hour element, and minutes has the minute element
	time_minutes = time % 100
	while time_minutes + minutes > 59:
		minutes -= 60
		hours += 100
	hours = hours + minutes 
	if time + hours > 1259:
		return int(time + hours - 1200)
	return int(time + hours)


def combine_and_deduct_time_entries(time_entries):
	entry = token_times_from_string(time_entries)
	if entry == []:
		raise Exception("Please enter a time")
	start_time = entry[0]
	total_time =  parse_times(entry)
	deductable_time = parse_times(entry, match_type = False)
	end_time = add_hours_to_time(start_time, total_time)
	return start_time, end_time, deductable_time, round(total_time-deductable_time,2)

	
if __name__ == "__main__":
	while True:
		try:
			time_entries = input(">")
			time_values = combine_and_deduct_time_entries(time_entries)
			print("start time: {}, end time: {}, deduct: {}, total: {}".format(*time_values))
			
		except Exception as e:
			print(e)