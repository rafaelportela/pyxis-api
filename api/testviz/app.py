from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dashboard:password@192.168.33.42/sandbox'

db = SQLAlchemy()
db.init_app(app)

class Run(db.Model):
  __tablename__ = 'runs'
  id = db.Column(db.String, primary_key = True)
  passes = db.Column(db.Integer)
  skips = db.Column(db.Integer)
  fails = db.Column(db.Integer)

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

@app.route('/')
def index():
  runs = db.session.query(Run).all()
  return render_template('index.html', runs = runs)

@app.route('/db')
def database():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

app.run(debug=True)
