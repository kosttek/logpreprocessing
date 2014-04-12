__author__ = 'kosttek'
class Fact():
    def __init__(self,factname,arglist):
        self.factname = factname
        self.arglist  = arglist
        self.target = arglist[0]