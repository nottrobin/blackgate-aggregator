#!/usr/bin/env python

# Modules
from flask import Flask
from flask.views import View

# Local
from lib import (
    article_hash,
    article_path,
    article_slug,
    find_article_by_hash,
    rss_articles
)

articles = rss_articles('https://robinwinslow.co.uk/rss-canonical.xml')

app = Flask(__name__)


@app.route("/")
def index():
    """
    Return a list of all articles in RSS feed
    """

    body = '<ul>'

    for article in articles:
        body += '<li><a href="{}">{}: {}</a></li>'.format(
            article_path(article),
            article['updated'][:10],
            article['title'].encode('utf-8')
        )

    return body + '</ul>'


@app.route("/<hash_id>/<slug>")
def article(hash_id, slug):
    """
    Return content for an article
    """

    article = find_article_by_hash(articles, hash_id)

    return '<h1>{}</h1><article>{}</article>'.format(
        article['title'].encode('utf-8'),
        article['summary'].encode('utf-8')
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
