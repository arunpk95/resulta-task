The service is hosted in heroku client. The endpoint for the service is 
https://resulta-task.herokuapp.com/getstats/<league_name>/<yyyy-mm-dd>/<yyyy-mm-dd>
<i>Note: The difference between the start date and end date should be less than 7</i>

Sample test case https://resulta-task.herokuapp.com/getstats/NFL/2020-01-08/2020-01-13

# Try it on Codepen client

https://codepen.io/arunpk95/pen/ExvwEmZ

Please visit the above link to check/test the WebClient for the service


# Try it locally
1. Download/Clone the repo
2. Please install the python packages required: 
<pre>pip install -r requirements.txt</pre>
3. run __init__.py to start the local serve

Fetch the GET request in the browser from the local server: http://127.0.0.1:5000/getstats/NFL/2020-01-08/2020-01-13

# File structure of the application
  flask-task/
    config/
        endPointsKey.py -- contains key and api information
    helpers.py - functions to help with implementations
    __init__.py - flask endpoints and main file

  
