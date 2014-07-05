__author__ = 'kosttek'

from parsefacts import  ParseFacts
class RuleEngine():

    def __init__(self):
        ''' factname -> list of facts
        '''
        self.facts = dict()
        self.method_default = None

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
        method = self.getDefaultBehaviourMethod()
        for key in self.facts:
            method_check = getattr(self,key+"_check")
            if method_check(rawlog,self.facts[key]):
                method = getattr(self,key)
                break

        return method(rawlog)

    def checkTemplate(self,rawlog,factlist,getmethod):
        for fact in factlist:
            if fact.target.lstrip().rstrip() == getmethod(rawlog).rstrip().lstrip():
                return True
        return False

    def getDefaultBehaviourMethod(self):
        if self.method_default == None:
            self.method_default =  self.checkDefault()
            self.removeNotCheckableFacts()
        return self.method_default

    def removeNotCheckableFacts(self):
        self.facts.pop('default',None)

    def getCompressedLog(self,rawlog):
        time = rawlog.date
        logmessage = rawlog.clog.clogname
        return [time,logmessage]

    def prepareLogOut(self,rawlog,method):
        time = rawlog.date
        logmessage = method(rawlog)
        return [time,logmessage]

    def getRawLogOut(self,rawlog):
        return self.prepareLogOut(rawlog,self.getRawlogFromRawlog)

    def getCompressedLogOut(self,rawlog):
        return self.prepareLogOut(rawlog,self.getClognameFromRawlog)

    def getTagLogOut(self,rawlog):
        return self.prepareLogOut(rawlog,self.getTagFromRawlog)

    def checkCompressedLog(self,rawlog,factlist):
        return self.checkTemplate(rawlog,factlist,self.getClognameFromRawlog)

    def checkTag(self,rawlog,factlist):
        return self.checkTemplate(rawlog,factlist,self.getTagFromRawlog)

    def getClognameFromRawlog(self,rawlog):
        return rawlog.clog.clogname

    def getTagFromRawlog(self,rawlog):
        return rawlog.clog.tag.tagname

    def getRawlogFromRawlog(self,rawlog):
        return rawlog.log


# rules default
    def checkDefault(self):
        methodname = 'clog' # if defalut is note precised then default_clog will be runx
        if 'default' in self.facts: # 'default' is in facts dict only on the beggining
            methodname = self.facts['default'][0].arglist[0]
        method = getattr(self,'default_'+methodname)
        return method

    def default_tag(self,rawlog):
        return self.getTagLogOut(rawlog)

    def default_clog(self,rawlog):
        return self.getCompressedLogOut(rawlog)

    def default_rawlog(self,rawlog):
        return self.getRawLogOut(rawlog)

    def default_remove(self,rawlog):
        return None

#rules
#extend
#removetag

    def extend_check(self,rawlog,factlist):
        return self.checkCompressedLog(rawlog,factlist)

    def extend(self,rawlog):
        return self.getRawLogOut(rawlog)

    def removetag_check(self,rawlog,factlist):
        return self.checkTag(rawlog,factlist)

    def removetag(self,rawlog):
        return None

    def removeclog_check(self,rawlog,factlist):
        return self.checkCompressedLog(rawlog,factlist)

    def removeclog(self,rawlog):
        return None

    def leavetagfromtag_check(self,rawlog,factlist):
        return self.checkTag(rawlog,factlist)

    def leavetagfromtag(self,rawlog):
        return self.getTagLogOut(rawlog)

    def notremoveclog_check(self,rawlog,factlist):
        return self.checkCompressedLog(rawlog,factlist)

    def notremoveclog(self,rawlog):
        return self.getCompressedLogOut(rawlog)