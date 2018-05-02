
# -*- coding: utf-8 -*-


import json
import flask
from resources_crawler.crawler import Crawler
from resources_crawler.rss import RssLoad


ITEM_MANDATORY_FIELDS = ("title", "link", "published", "description")
UNLIMITED_ITEMS_COUNT = -1


app = flask.Flask(__name__)

def collect_feed(feed_data):
    def local_data(feed):
        feed_data["title"] = feed.title
    
    return local_data

def collect_items(items_data, items_count=UNLIMITED_ITEMS_COUNT):
    def local_data(item):
        len_items_data = len(items_data)
        # check limit of items. If there is limit of data and we already have
        # enough items, just skip next step
        if int(items_count) > 0 and int(len_items_data) >= int(items_count):
            return False

        local_item = dict()
        for key in ITEM_MANDATORY_FIELDS:
            local_item[key] = item.get(key)

        items_data.append(local_item)

    return local_data

def get_rss_data(url, count):
    feed_data = dict()
    items_data = list()

    feed_handler = collect_feed(feed_data)
    item_handler = collect_items(items_data, count)

    rss_object = RssLoad(feed_handler, item_handler)
    crawler = Crawler(rss_object)

    res = crawler.process(url)
    if res.success:
        return flask.Response(
            status=200,
            mimetype="application/json",
            response=json.dumps((feed_data, items_data)) + "\n"
        )
    else:
        return flask.Response(
            status=500,
            response=res.error
        )


@app.route('/')
def root():
    return flask.redirect('/api/1.0/rss')

@app.route("/api/1.0/rss", methods=["GET"])
def rss():
    url = flask.request.args.get("url")
    if url is None:
        return flask.Response(status=500, response="Give me an URL")

    count = flask.request.args.get("count")
    if count is None:
        count = UNLIMITED_ITEMS_COUNT

    return get_rss_data(url, count)

if __name__ == '__main__':
    app.debug = True
    app.run()
