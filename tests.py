from main import calculate_time
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
