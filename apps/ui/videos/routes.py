from flask import render_template, request, jsonify, current_app as app
from . import videos
from pytube import YouTube
from tasks.youtube import download as download_yt, \
                          list_streams as list_yt_streams, \
                          search as search_yt
import traceback

@videos.route('/')
def index():
    return render_template('videos.html')

#----------------#
# Youtube routes #
#----------------#
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
def download_youtube_streams():
    url = request.args['url']
    itag = request.args['itag']
    try:
        download_yt(url, itag, output_path=app.config['DOWNLOAD_FOLDER'], filename=request.args.get('filename'))
        return jsonify({
            'download_folder': app.config['DOWNLOAD_FOLDER'],
            'success': True
        })
    except Exception as e:
        tb = traceback.format_exc(e)
        return jsonify({
            'success': False,
            'exception_class': type(e).__name__,
            'exception_str': str(e),
            'traceback': tb
        })
