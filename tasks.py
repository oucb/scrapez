from celery import task, group
from celery.result import allow_join_result
from pytube import YouTube
from pytube.cli import on_progress
import logging
import pprint

log = logging.getLogger(__name__)

@task
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

@task
def list_streams(url, order_by='resolution'):
    """List available YouTube streams from URL.

    Args:
        url (str): A valid YouTube watch URL.
        order_by (str): A py to order the list of `pytube.Stream` by.
    """
    print("Listing streams for %s" % url)
    yt = YouTube(url)
    streams = yt.streams.order_by(order_by).desc().all()
    streams = get_json_streams(streams)
    print("%s streams found" % len(streams))
    data = {
        'url': url,
        'title': yt.title,
        'thumbnail_url': yt.thumbnail_url,
        'streams': streams
    }
    log.debug(pprint.pformat(data))
    return data

def get_yt(url):
    return YouTube(url)

@task
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

    # Get streams for each URL and return stream data as well
    items = []
    # for u in urls:
    #     try:
    #         item = list_streams(u)
    #         items.append(item)
    #     except Exception as e:
    #         log.error("Error listing streams for %s" % u)
    #         continue
    g = group([list_streams.delay(u) for u in urls])
    res = g.apply_async()
    with allow_join_result():
        items = res.join()
    return items

def get_json_streams(streams):
    res = []
    for s in streams:
        data = s.fmt_profile
        data['itag'] = s.itag
        data['mime_type'] = s.mime_type
        res.append(data)
    return res
