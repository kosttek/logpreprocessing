__author__ = 'kosttek'


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    addresses = relationship("Address", order_by="Address.id", backref="user")
    def __repr__(self):
       return "<User(name='%s', fullname='%s', password='%s')>" % (
                            self.name, self.fullname, self.password)




class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    #user = relationship("User", backref=backref('addresses', order_by=id))

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

if __name__ == "__main__":
    engine = create_engine('sqlite:///testdb/testalchemy.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
    jack.addresses = [
                Address(email_address='jack@google.com'),
                Address(email_address='j25@yahoo.com')]

    session.add(jack)
    session.commit()

    jack2 = session.query(User).filter_by(name='jack').first()
    jack.password='fucklogic'
    print jack2.addresses[0].user
