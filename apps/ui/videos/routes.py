from flask import render_template, request, jsonify, current_app as app
from . import videos
from pytube import YouTube
from tasks.youtube import download as downlad_yt, \
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
def download_youtube_streams():
    url = request.args['url']
    itag = request.args['itag']
    try:
        download_yt(url, itag, app.config['DOWNLOAD_FOLDER'])
        return jsonify({
            'success': True,
            'output_path': output_path
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'exception_class': type(e).__name__,
            'exception_str': str(e)
        })
