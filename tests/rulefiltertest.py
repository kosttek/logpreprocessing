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

    def test_regexp(self):
        ps = ParseFacts()
        ps.parseLine("default(\"remove\")")
        ps.parseLine("clogregexp(\" Start proc.*\")")

        rl = RuleEngine()
        rl.initFactsDict(ps)

        clog_false_str = " End pro @@@ @@@"
        clog_true_str = " Start proc @@@ @@@"

        rawlog_false = self.create_log_and_clog(" End pro blabla bla", clog_false_str,[3,4])
        rawlog_true = self.create_log_and_clog(" Start proc blabla bla",  clog_true_str,[3,4])

        none_result = rl.filterLog(rawlog_false)
        [date2,logmessage_true] = rl.filterLog(rawlog_true)

        self.assertEqual(None,none_result)
        self.assertEqual(logmessage_true,logmessage_true)



    def create_log_and_clog(self, log, clog_str, diff_words_arr, date=datetime.datetime.now()):
        rawlog = RawLog(date, log)
        clog1 = CompressedLog(clog_str)
        clog1.setDiffWordsSet(diff_words_arr)
        clog1.rawlogs.append(rawlog)
        return rawlog


