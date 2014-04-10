__author__ = 'kosttek'
import unittest
from statisticlog.logmetric import SequenceMatcher

class TestLogSequenceMatcher(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple(self):
        pass
        sentence_a = "takie zdanie 100% to samo"
        sentence_b = "takie zdanie 100% to samo"
        seq = SequenceMatcher(sentence_a,sentence_b)
        self.assertEqual(seq.ratio(),1)

    def test_onediffernece(self):
        sentence_a = "takie zdanie 80% to samo"
        sentence_b = "takie zdanie 100% to samo"
        seq = SequenceMatcher(sentence_a,sentence_b)
        self.assertEqual(seq.ratio(),0.8)

    def test_onesame(self):
        sentence_a = "takie zdanie 20% to samo"
        sentence_b = "takie pranie 100% krowa zywa"
        seq = SequenceMatcher(sentence_a,sentence_b)
        self.assertEqual(seq.ratio(),0.2)

    def test_largersentence(self):
        sentence_a = "takie zdanie 10% to samo" # 5 slow
        sentence_b = "takie pranie 100% krowa zywa jeden dwa trzy cztery piec" #10 slow
        seq = SequenceMatcher(sentence_a,sentence_b)
        self.assertEqual(seq.ratio(),0.1)

    def test_nonsame(self):
        sentence_a ="Start proc com.android.exchange for service com.android.exchange/.ExchangeService: pid= uid= gids="
        sentence_b ="Force stopping package com.android.vending uid=10058"
        seq = SequenceMatcher(sentence_a,sentence_b)
        self.assertEqual(seq.ratio(),0.0)


if __name__ == "__mian__":
    unittest.main()

