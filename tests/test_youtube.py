"""Test youtube functions."""
import unittest
from celeryapp import app
app.conf.update({'task_always_eager': True})

DATA = {
    'query': "Michael Jackson",
    'url': "https://www.youtube.com/watch?v=sOnqjkJTMaA",
    'itag': "135"
}

class YoutubeTest(unittest.TestCase):
    def test_youtube_search(self):
        from tasks.youtube import search
        query = DATA['query']
        resp = search(query)
        self.assertTrue(resp is not [])

    def test_youtube_list_streams(self):
        from tasks.youtube import list_streams
        url = DATA['url']
        resp = list_streams(url)
        self.assertTrue(resp is not {})

    def test_youtube_download(self):
        from tasks.youtube import download
        url = DATA['url']
        itag = DATA['itag']
        filepath = download(url, itag)
        self.assertTrue(filepath is not None)
