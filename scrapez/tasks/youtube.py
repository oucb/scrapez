from celery import task, group
from celery.result import allow_join_result
from celery.utils.log import get_task_logger
from celeryapp import app
from flask_socketio import SocketIO
import eventlet
import logging
import pprint
import json
import os
import uuid
import requests

# monkey patch PyTube
import pytube
def safe_filename(s, max_length=255):
    return str(uuid.uuid4())

log = get_task_logger(__name__)

try:
    socketio = SocketIO(
        message_queue='redis://localhost',
        async_mode='eventlet',
        logger=True,
        engineio_logger=True)
except ImportError:
    log.warning("SocketIO not found ! Events won't work.")
    socketio = None

@app.task()
def download(url, itag, output_path=None, filename=None, api=False, events=False):
    """Start downloading a YouTube video.

    Args:
        url (str): A valid YouTube watch URL.
        itag (str): YouTube format identifier code.
    """
    yt = pytube.YouTube(url, on_progress_callback=on_progress(events=events))
    stream = yt.streams.get_by_itag(int(itag))
    title = stream.default_filename
    pytube.helpers.safe_filename = safe_filename # monkey patch pytube for default filename
    log.info('\n{fn} | {fs} bytes'.format(
        fn=stream.default_filename,
        fs=stream.filesize,
    ))
    try:
        stream.download(output_path=output_path, filename=stream.default_filename)
    except Exception as e:
        msg = "Error while downloading video to '%s'. %s: %s" % (output_path, type(e).__name__, str(e)) 
        log.exception(e)

    full_path = os.path.join(output_path, stream.default_filename)
    data = {
        'title': title,
        'path': full_path,
        'url': url,
        'size': stream.filesize,
        'extra_data': "itag=%s" % itag
    }
    if api:
        r = requests.post('http://localhost:5001/api/downloads', json=data)
        if not r.ok:
            log.error("Error while adding download to API. %s (%s)" % (r.status_code, r.reason))
            log.info(r.json())
    if events:
        socketio.emit('downloaded', data, namespace='/video')
    return data

@app.task()
def list_streams(url, order_by='resolution', events=False):
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
        if events:
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
def search(query, async=False, events=False):
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
    log.info("Executing %s tasks. Distributed ? %s .." % (len(urls), async))
    if async:
        g = group([list_streams.s(u, events=events) for u in urls])
        r = g.apply_async()
        with allow_join_result():
            result = r.get()
    else:
        result = []
        for u in urls:
            res = list_streams(u, events=events)
            result.append(res)
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

def on_progress(events=False):
    def inner(stream, chunk, file_handle, bytes_remaining, events=events):
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
        if events and (percent.is_integer()):
            socketio.emit('progress', {'percent': percent, 'url': url}, namespace='/video')
    return inner
