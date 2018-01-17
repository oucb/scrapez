#!/usr/bin/env python
import os
import json
import logging

log = logging.getLogger(__name__)

def register_blueprints(app, blueprints):
    """Register all Flask blueprints with our Flask app.

    Args:
        app: The Flask application.
        blueprints (list): A list of tuple (blueprint, path).
    """
    for bp, path in blueprints:
        try:
            app.register_blueprint(bp, url_prefix=path)
            log.info("Blueprint registered: %s --> %s" % (bp, path))
        except Exception as e:
            log.error("Error registering blueprint %s --> %s" % (bp, path))
    log.debug("Registered %s blueprints" % len(blueprints))
    log.info("URL Map: %s" % app.url_map)

def register_extensions(app, extensions):
    """Register all Flask extensions with our Flask app.

    Args:
        app: The Flask application.
        blueprints (list): A list of tuple (blueprint, path).
    """
    for e in extensions:
        if isinstance(e, tuple):
            log.info("Registering extension: %s" % e[0])
            log.info("Extension config: %s" % e[1])
            kwargs = e[1]
            e = e[0]
        else:
            log.info("Registering extension: %s" % e)
            kwargs = {}
        e.init_app(app, **kwargs)

class Node:
    def __init__(self, id, text, parent):
        self.id = id
        self.text = text
        self.parent = parent

    def is_equal(self, node):
        return self.id == node.id

    def as_json(self):
        return dict(
            id=self.id,
            parent=self.parent,
            text=self.text
        )

def get_nodes_from_path(path):
    nodes = []
    path_nodes = path.split(os.sep)
    for idx, node_name in enumerate(path_nodes):
        parent = None
        node_id = os.sep.join(path_nodes[0:idx+1])
        if idx != 0:
            parent = os.sep.join(path_nodes[0:idx])
        else:
            parent = "#"
        nodes.append(Node(node_id, node_name, parent))
    return nodes

def get_dir_tree(root_dir):
    unique_nodes = []
    print("Root: %s" % root_dir)
    for root, dirs, files in os.walk(root_dir, topdown=True):
        print("Dir: %s" % root)
        # root = root.replace('\\', '/')
        root = root.replace('/', '\\')
        for name in files:
            print ("Root: %s | File: %s" % (root, name))
            path = os.sep.join([root, name])
            nodes = get_nodes_from_path(path)
            for node in nodes:
                if not any(node.is_equal(unode) for unode in unique_nodes):
                    unique_nodes.append(node)
    return [node.as_json() for node in unique_nodes]
