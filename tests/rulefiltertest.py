__author__ = 'kosttek'
import unittest
from rulesengine.parsefacts import ParseFacts
from rulesengine.rulesengine import RuleEngine
from statisticlog.databaseSchema import Tag, CompressedLog, RawLog
import datetime

class TestRuleFilter(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple(self):
        ps = ParseFacts()
        ps.parseLine("extend(\"compressed @@@\")")


        rl = RuleEngine()
        rl.initFactsDict(ps)

        clog1 = CompressedLog("compressed @@@")
        clog1.setDiffWordsSet({1})

        clog2 = CompressedLog("compressed2 @@@")
        clog2.setDiffWordsSet({1})

        rawlog1 = RawLog(date=datetime.datetime.now(),log="compressed a")
        rawlog2 = RawLog(date=datetime.datetime.now(),log="compressed b")
        rawlog3 = RawLog(date=datetime.datetime.now(),log="compressed2 a")
        rawlog4 = RawLog(date=datetime.datetime.now(),log="compressed2 b")

        clog1.rawlogs.append(rawlog1)
        clog1.rawlogs.append(rawlog2)

        clog2.rawlogs.append(rawlog3)
        clog2.rawlogs.append(rawlog4)

        [date1,logmessage1] = rl.filterLog(rawlog1)
        [date2,logmessage2] = rl.filterLog(rawlog2)
        [date3,logmessage3] = rl.filterLog(rawlog3)
        [date4,logmessage4] = rl.filterLog(rawlog4)

        self.assertEqual("compressed a",logmessage1)
        self.assertEqual("compressed b",logmessage2)
        self.assertEqual("compressed2 @@@",logmessage3)
        self.assertEqual("compressed2 @@@",logmessage4)

