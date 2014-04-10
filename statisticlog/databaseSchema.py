__author__ = 'kosttek'

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
import datetime
import json

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer,Sequence("tag_id_seq") ,primary_key=True)
    tagname = Column(String, nullable=False, unique=True)
    compressedlogs = relationship("CompressedLog", order_by="CompressedLog.id", backref="tag")

    def __init__(self,tagname):
        self.tagname=tagname

    def putCompressedLog(self,clog):
        self.compressedlogs.append(clog)

    def __repr__(self):
        return "<Tag(tagname='%s')>" % self.tagname

class CompressedLog(Base):
    __tablename__ = 'compressedlogs'
    id = Column(Integer,Sequence("compressedlog_id_seq"), primary_key=True)
    clogname = Column(String, nullable=False)
    diffwords = Column(String, nullable=False) # should be string kind of [3, 5, 6] json.dumps(list(diffwordset))
    tag_id = Column(Integer, ForeignKey('tag.id'))
    rawlogs = relationship("RawLog", order_by="RawLog.id", backref="clog")



    # def __init__(self,clogname,diffwords):
    #     self.clogname = clogname
    #     self.diffwords= diffwords
    #     self.diffwordsset=None

    def __init__(self,clogname):
        self.clogname = clogname
        self.diffwords= '[]'
        self.diffwordsset = None

    def getDiffWordsSet(self):
        if self.diffwordsset == None :
            self.diffwordsset = set()
        else:
            self.diffwordsset = (json.loads(self.diffwords))
            pass
        return self.diffwordsset

    def setDiffWordsSet(self,set):
        self.diffwordsset = set
        self.diffwords = json.dumps(list(set))

    def compareAndAddDifferences(self,set):
        if self.diffwordsset == None:
            self.setDiffWordsSet(set)
            return True
        elif self.diffwordsset == set:
            return True
        else:
            return False


    def putRawLog(self,rlog):
        self.rawlogs.append(rlog)

    def clearRawLogList(self):
        del self.rawlogs[:]

    def __repr__(self):
        return "<CompressedLog(clog={}, diffwords={})>".format( self.clogname, self.diffwords)


class RawLog(Base):
    __tablename__ = 'rawlogs'
    id = Column(Integer,Sequence("rawlog_id_seq"), primary_key=True)
    log = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    clog_id = Column(Integer, ForeignKey('compressedlogs.id'))

    def __init__(self,log,date):
        self.log  = log
        self.date = date

    def __repr__(self):
        return "<RawLog(date={}, tag={} , log={})>".format( self.date,self.clog.tag.tagname, self.log)


if __name__  == "__main__":
    #its only for test purpose
    engine = create_engine('sqlite:///testdb/test.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    tag = Tag()
    tag.tagname = "TagLog"

    comlog = CompressedLog()
    comlog.clogname="compressed log name Start proc for example"
    comlog.diffwords="[]"

    tag.compressedlogs.append(comlog)

    rawlog = RawLog()
    rawlog.log="log message"
    rawlog.date = datetime.datetime.now()

    comlog.rawlogs.append(rawlog)

    session.merge(tag)
    session.commit()

    rlog = session.query(RawLog).first()
    print rlog
