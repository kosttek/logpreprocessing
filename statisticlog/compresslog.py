# -*- coding: latin-1 -*-
__author__ = 'kosttek'

from logmetric import SequenceMatcher
import re
import datetime
from databaseSchema import Tag, RawLog, CompressedLog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import databaseSchema

class CompressLog():
    '''[tag][log]->logdictdata'''

    compare_ration = 0.5

    def __init__(self):
        self.taglist=list()

    def add(self,rawlog):
        [tag_str,log,date] = self.parseLog(rawlog)

        #if rawlog is not log but kind of --------begining of /dev/logsystem
        if tag_str == None:
            return

        #raw logs alre without numbers
        #log = self.removeNumsAfterEqualityChar(log)
        log = self.removeNumsBiggerThanTwoDigits(log)
        log = log.replace(",", " ")
        #find tag
        tag_obj = self.checkIfTagExistAndReturn(tag_str)
        if tag_obj == None:
            tag_obj = self.createNewTag(tag_str)

        # check logs for same
        for key_compressedlog in tag_obj.compressedlogs:
            key = key_compressedlog.clogname

            seq = SequenceMatcher(key,log)
            if seq.ratio() >= CompressLog.compare_ration:
                isSame = key_compressedlog.compareAndAddDifferences(seq.different_words)
                if isSame :
                    key_compressedlog.clogname = self.replaceDiffWordsWithSigns(log,seq.different_words,"@@@")
                    key_compressedlog.rawlogs.append(RawLog(log=log,date=date))
                    return # end of comparing

        # if not found same create new log
        new_clog = CompressedLog(log)
        new_clog.rawlogs.append(RawLog(log=log,date=date))
        tag_obj.compressedlogs.append(new_clog)

    # None if do not
    def checkIfTagExistAndReturn(self,tag):
        for tag_obj in self.taglist:
            if tag_obj.tagname == tag:
                return tag_obj
        return None

    def createNewTag(self,tag):
        tag_obj = Tag(tag)
        self.taglist.append(tag_obj)
        return tag_obj

    def replaceDiffWordsWithSigns(self,log,diffset,sign):
        splitedlog = log.split(" ")
        for index in diffset:
            splitedlog[index] = sign
        return " ".join(splitedlog)

    def parseLog(self,log_):
        '''
        03-28 15:43:19.225 W/ActivityManager(  341): Unable to start service Intent { cmp=com.aware/.Applications }: not found
        '''
        log_words_tag = log_.split(":",2)
        #remorve begining buffers token
        if len(log_words_tag) == 1:
            return [None,None,None]

        log = log_words_tag[2][log_words_tag[2].index(')')+2:].rstrip('\n').rstrip('\r')

        sec_and_tag = log_words_tag[2].split(' ',1);
        tag_temp = sec_and_tag[1]
        tag = tag_temp[:tag_temp.index('(')].rstrip(" ")
        date = self.getDate(log_words_tag[0],log_words_tag[1],sec_and_tag[0])

        #decode to utf-8
        tag_out = tag.decode('utf-8')
        log_out = log.decode('utf-8')
        return [tag_out, log_out, date]

    year = 2014
    def getDate(self,date_hour, minutes, sec_milisec):
        '''
        03-28 15:43:19.225
        ['03-28 15', '43', '19.225']
        '''
        year = CompressLog.year
        [month_day,hour]=date_hour.split(" ")
        [month,day]=month_day.split("-")
        [sec,milisec]=sec_milisec.split(".")

        return datetime.datetime(year,int(month),int(day),int(hour),int(minutes),int(sec),int(milisec))

    def removeNumsAfterEqualityChar(self,log):
        '''replace every number witch start with '=' sign by '='(secound argument) or '|' all brackets {} with numbers in it separated by commma ',' '''
        result = re.sub("=(\d+)|=\{([0-9, ])+\}","=",log)
        return result

    def removeNumsBiggerThanTwoDigits(self, log):
        result = re.sub("(\d\d+)|\{([0-9, ])+\}|=\[([0-9, ])+\]","",log)
        return result

    def parse_logs_to_database(self, log_file_path, database_file_path):
        log_file = open(log_file_path)
        for log_line in log_file:
            self.add(log_line)
        engine = create_engine('sqlite:///'+database_file_path, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        databaseSchema.Base.metadata.create_all(engine)

        for tag in self.taglist:
            session.add(tag)
        session.commit()

if __name__ == "__main__":
    compres = CompressLog()

    f = open("../logs/logcatlogs",'r')

    for i in range(0,10000):
        line = f.readline()
        compres.add(line)

    for tag  in compres.taglist:
        print tag
        for clog in tag.compressedlogs:
            print " ",len(clog.rawlogs), clog.diffwords, clog.clogname

    engine = create_engine('sqlite:///testdb/testlogs.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    databaseSchema.Base.metadata.create_all(engine)

    for tag in compres.taglist:
        session.add(tag)
    session.commit()