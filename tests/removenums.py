import datetime

__author__ = 'kosttek'
import unittest
from statisticlog.compresslog import CompressLog

class TestRemoveNums(unittest.TestCase):
    def setUp(self):
        pass

    def test_remove_nums(self):
        compres = CompressLog()
        result = compres.removeNumsBiggerThanTwoDigits("ala021todo")
        self.assertEqual(result,"alatodo")

        result = compres.removeNumsBiggerThanTwoDigits("ala1todo")
        self.assertEqual(result,"ala1todo")