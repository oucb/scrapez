from celery import task, group
from celery.result import allow_join_result
from celeryapp import app
from pytube import YouTube
from pytube.cli import on_progress
import logging
import pprint
import lxml

log = logging.getLogger(__name__)

@app.task()
def download(url, itag, output_path=None, filename=None):
    """Start downloading a YouTube video.

    Args:
        url (str): A valid YouTube watch URL.
        itag (str): YouTube format identifier code.
    """
    yt = YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.get_by_itag(itag)
    log.info('\n{fn} | {fs} bytes'.format(
        fn=stream.default_filename,
        fs=stream.filesize,
    ))
    stream.download(output_path=output_path, filename=filename)

@app.task()
def list_streams(url, order_by='resolution'):
    """List available YouTube streams from URL.

    Args:
        url (str): A valid YouTube watch URL.
        order_by (str): A py to order the list of `pytube.Stream` by.
    """
    try:
        print("Listing streams for %s" % url)
        yt = YouTube(url)
        streams = yt.streams.order_by(order_by).desc().all()
        streams = get_json_streams(streams)
        print("%s streams found" % len(streams))
        data = {
            'url': url,
            'title': yt.title,
            'id': yt.video_id,
            'thumbnail_url': yt.thumbnail_url,
            'streams': streams
        }
        log.debug(pprint.pformat(data))
        return data
    except Exception as e:
        print("An error occured while listing streams for '%s'" % url)
        print("Exception: %s - %s" % (type(e).__name__, str(e)))
        return {}

def get_yt(url):
    return YouTube(url)

@app.task()
def search(query):
    """Search YouTube and return a list of video links.

    Args:
        query (str): Text to search for on YouTube.
    """
    import urllib
    import urllib2
    from bs4 import BeautifulSoup
    query = urllib.quote(query)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'lxml')
    urls = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        url = vid['href']
        if url.startswith('/watch'):
            urls.append('https://www.youtube.com' + url)

    # Get streams for each URL and return streams data as well
    log.info("Executing group of %s tasks .." % len(urls))
    # urls = [urls[0]]
    g = group([list_streams.s(u) for u in urls])
    r = g.apply_async()
    with allow_join_result():
        result = r.get()
    return result

def get_json_streams(streams):
    res = []
    for s in streams:
        data = s.fmt_profile
        data['itag'] = s.itag
        data['mime_type'] = s.mime_type
        res.append(data)
    return res
