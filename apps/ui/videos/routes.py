from flask import render_template, request, jsonify, current_app as app
from . import videos
from pytube import YouTube
from tasks.youtube import download as download_yt, \
                          list_streams as list_yt_streams, \
                          search as search_yt

@videos.route('/')
def index():
    return render_template('videos.html')

@videos.route('/youtube/search')
def search_youtube():
    query = request.args['query']
    data = search_yt(query)
    return jsonify(data)

@videos.route('/youtube/list')
def list_youtube_streams():
    url = request.args['url']
    data = list_yt_streams(url)
    return jsonify(data)

@videos.route('/youtube/download')
def download_youtube():
    url = request.args['url']
    itag = request.args['itag'].rstrip(',')
    app.logger.info("Downloading %s with itag %s" % (url, itag))
    print("Downloading %s with itag %s" % (url, itag))
    # print("Download folder: %s" % app.config['DOWNLOAD_FOLDER'])
    try:
        res = download_yt.delay(url, itag, output_path=app.config['DOWNLOAD_FOLDER'])
        return jsonify({
            'success': True,
            'message': 'Your video is downloading',
            'id': res.id
            # 'output_path': app.config['DOWNLOAD_FOLDER']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'exception_class': type(e).__name__,
            'exception_str': str(e)
        })
