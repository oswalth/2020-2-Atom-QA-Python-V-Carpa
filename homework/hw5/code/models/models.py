from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class File(Base):
    __tablename__ = 'file'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(30), nullable=False)

    def __repr__(self):
        return f"<File(id='{self.id}', filename='{self.filename}'>"


class Log(Base):
    __tablename__ = 'log'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey(f'{File.__tablename__}.{File.id.name}'), nullable=False)
    ipv4 = Column(String(15), nullable=False)
    datetime = Column(DateTime(timezone=True), nullable=False, default='1970-01-01')
    method = Column(Text, nullable=False)
    url = Column(String(2000), nullable=False)
    req_ver = Column(String(20), nullable=False)
    code_status = Column(Integer)
    size = Column(Integer)
    option_1 = Column(Text, nullable=False)
    option_2 = Column(Text, nullable=False)
    option_3 = Column(Text, nullable=False)

    def __repr__(self):
        return f"<File(id='{self.id}', filename='{self.ipv4}'>"
