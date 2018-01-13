from . import files
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from celery.result import AsyncResult
import pprint, logging

app = Flask(__name__)
log = logging.getLogger(__name__)

ROOT_DIR = 'C:/Users/JahMyst/Desktop/scrapex'

@files.route('/')
def index():
    return render_template('index.html')

@files.route('/query', methods=['POST'])
def query():
    from scrape import scrape_files
    log.info("-> Received query")
    url_data = request.get_json()
    log.info("-> Query data: %s" % pprint.pformat(url_data))
    if not url_data:
        return jsonify({
            'message': 'No URL data'
        })
    if 'name' not in url_data:
        url_data['name'] = url_data['url']
    if 'recurse' not in url_data:
        url_data['recurse'] = True
    if 'subfolders' not in url_data:
        url_data['subfolders'] = True
    url_data['extensions'] = url_data['extensions'].split(',')
    log.info("-> Creating Celery task ...")
    r = scrape_files.delay([url_data], ROOT_DIR)
    msg = "Task '%s' created" % r.id
    log.info("-> " + msg)
    resp = {
        'message': msg,
        'id': r.id
    }
    log.debug(resp)
    return jsonify(resp)

@files.route('/list', methods=['GET'])
def list_files():
    from utils import get_dir_tree
    files = get_dir_tree(ROOT_DIR)
    log.info(pprint.pformat(files))
    return jsonify(files)

# @files.route('/task/<id>')
# def task_info(id):
#     res = AsyncResult(id)
#     log.info("-> Polling task: %s" % res)
#     resp = {
#         'result': None,
#         # 'ready': res.ready(),
#         'status': res.status,
#         'id': res.task_id
#     }
#     if res.ready():
#         resp['result'] = res.get()
#     return jsonify(resp)
