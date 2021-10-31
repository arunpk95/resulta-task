from helpers import *
from flask import Flask

#iniate flask app
app = Flask(__name__)

#endpoint for the required stats  http://127.0.0.1:5000/getstats/<league_name>/<from_date>/<to_date>
#sample url: http://127.0.0.1:5000/getstats/NFL/2020-01-12/2020-01-13
@app.route('/getstats/<league_name>/<from_date>/<to_date>')
def get_stats(league_name, from_date, to_date):
    return get_combined_result(league_name, from_date, to_date)

if __name__ == '__main__':
    app.run(debug = True)