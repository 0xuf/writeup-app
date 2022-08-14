from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from tomli import load

with open("config.toml", mode="rb") as _config_file:
    _config = load(_config_file)
    _config_file.close()

Base = declarative_base()


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    url = Column(String)
    title = Column(String)
    author = Column(String)
    platform = Column(String)
