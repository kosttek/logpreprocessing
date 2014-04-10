__author__ = 'kosttek'
#test difflib
import difflib


if __name__ == "__main__":

    print "test"
    a ="Start proc com.android.email for broadcast com.android.email/.service.EmailBroadcastReceiver: \
pid= uid= gids="
    b ="Start proc com.android.exchange for service com.android.exchange/.ExchangeService: pid= uid\
= gids="
    c ="Force stopping package com.android.vending uid=10058"

    seq=difflib.SequenceMatcher(a=a.lower(), b=b.lower())
    print seq.ratio()

    seq2=difflib.SequenceMatcher(a=a.lower(), b=c.lower())
    print seq2.ratio()