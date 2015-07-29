# System
from datetime import datetime
from hashlib import sha1
import string

# Modules
import feedparser
import requests
import requests_cache

def rss_articles(feed_url):
    """
    Get all articles in RSS feed
    """

    # Setup cache for requests
    requests_cache.install_cache('aggregator.cache')

    # Get the feed RSS
    rss_request = requests.get(feed_url, verify=False)

    # Parse and return the RSS data
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


def find_article_by_hash(articles, hash_id):
    """
    Given an article's hash, find the article
    """

    for article in articles:
        if hash_id == article_hash(article):
            return article
