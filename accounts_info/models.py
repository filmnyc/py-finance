
from datetime import datetime
from sqlalchemy import (create_engine, Column, Integer, String, Float, Text,
                        ForeignKey, Date)
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://myuser:mypass@localhost:5432/accounts',
                       echo=False)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Base = declarative_base()

Base.query = db_session.query_property()


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    balance = Column(Float)
    transact = relationship('Transaction', cascade="all,delete",
                            backref='transact', lazy=True)

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    action = Column(String(12), nullable=False)
    amount = Column(Float, nullable=False)
    cdate = Column(Date, default=datetime.today().strftime("%Y-%m-%d"),
                   nullable=False)
    comment = Column(Text)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)


account_table = Account.__table__
transaction_table = Transaction.__table__

if __name__ == '__main__':
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db_session.commit()
