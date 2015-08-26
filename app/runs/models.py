from app import db

class TestRuns(db.Model):
  __tablename__ = 'test_runs'
  id = db.Column(db.String, primary_key = True)
  run_id = db.Column(db.Integer, db.ForeignKey('runs.id'), primary_key=True)
  test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), primary_key=True)
  status = db.Column(db.String)
  test = db.relationship('Test')

class Run(db.Model):
  __tablename__ = 'runs'
  id = db.Column(db.String, primary_key = True)
  passes = db.Column(db.Integer)
  skips = db.Column(db.Integer)
  fails = db.Column(db.Integer)
  testruns = db.relationship('TestRuns')

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

class Test(db.Model):
  __tablename__ = 'tests'
  id = db.Column(db.String, primary_key = True)
  name = db.Column('test_id', db.String(256))

  def __init__(self, id, name):
    self.id = id
    self.name = name

  def serialize(self):
    return { 'id': self.id, 'name': self.name }
