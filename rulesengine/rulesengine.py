__author__ = 'kosttek'

from parsefacts import  ParseFacts
class RuleEngine():

    def __init__(self):
        ''' factname -> list of facts
        '''
        self.facts = dict()

    def parseFacts(self,filename):
        pf = ParseFacts()
        pf.parseFile(filename)

        self.initFactsDict(pf)

    def initFactsDict(self,parsedFacts):
        for fact in parsedFacts.knowledgelist:
            if fact.factname not in self.facts:
                self.facts[fact.factname] = list()
            self.facts[fact.factname].append(fact)





    def filterLog(self,rawlog):
        result = self.getCompressedLog(rawlog) # it default behaviour that it takes compressed logs
        for key in self.facts:
            method_check = getattr(self,key+"_check")
            if method_check(rawlog,self.facts[key]):
                method = getattr(self,key)
                result = method(rawlog)

        return result

    def getCompressedLog(self,rawlog):
        time = rawlog.date
        logmessage = rawlog.clog.clogname
        return [time,logmessage]

    def getRawLog(self,rawlog):
        time = rawlog.date
        logmessage = rawlog.log
        return [time,logmessage]

    def checkCompressedLog(self,rawlog,factlist):
        for fact in factlist:
            if fact.target == rawlog.clog.clogname:
                return True
        return False

    def extend_check(self,rawlog,factlist):
        return self.checkCompressedLog(rawlog,factlist)

    def extend(self,rawlog):
        return self.getRawLog(rawlog)