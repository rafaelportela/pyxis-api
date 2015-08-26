from app import app
import os

app.run(debug=True, host=os.getenv('HOST', 'localhost'))
