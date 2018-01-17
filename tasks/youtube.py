from celery import task, group
from celery.result import allow_join_result
from celery.utils.log import get_task_logger
from celeryapp import app
from flask_socketio import SocketIO
from pytube.cli import display_progress_bar
import eventlet
import logging
import pprint
import json
import os

# monkey patch PyTube
import pytube
def safe_filename(s, max_length=255):
    import base64
    return base64.urlsafe_b64encode(your_string)
pytube.helpers.safe_filename = safe_filename


log = get_task_logger(__name__)
socketio = SocketIO(
    message_queue='redis://localhost',
    async_mode='eventlet',
    logger=True,
    engineio_logger=True)

@app.task()
def download(url, itag, output_path=None, filename=None):
    """Start downloading a YouTube video.

    Args:
        url (str): A valid YouTube watch URL.
        itag (str): YouTube format identifier code.
    """
    yt = pytube.YouTube(url, on_progress_callback=on_progress)
    stream = yt.streams.get_by_itag(int(itag))
    log.info('\n{fn} | {fs} bytes'.format(
        fn=stream.default_filename,
        fs=stream.filesize,
    ))
    stream.download(output_path=output_path, filename=stream.default_filename)
    socketio.emit('downloaded', {'url': url, 'itag': itag, 'size': stream.filesize }, namespace='/video')
    return os.path.join(output_path, stream.default_filename)

@app.task()
def list_streams(url, order_by='resolution'):
    """List available YouTube streams from URL.

    Args:
        url (str): A valid YouTube watch URL.
        order_by (str): A py to order the list of `pytube.Stream` by.
    """
    try:
        print("Listing streams for %s" % url)
        yt = pytube.YouTube(url)
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
        socketio.emit('new_video', data, namespace='/video')
        log.debug(pprint.pformat(data))
        return data
    except Exception as e:
        print("An error occured while listing streams for '%s'" % url)
        print("Exception: %s - %s" % (type(e).__name__, str(e)))
        return {}

def get_yt(url):
    return pytube.YouTube(url)

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
        log.info("resolution: %s" % data['resolution'])
        if data['resolution']:
            data['resolution_int'] = int(data['resolution'].rstrip('p'))
        else:
            data['resolution_int'] = 0
        if s.mime_type not in ['video/webm', 'video/3gpp']:
            res.append(data)
    res = sorted(res, key=lambda k: k['resolution_int'], reverse=True)
    return res

def on_progress(stream, chunk, file_handle, bytes_remaining):
    """On download progress callback function.
    :param object stream:
        An instance of :class:`Stream <Stream>` being downloaded.
    :param file_handle:
        The file handle where the media is being written to.
    :type file_handle:
        :py:class:`io.BufferedWriter`
    :param int bytes_remaining:
        How many bytes have been downloaded.
    """
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    url = stream.player_config_args['loaderUrl']
    socketio.emit('progress', {'percent': percent, 'url': url}, namespace='/video')
