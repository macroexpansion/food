from recommender import CollaborativeFiltering
from api import recommend as recommend_function
from flask import Flask
app = Flask(__name__)


@app.route('/recommend')
def recommend():
    return recommend_function()


if __name__ == '__main__':
    # app.run(debug=False)
    import waitress
    print('http://localhost:8888/recommend')
    waitress.serve(app, host='127.0.0.1', port=8888)