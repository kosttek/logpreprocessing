__author__ = 'kosttek'

from logmetric import SequenceMatcher
import re

class CompressLog():
    '''[tag][log]->logdictdata'''

    compare_ration = 0.5

    def __init__(self):
        self.logdict=dict()

    def add(self,rawlog):
        [tag,log] = self.parseLog(rawlog)

        #if rawlog is not log but kind of --------begining of /dev/logsystem
        if tag == None:
            return

        log = self.removeNumsAfterEqualityChar(log)

        #find tag
        if self.logdict.has_key(tag):
            tag_dict = self.logdict[tag]
        else:
            tag_dict = dict()
            self.logdict[tag]=tag_dict

        # check logs for same
        for key in tag_dict.iterkeys():
            seq = SequenceMatcher(key,log)
            if seq.ratio() >= CompressLog.compare_ration:
                logDictData = tag_dict[key]
                isSame = logDictData.compare(seq.different_words)
                if isSame :
                    logDictData.incrementCount()
                    return # end of comparing

        # if not found same create new log
        tag_dict[log]=LogDictData()

    def parseLog(self,log):
        log_words_tag = log.split(":",3)
        #remorve begining buffers token
        if len(log_words_tag) == 1:
            return [None,None]

        log = log_words_tag[3].rstrip('\n').rstrip('\r')

        tag_temp = log_words_tag[2].split(' ',1)[1]
        tag = tag_temp[:tag_temp.index('(')]

        return [tag,log]

    def removeNumsAfterEqualityChar(self,log):
        '''replace every number witch start with '=' sign by '='(secound argument) or '|' all brackets {} with numbers in it separated by commma ',' '''
        result = re.sub("=(\d+)|=\{([0-9, ])+\}","=",log)
        return result



class LogDictData():
    def __init__(self):
        self.diffwordsset = None
        self.count = 1

    # def __init__(self,set):
    #     self.diffwordsset = set
    #     self.incrementCount() # 2?

    def incrementCount(self):
        self.count +=1

    def compare(self,set):
        if self.diffwordsset == None:
            self.diffwordsset = set
            return True
        elif self.diffwordsset == set:
            return True
        else:
            return False

if __name__ == "__main__":
    compres = CompressLog()

    f = open("../logs/logcatlogs",'r')

    for i in range(0,10000):
        try:
            line = f.readline()
            compres.add(line)
        except:
            print line

    for tag , tagval in compres.logdict.iteritems():
        print tag
        for log,val in tagval.iteritems():
            print " ",val.count, val.diffwordsset, log