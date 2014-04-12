__author__ = 'kosttek'
import unittest
from rulesengine.parsefacts import ParseFacts

class TestParseFacts(unittest.TestCase):
    def setUp(self):
        pass

    def test_QmarkInedxes(self):
        ps = ParseFacts()
        indexes = ps.findWithOutSpecialQuestionMarks("\"arg1\",\"arg2 this is\\\"not funny\\\"\"")
        self.assertEqual(indexes,[0,5,7,33])

    def test_parsing_simple(self):
        pf = ParseFacts()
        pf.parseLine("extend(\"lol kind of shit\", \"arg nr 1\", \"arg nr 2\")")
        fact = pf.knowledgelist[0]
        self.assertEqual(fact.factname,"extend")
        self.assertEqual(fact.arglist[0],"lol kind of shit")
        self.assertEqual(fact.arglist[1],"arg nr 1")
        self.assertEqual(fact.arglist[2],"arg nr 2")
