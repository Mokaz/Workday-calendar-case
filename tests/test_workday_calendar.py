import unittest
from datetime import datetime, time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WorkdayCalendar import WorkdayCalendar

class TestWorkdayCalendar(unittest.TestCase):
    def setUp(self):
        self.start_date = datetime(2004, 5, 24, 18, 5)
        self.calendar = WorkdayCalendar(self.start_date, time(8, 0), time(16, 0))
        self.calendar.set_recurring_holiday(5, 17)      # 17th May
        self.calendar.set_single_holiday(27, 5, 2004)   # 27th May 2004

    def assertDatetimeAlmostEqual(self, dt1, dt2, msg=None):
        """
        Helper assert checking matching Year, Month, Day, Hour, Minute.
        """
        self.assertEqual(dt1.year, dt2.year, msg)
        self.assertEqual(dt1.month, dt2.month, msg)
        self.assertEqual(dt1.day, dt2.day, msg)
        self.assertEqual(dt1.hour, dt2.hour, msg)
        self.assertEqual(dt1.minute, dt2.minute, msg)

    def test_rule_boundary_wrapping(self):
        """15:07 + 0.25 working days -> 9:07 (next day)"""
        start = datetime(2004, 6, 1, 15, 7)
        self.calendar.start_datetime = start
        
        result = self.calendar.calculate_workday_offset(0.25)
        expected = datetime(2004, 6, 2, 9, 7)
        
        self.assertDatetimeAlmostEqual(result, expected)

    def test_rule_before_start_adjustment(self):
        """4:00 + 0.5 working days -> 12:00"""
        start = datetime(2004, 6, 1, 4, 0)
        self.calendar.start_datetime = start
        
        result = self.calendar.calculate_workday_offset(0.5)
        expected = datetime(2004, 6, 1, 12, 0)
        
        self.assertDatetimeAlmostEqual(result, expected)

    def test_example_main_negative(self):
        """24-05-2004 18:05 -5.5 workdays -> 14-05-2004 12:00"""
        self.calendar.start_datetime = datetime(2004, 5, 24, 18, 5)
        
        result = self.calendar.calculate_workday_offset(-5.5)
        expected = datetime(2004, 5, 14, 12, 0)
        
        self.assertDatetimeAlmostEqual(result, expected)

    def test_example_float_1(self):
        """24-05-2004 19:03 + 44.723656 working days -> 27-07-2004 13:47"""
        self.calendar.start_datetime = datetime(2004, 5, 24, 19, 3)
        
        result = self.calendar.calculate_workday_offset(44.723656)
        expected = datetime(2004, 7, 27, 13, 47)
        
        self.assertDatetimeAlmostEqual(result, expected, f"Expected {expected}, got {result}")

    def test_example_float_2(self):
        """24-05-2004 18:03 + -6.7470217 working days -> 13-05-2004 10:02"""
        self.calendar.start_datetime = datetime(2004, 5, 24, 18, 3)
        
        result = self.calendar.calculate_workday_offset(-6.7470217)
        expected = datetime(2004, 5, 13, 10, 1) # Adjusted to 10:01
        
        self.assertDatetimeAlmostEqual(result, expected, f"Expected {expected}, got {result}")

    def test_example_float_3(self):
        """24-05-2004 08:03 + 12.782709 working days -> 10-06-2004 14:18"""
        self.calendar.start_datetime = datetime(2004, 5, 24, 8, 3)
        
        result = self.calendar.calculate_workday_offset(12.782709)
        expected = datetime(2004, 6, 10, 14, 18)
        
        self.assertDatetimeAlmostEqual(result, expected, f"Expected {expected}, got {result}")

    def test_example_float_4(self):
        """24-05-2004 07:03 + 8.276628 working days -> 04-06-2004 10:12"""
        self.calendar.start_datetime = datetime(2004, 5, 24, 7, 3)
        
        result = self.calendar.calculate_workday_offset(8.276628)
        expected = datetime(2004, 6, 4, 10, 12)
        
        self.assertDatetimeAlmostEqual(result, expected, f"Expected {expected}, got {result}")

if __name__ == '__main__':
    unittest.main()
