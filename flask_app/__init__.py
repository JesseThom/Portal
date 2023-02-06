from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'its a secret to everybody'
#for saving to server
app.upload_folder = '/Users/MSI/Desktop/python/Portal/flask_app/static/imgs/paystubs'

DATABASE = "nld_db"#TODO change schema name 
#for saving to s3
BUCKET ="thom-bucket"