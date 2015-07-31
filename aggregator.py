#!/usr/bin/env python

# Modules
from flask import Flask, send_from_directory
from flask.views import View

# Local
from lib import (
    article_data,
    article_hash,
    article_path,
    article_slug,
    find_article_by_hash,
    rss_articles,
    parse_template
)

articles = rss_articles('https://robinwinslow.co.uk/rss-canonical.xml')

app = Flask(__name__)


@app.route("/")
def index():
    """
    Return a list of all articles in RSS feed
    """

    sanitised_articles = [article_data(article) for article in articles]

    return parse_template('index.html', {'articles': sanitised_articles})


@app.route("/<hash_id>/<slug>")
def article(hash_id, slug):
    """
    Return content for an article
    """

    article = find_article_by_hash(articles, hash_id)

    return parse_template('article.html', article_data(article))


@app.route('/css/<path>')
def send_css(path):
    """
    Serve static CSS files
    """

    return send_from_directory('css', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
