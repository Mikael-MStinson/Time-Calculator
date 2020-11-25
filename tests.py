from main import calculate_time
from main import token_times_from_string
from main import UnknownTokenError
from main import parse_times
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
		self.assertEqual(calculate_time(1011,1042), 0.52)
		
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