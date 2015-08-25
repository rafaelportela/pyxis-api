from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

class TestRuns(Base):
  __tablename__ = 'test_runs'
  id = Column(String, primary_key = True)
  run_id = Column(Integer, ForeignKey('runs.id'), primary_key=True)
  test_id = Column(Integer, ForeignKey('tests.id'), primary_key=True)
  status = Column(String)
  test = relationship('Test')

class Run(Base):
  __tablename__ = 'runs'
  id = Column(String, primary_key = True)
  passes = Column(Integer)
  skips = Column(Integer)
  fails = Column(Integer)
  tests = relationship('TestRuns')

  def __init__(self, id, passes, fails, skips):
    self.id = id
    self.passes = passes
    self.fails = fails
    self.skips = skips

  def success_percentage(self):
    if self.passes == 0:
      return 0

    total = self.passes + self.skips + self.fails
    percent =  (self.passes / float(total)) * 100
    truncated = int(percent)
    return truncated

  def serialize(self):
    return { 'id': self.id,
        'success_percentage': self.success_percentage(),
        'passes': self.passes,
        'fails': self.fails,
        'skips': self.skips }

class Test(Base):
  __tablename__ = 'tests'
  id = Column(String, primary_key = True)
  name = Column('test_id', String(256))

  def __init__(self, id, name):
    self.id = id
    self.name = name

  def serialize(self):
    return { 'id': self.id, 'name': self.name }
