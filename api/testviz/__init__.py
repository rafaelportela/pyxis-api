app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dashboard:password@192.168.33.42/sandbox'
 
from models import db
db.init_app(app)

import pdb; pdb.set_trace()
