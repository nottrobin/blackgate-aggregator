#!/usr/bin/env python

# Modules
from flask import Flask
import feedparser
import requests
import requests_cache

requests_cache.install_cache('aggregator.cache')

app = Flask(__name__)

@app.route("/")
def hello():
    rss_request = requests.get('https://robinwinslow.co.uk/rss-canonical.xml', verify=False)
    rss = feedparser.parse(rss_request.content)

    body = '<ul>'

    for article in rss['entries']:
        body += "<li>{}: {}</li>".format(article['updated'], article['title'])

    return body + '</ul>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
