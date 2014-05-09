import datetime

__author__ = 'kosttek'
import unittest
from statisticlog.compresslog import CompressLog

class TestParseLogs(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_log(self):
        log1 = "03-28 15:43:19.225 W/ActivityManager(  341): Unable to start service Intent { cmp=com.aware/.Applications }: not found"

        cl = CompressLog()
        [tag,log,date] = cl.parseLog(log1)


        self.assertEqual(tag,"W/ActivityManager")
        self.assertEqual(log," Unable to start service Intent { cmp=com.aware/.Applications }: not found")

        assert_date = datetime.datetime(2014,int(3),int(28),int(15),int(43),int(19),int(225))
        self.assertEqual(date,assert_date)

    def test_parse_log_tagspaces(self):
        log1 = "03-28 15:43:19.225 W/Activity    (  341): Unable to start service Intent { cmp=com.aware/.Applications }: not found"

        cl = CompressLog()
        [tag,log,date] = cl.parseLog(log1)


        self.assertEqual(tag,"W/Activity")
        self.assertEqual(log," Unable to start service Intent { cmp=com.aware/.Applications }: not found")




    def test_parse_log_with_colon(self):
        log1 = "03-28 15:43:19.225 E/AWARE:HTML   (  341): Unable to start service Intent { cmp=com.aware/.Applications }: not found"

        cl = CompressLog()
        [tag,log,date] = cl.parseLog(log1)


        self.assertEqual(tag,"E/AWARE:HTML")
        self.assertEqual(log," Unable to start service Intent { cmp=com.aware/.Applications }: not found")

        assert_date = datetime.datetime(2014,int(3),int(28),int(15),int(43),int(19),int(225))
        self.assertEqual(date,assert_date)

