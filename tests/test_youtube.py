"""Test youtube functions."""
import unittest
from celeryapp import app
import os
app.conf.update({'task_always_eager': True})

DATA = {
    'query': "Michael Jackson",
    'url': "https://www.youtube.com/watch?v=sOnqjkJTMaA",
    'itag': "135"
}
ASYNC = os.environ.get('FLASK_TEST_ASYNC', False)
EVENTS = os.environ.get('FLASK_TEST_EVENTS', False)
API = os.environ.get('FLASK_TEST_API', False)

class YoutubeTest(unittest.TestCase):
    def test_youtube_search(self):
        from tasks.youtube import search
        query = DATA['query']
        resp = search(query, async=False)
        self.assertTrue(resp is not [])

    def test_youtube_list_streams(self):
        from tasks.youtube import list_streams
        url = DATA['url']
        resp = list_streams(url, async=ASYNC, events=EVENTS)
        self.assertTrue(resp is not {})

    def test_youtube_download(self):
        from tasks.youtube import download
        url = DATA['url']
        itag = DATA['itag']
        data = download(url, itag, events=EVENTS, api=API)
        self.assertTrue(data is not None)
        self.assertTrue('url' in data)
        self.assertTrue('path' in data)
        self.assertTrue('title' in data)
        self.assertTrue('size' in data)
