from recommender import CollaborativeFiltering
from api import recommend as recommend_function, get_data
from flask import Flask
app = Flask(__name__)


@app.route('/recommend')
def recommend():
    get_data()
    return recommend_function()

@app.route('/')
def home():
    return 'http://localhost:8888/recommend'


if __name__ == '__main__':
    # app.run(debug=False)
    import waitress
    print('http://localhost:8888/recommend')
    waitress.serve(app, host='127.0.0.1', port=8888)