# Import necessary libraries
from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_posts():
    api_url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
