# coding=utf-8

from unittest import TestCase

from tests_zeeguu_api.api_test_mixin import APITestMixin

from tests_zeeguu.rules.rss_feed_rule import RSSFeedRule
from zeeguu.content_retriever.article_downloader import download_from_feed
from zeeguu.model import RSSFeedRegistration
import zeeguu

from tests_zeeguu_api.test_feeds import FeedTests

URL_1 = "http://www.spiegel.de/politik/deutschland/diesel-fahrverbote-schuld-sind-die-grenzwerte-kolumne-a-1197123.html"


class UserArticlesTests(APITestMixin, TestCase):

    def setUp(self):
        super(UserArticlesTests, self).setUp()
        self.url = URL_1

    def test_starred_or_liked(self):
        # No article is starred initially
        result = self.json_from_api_get(f'/user_articles/starred_or_liked')
        assert (len(result) == 0)

        # Star article
        self.api_post(f'/user_article', formdata=dict(starred='True', url=self.url))

        # One article is starred eventually
        result = self.json_from_api_get(f'/user_articles/starred_or_liked')
        assert (len(result) == 1)

        # Like article
        self.api_post(f'/user_article', formdata=dict(liked='True', url=self.url))

        # Still one article is returned
        result = self.json_from_api_get(f'/user_articles/starred_or_liked')
        assert (len(result) == 1)

    def test_recommended(self):
        self.feed1 = RSSFeedRule().feed1
        self.feed2 = RSSFeedRule().feed2

        download_from_feed(self.feed1, zeeguu.db.session, 2)
        download_from_feed(self.feed2, zeeguu.db.session, 3)

        RSSFeedRegistration.find_or_create(zeeguu.db.session, self.user, self.feed1)
        RSSFeedRegistration.find_or_create(zeeguu.db.session, self.user, self.feed2)

        feed_items = self.json_from_api_get(f"/user_articles/recommended/5")
        assert (len(feed_items) == 5)
