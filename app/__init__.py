from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yugal'  # Change this to a secure secret key

from app import routes 