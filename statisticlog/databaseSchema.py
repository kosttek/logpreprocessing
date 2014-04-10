__author__ = 'kosttek'

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer,Sequence("tag_id_seq") ,primary_key=True)
    tagname = Column(String, nullable=False)

    compressedlogs = relationship("CompressedLog", order_by="CompressedLog.id", backref="tag")

    def __repr__(self):
        return "<Tag(tagname='%s')>" % self.tagname

class CompressedLog(Base):
    __tablename__ = 'compressedlogs'
    id = Column(Integer,Sequence("compressedlog_id_seq"), primary_key=True)
    clogname = Column(String, nullable=False)
    diffwords = Column(String, nullable=False) # should be string kind of [3, 5, 6] json.dumps(list(diffwordset))

    tag_id = Column(Integer, ForeignKey('tag.id'))
    ##tag = relationship("Tag", backref=backref('compressedlogs', order_by=id))

    rawlogs = relationship("RawLog", order_by="RawLog.id", backref="clog")

class RawLog(Base):
    __tablename__ = 'rawlogs'
    id = Column(Integer,Sequence("rawlog_id_seq"), primary_key=True)
    log = Column(String, nullable=False)
    #date =
    clog_id = Column(Integer, ForeignKey('compressedlogs.id'))
 ##   clog = relationship("CompressedLog", backref=backref('rawlogs', order_by=id))


if __name__  == "__main__":
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

    comlog.rawlogs.append(rawlog)

    session.add(tag)
    session.commit()

