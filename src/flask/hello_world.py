from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page"

@app.route('/hello')
@app.route('/hello/<username>')
def hello_world(username="friend"):
    return f'Hello {username}. This is the Big Muddy Railroad!'
