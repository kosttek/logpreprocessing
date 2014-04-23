__author__ = 'kosttek'

from statisticlog.databaseSchema import Tag, RawLog, CompressedLog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import statisticlog.databaseSchema
from rulesengine.rulesengine import RuleEngine
import preparearff

class PrepareLogsFromDB():

    def __init__(self,databasefile,knowledgebasefile):
        self.loglist = list()
        self.logset_list = list
        logset = set()

        re = RuleEngine()
        re.parseFacts(knowledgebasefile)
        for rawlog in self.queryAllRawlogs(databasefile):

            result = re.filterLog(rawlog)
            if result == None:
                continue

            [date,logmessage]= result

            self.loglist.append([date,logmessage])
            logset.add(logmessage)

        self.logset_list = list(logset)
        self.loglist = sorted(self.loglist, key=lambda k: k[0]) # sort by date


    def queryAllRawlogs(self,databasefile):
        '''databasefile = testlogs.db'''
        engine = create_engine('sqlite:///../statisticlog/testdb/'+databasefile, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        statisticlog.databaseSchema.Base.metadata.create_all(engine)
        return session.query(RawLog).all()


    def createLearningData(self,timewindowsize_sec):
        ''' create learning data as array for association rule mining
        for every time window there is array where for any kind of log there is boolean variable which symbolise
        if its occure or not in time window
        there is no such dependency as log is before or after other log o
        '''
        self.timewindowdata = list()
        for log in self.loglist:
            timewindowlogarray = self.create_empty_array()
            start_index=self.loglist.index(log)
            first_log_date = log[0]
            index = start_index
            for next_log in self.loglist[index:]:
                date = next_log[0]
                timedelta = date - first_log_date
                delta_sec = float(timedelta.microseconds)/1000000 + timedelta.seconds
                if timewindowsize_sec >= delta_sec:
                    self.add_log_to_array(next_log, timewindowlogarray)
                    print next_log
                else:
                    print "----", delta_sec
                    break
            self.timewindowdata.append(timewindowlogarray)

    def create_empty_array(self):
        return [False] * len(self.logset_list)

    def add_log_to_array(self, log , array):
        index = self.logset_list.index(log[1])
        array[index] = True

if __name__ == '__main__':
    prepareLogs = PrepareLogsFromDB('testlogs.db','../rulesengine/knowledgebase')
    for log in prepareLogs.logset_list:
        print log
    prepareLogs.createLearningData(2)
    for timew in prepareLogs.timewindowdata:
        print timew

    _preparearff = preparearff.PrepareArff()

    _preparearff.prepare_bool_association_file("one_day_logs",prepareLogs.logset_list,prepareLogs.timewindowdata)