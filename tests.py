from main import UnknownTokenError
from main import combine_and_deduct_time_entries
from main import Timestamp
from unittest import TestCase
		
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
		
	def test_bug_4(self):
		self.assertEqual(combine_and_deduct_time_entries("1110 off 1132 on 1217 off 1235 on 1254"),(1110,1254,0.67,1.06))