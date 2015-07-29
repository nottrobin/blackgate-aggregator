#!/usr/bin/env python

# Modules
from flask import Flask
import requests
import requests_cache

requests_cache.install_cache('aggregator.cache')

app = Flask(__name__)

@app.route("/")
def hello():
    rss_request = requests.get('https://robinwinslow.co.uk/rss-canonical.xml', verify=False)
    return rss_request.content

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
