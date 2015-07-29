#!/usr/bin/env python

# System
from datetime import datetime
from hashlib import sha1
import string

# Modules
from flask import Flask
from flask.views import View
import feedparser
import requests
import requests_cache

requests_cache.install_cache('aggregator.cache')

app = Flask(__name__)


def rss_articles():
    """
    Get all articles in RSS feed
    """

    rss_request = requests.get('https://robinwinslow.co.uk/rss-canonical.xml', verify=False)
    return feedparser.parse(rss_request.content)['entries']


def article_slug(article):
    """
    Generate a relatively friendly-looking
    slug for the article
    (e.g.: 2015-05-04-my-new-article)
    """

    # Get just the ISO date (YYYY-MM-DD)
    article_date = article['updated'][:10]

    # Allowed characters - lowercase plus hyphen
    valid_chars = string.ascii_lowercase + '-'

    # Make title lowercase and replace spaces
    title = article['title'].encode('utf-8')
    simple_title = title.replace(' - ', '-').replace(' ', '-').lower()

    # Get all title characters in allowed set
    allowed_characters = []

    for character in simple_title:
        if character in valid_chars:
            allowed_characters.append(character)

    # Join allowed characters to make the sanitised title
    sanitised_title = ''.join(allowed_characters)

    return '{}-{}'.format(article_date, sanitised_title)

def article_path(article):
    """
    Generate a relatively friendly URL path
    for an article
    """

    return '/{}/{}'.format(article_hash(article), article_slug(article))


def article_hash(article):
    """
    Get a 6-digit SHA1 of an article's ID
    """

    return sha1(article['id']).hexdigest()[:6]


def get_article_by_hash(hash_id):
    """
    Given an article's hash, find the article
    """

    for article in rss_articles():
        if hash_id == article_hash(article):
            return article


@app.route("/")
def index():
    """
    Return a list of all articles in RSS feed
    """

    body = '<ul>'

    for article in rss_articles():
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

    article = get_article_by_hash(hash_id)

    return '<h1>{}</h1><article>{}</article>'.format(
        article['title'].encode('utf-8'),
        article['summary'].encode('utf-8')
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
