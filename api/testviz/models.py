from sqlalchemy import Column, Integer, String
from database import Base

class Run(Base):
  __tablename__ = 'runs'
  id = Column(String, primary_key = True)
  passes = Column(Integer)
  skips = Column(Integer)
  fails = Column(Integer)

  def __init__(self, id, passes, skips, fails):
    self.id = id
    self.passes = passes
    self.skips = skips
    self.fails = fails

  def success_percentage(self):
    if self.passes == 0:
      return 0

    total = self.passes + self.skips + self.fails
    percent =  (self.passes / float(total)) * 100
    truncated = int(percent)
    return truncated
