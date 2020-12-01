from main import calculate_time
from main import token_times_from_string
from main import UnknownTokenError
from main import parse_times
from main import add_hours_to_time
from main import combine_and_deduct_time_entries
from unittest import TestCase

class TestCalculateTime(TestCase):
	def test_one_hour(self):
		self.assertEqual(calculate_time(900,1000), 1)
	 
	def test_two_hours(self):
		self.assertEqual(calculate_time(900,1100), 2)
		
	def test_half_hour(self):
		self.assertEqual(calculate_time(900,930), 0.5)
		
	def test_two_hours_over_noon(self):
		self.assertEqual(calculate_time(1100,100), 2)
		
	def test_one_hour_offset(self):
		self.assertEqual(calculate_time(930,1030), 1)
		
	def test_seven_hours(self):
		self.assertEqual(calculate_time(800,300), 7)
		
	def test_odd_hours(self):
		self.assertAlmostEqual(calculate_time(1011,1042), 0.5166666666666663)
		
class TestTokenTimesFromString(TestCase):
	def test_no_time_block(self):
		self.assertEqual(token_times_from_string(""),[])
	
	def test_one_time_block(self):
		self.assertEqual(token_times_from_string("900 on 1000"),[900, True, 1000])
		
	def test_multiple_successive_time_blocks(self):
		self.assertEqual(token_times_from_string("900 on 1000 off 1100"),[900, True, 1000, False, 1100])
	
	def test_multiple_broken_time_blocks(self):
		self.assertEqual(token_times_from_string("900 on 1000 off 1100 1200 on 100"),[900, True, 1000, False, 1100, 1200, True, 100])
		
	def test_invalid_toke(self):
		self.assertRaises(UnknownTokenError, token_times_from_string, "900 on 1000 off hello 1100")
		
class TestParseTimes(TestCase):
	def test_no_times_matching_all(self):
		self.assertEqual(parse_times([]), 0)
	
	def test_one_times_matching_all(self):
		self.assertEqual(parse_times([900, True, 1000]), 1)
		
	def test_two_successive_times_matching_all(self):
		self.assertEqual(parse_times([900, True, 1000, True, 1100]), 2)
		
	def test_three_successive_times_matching_all(self):
		self.assertEqual(parse_times([900, True, 1000, True, 1100, True, 100]), 4)
		
	def test_two_broken_times_matching_all(self):
		self.assertEqual(parse_times([900, True, 1000, 1100, True, 1200]), 2)
	
	def test_three_successive_times_and_two_broken_times_matching_all(self):
		self.assertEqual(parse_times([900, True, 1000, True, 1100, True, 100, 200, True, 300, 400, True, 500]), 6)
		
	def test_three_successive_times_with_one_discounted_matching_all(self):
		self.assertEqual(parse_times([900, True, 1000, False, 1100, True, 100]), 4)
		
	def test_three_successive_times_with_one_discounted_matching_true(self):
		self.assertEqual(parse_times([900, True, 1000, False, 1100, True, 100], match_type = True), 3)
		
	def test_three_successive_times_with_one_discounted_matching_false(self):
		self.assertEqual(parse_times([900, True, 1000, False, 1100, True, 100], match_type = False), 1)
		
class TestAddHoursToTime(TestCase):	
	def test_add_zero_hours_to_time(self):
		self.assertEqual(add_hours_to_time(1000,0), 1000)
		
	def test_add_one_hour_to_time(self):
		self.assertEqual(add_hours_to_time(1000,1), 1100)

	def test_add_one_hour_to_time_over_noon(self):
		self.assertEqual(add_hours_to_time(1200,1), 100)
	
	def test_add_half_hour_to_time(self):
		self.assertEqual(add_hours_to_time(1000,0.5), 1030)
	
	def test_add_half_hour_to_time_over_noon(self):
		self.assertEqual(add_hours_to_time(1200,0.5), 1230)
		
	def test_add_one_hour_to_time_over_noon_from_half_hour(self):
		self.assertEqual(add_hours_to_time(1230,1), 130)
		
	def test_faulty_addition_1(self):
		self.assertEqual(add_hours_to_time(945,1.7), 1127.0)
		
	def test_faulty_addition_2(self):
		self.assertEqual(add_hours_to_time(202,0.64), 241)
		
class TestCombineAndDeductTimeEntries(TestCase):
	def test_no_time_entries(self):
		self.assertRaises(Exception, combine_and_deduct_time_entries, "")
		
	def test_one_time_entry(self):
		self.assertEqual(combine_and_deduct_time_entries("1000 on 1100"),(1000,1100,0.0,1.0))
		
	def test_consecutive_time_entries(self):
		self.assertEqual(combine_and_deduct_time_entries("1000 on 1100 off 100 on 200"),(1000,200,2.0,2.0))
	
	def test_non_consecutive_time_entries(self):
		self.assertEqual(combine_and_deduct_time_entries("1000 on 1100 off 100 on 200 300 on 430"),(1000,330,2.0,3.5))
	
	def test_bug_1(self):
		'''End time is invalid hour values'''
		self.assertEqual(combine_and_deduct_time_entries("945 off 1016 on 1112 1234 on 1249"),(945,1127,0.52,1.18))
	
	def test_bug_2(self):
		'''Actual Hours Discrepancy'''
		self.assertEqual(combine_and_deduct_time_entries("1112 off 1124 on 1155 off 1215 1249 on 1258"),(1112,1224,0.53,0.67))
		
	def test_bug_3(self): 
		'''End time of consecutive time entries does not line up'''
		self.assertEqual(combine_and_deduct_time_entries("202 off 217 on 225 off 239 on 241"),(202,241,0.48,0.17)) #connectwise is saying 0.17 for actual time: 0.133333 + 0.03333333