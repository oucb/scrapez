#!/usr/bin/env python
import os
import json

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
