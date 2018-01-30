import urllib2
from bs4 import BeautifulSoup
import requests
import os.path
from urlparse import urlparse
from time import time
import logging
import requests
import pprint
from celeryapp import app
from celery import group
log = logging.getLogger(__name__)

DEFAULT_RECURSE_DEPTH = 4

def get_links(root_url, extensions, links={}, visited=[], count={}, auth=(), recurse=True, min_depth=0, max_depth=2):
    """Crawl links to files of certain extensions from root_url.

    Args:
        root_url (str): The URL to crawl from.
        extensions (list): A list of extensions (pdf, csv, doc, ...) to search for.
        links (dict): Dict of links indexed by extension.
        visited (list): List of already visited links.
        count (dict): Dict of link counts indexed by extension.
        auth (tuple): Authentication tuple if required
        recurse (bool): Recurse through links on webpage.
        min_depth (int): The minimum recurse depth.
        max_depth (int): The maximum recurse depth.

    Returns:
        links (dict): Dict of file links indexed by extension.

    Example:
        >>> get_links('http://example.com', ['pdf', 'doc'])
        {
            'pdf': [
                'http://example.com/path/to/a.pdf',
                'http://example.com/path/to/b.pdf'
            ],
            'doc': [
                'http://example.com/path/to/a.doc',
                'http://example.com/path/to/b.doc'
            ]
        }
    """
    start = time()
    log.info("-" * 60)
    log.info("-> Processing %s" % root_url)
    log.debug("Extensions: %s" % extensions)
    if root_url in visited:
        return {}
    parsed_root_uri = urlparse(root_url)
    domain_root = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_root_uri)
    try:
        if auth and 'username' in auth and 'password' in auth:
            log.info("-> Auth is %s / %s" % (auth['username'], auth['password']))
            auth = (auth['username'], auth['password'])
        html = requests.get(root_url, auth=auth).content
    except (requests.exceptions.HTTPError, requests.exceptions.SSLError, ValueError) as e:
        log.error("Failed to hit '%s'. Exception: %s" % (root_url, str(e)))
        log.exception(e)
        return {}
    sopa = BeautifulSoup(html, "html.parser")
    if not sopa:
        return {}

    # If root ext is a file we want, add the link
    ext = root_url.split('.')[-1]
    log.debug("Root ext: %s" % ext)
    if ext in extensions:
        log.info('Found ".%s" file at %s' % (ext, root_url))
        if ext in links:
            links[ext].append(root_url)
            visited.append(root_url)
            count[ext] += 1
        else:
            links[ext] = [root_url]
            count[ext] = 1
        return links
    else:
        # Iterate through links on current page
        all_links = sopa.find_all('a')
        log.info("\t-> %s links found" % len(all_links))
        for link in all_links:
            try:
                url = link.get('href')
                if url is None or ' ' in url or '<' in url or '>' in url or url.startswith('javascript') or url.isdigit():
                    continue
                if url.startswith('//'):
                    url = url.replace('//', 'http://')
                if url.startswith('/'):
                    url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_root_uri) + url
                if not url.startswith('http') or url.startswith('https'): # partial url
                    url = '{uri.scheme}://{uri.netloc}/{partial_url}'.format(uri=parsed_root_uri, partial_url=url)
                if '?' in url:
                    url = url.split('?')[0]
                if '#' in url:
                    url = url.split('#')[0]

                log.info("\t-> %s" %  url)
                parsed_uri = urlparse(url)
                domain_cur = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                # print("Current domain: %s" % domain_cur)
                if domain_cur != domain_root:
                    log.warning("\t\t-> Domain '%s' is external." % domain_cur)
                    # continue
            except Exception as e:
                log.error("\t\t->Couldn't process URL")
                log.exception(e)
                continue
            if url in visited:
                log.info("\t\t-> Already visited. Skipping.")
                continue
            else:
                visited.append(url)

            # Add links to mapping / count / visited
            ext = url.split('.')[-1]
            depth = len(url.split('/')[2:-1])
            min_depth = len(root_url.split('/')[2:-1])

            # Log some stuff
            log.debug("\t\t-> Current ext: %s" % ext)
            log.debug("\t\t-> Depth: %s" % depth)
            log.debug("\t\tCurrent min_depth: %s" % min_depth)
            log.debug("\t\tCurrent max_depth: %s" % max_depth)

            # If URL extension is in our list, add it to `links`
            if ext in extensions:
                log.info('\t\t-> Found ".%s" file. Adding.' % (ext))
                if ext in links:
                    links[ext].append(url)
                    visited.append(url)
                    count[ext] += 1
                else:
                    links[ext] = [url]
                    count[ext] = 1

            # Calculate depth and recurse through sublinks
            if recurse is True and min_depth <= depth <= max_depth:
                log.info("\t\t-> Crawlink links from '%s'. Depth: %s <= [%s] <= %s" % (url, min_depth, depth, max_depth))
                get_links(url, extensions, links, min_depth=min_depth, max_depth=max_depth, auth=auth)
            else:
                log.info("\t\t-> Depth reached. Not crawlink sublinks.")

    if not count:
        log.info("-> No file found in %s for extensions [%.4f s]" % (root_url, time() - start))
    for ext, num in count.items():
        log.info("-> Found %s files with extension '.%s' from %s [%.4f s]" % (num, ext, root_url, time() - start))
    return links

def download_all(links, root_dir, subfolders=False):
    """Takes a dict of links and download them into appropriate directories (also
    create subdirectories if missing).

    Example:
        >>> links = {
        ...     'pdf': ['http://example.com/path/to/file.pdf'],
        ...     'py': [
        ...         'http://example.com/path/to/a/script.py',
        ...         'http://example.com/path/to/b/script.py'
        ...     ]
        ... }
        >>> download_all(links, '/tmp/download_folder', subfolders=False)

        Will create following structure:
            - example.com
                - path
                    - to
                        -
    """
    start = time()
    ensure_dir(root_dir)
    paths = []
    for ext, urls in links.items():
        try:
            download_dir = root_dir + '/' + ext
            ensure_dir(download_dir)
            for url in urls:
                path = download_single(url, download_dir, subfolders)
                paths.append(path)
        except Exception as e:
            log.error("-> Failed to download %s urls" % len(urls))
            log.exception(e)
    log.info("-> Downloaded %s links [%4f s]" % (len(paths), time() - start))
    log.debug("-> Saved: %s" % pprint.pformat(paths))
    return paths

def download_single(url, download_dir, subfolders=False):
    """Download file at `url` to `download_dir`.
    If url has a path and `subfolders` is set to True, the method will create
    the subdirectories locally as well.

    Args:
        url (str): The URL to the file to download.
        download_dir (str): The path to the download directory.
        subfolders (bool, optional) [False]: Create subfolders to organize crawled files.

    Returns:
        str: The path the download file.
    """
    start = time()
    content = requests.get(url).content
    split_url = url.split('/')
    filename = split_url[-1]
    if subfolders:
        path_parts = split_url[2:-1]
        # log.info("Path parts: %s" % path_parts)
        current_dir = download_dir
        for p in path_parts:
            current_dir += '/' + p
            ensure_dir(current_dir)
        filepath = download_dir + '/' + '/'.join(path_parts) + '/' + filename
    else:
        filepath = download_dir + '/' + filename
    with open(filepath, 'wb') as f:
        f.write(content)
    log.info("-> Saved '%s' downloaded from %s [%4f s]" % (filepath, url, time() - start))
    return filepath

def ensure_dir(directory):
    if not os.path.exists(directory):
        log.info("-> Creating %s" % directory)
        os.makedirs(directory)
    # log.info("Ensured '%s' is created" % (directory))

@app.task()
def scrape_files(urls, root_dir):
    """Scrapes a list of URLs (see `scrape_files_single`).
    Creates a group of Celery task.
    """
    log.info("-> Processing %s URLs" % (len(urls)))
    g = group(scrape_files_single.s(u, root_dir) for u in urls)
    return g.delay()

@app.task()
def scrape_files_single(url, root_dir):
    """Scrapes a URL for files of chosen extensions and return a list of
    downloaded paths.

    Args:
        url (dict): The URL configuration:
            * url (str): The website URL to crawl.
            * extensions (list): A list of extensions to crawl for.
            * recurse (bool) [False]: Recurse through links contained in page.
            * recurse_depth (int): The recurse depth (how many links to follow)
            * subfolders (bool) [True]: Wether to create subfolders

    Returns:
        list: A list of paths of download files.
    """
    links = get_links(
        root_url=url['url'],
        extensions=url['extensions'],
        recurse=url['recurse'],
        max_depth=url.get('recurse_depth', DEFAULT_RECURSE_DEPTH),
        auth=url.get('auth'))
    log.debug("-> Links: %s" % pprint.pformat(links))
    fpaths = download_all(links, root_dir, subfolders=url['subfolders'])
    log.debug("-> Paths: %s" % pprint.pformat(fpaths))
    return fpaths

if __name__ == '__main__':
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.INFO)
    ROOT_DIR = 'C:/Users/JahMyst/Desktop/scrapex'
    TEST_URLS = [
        # {
        #     'name': 'AC Jan MPSI Website',
        #     'url': 'http://ac.jan.free.fr',
        #     'recurse': True,
        #     'subfolders': True,
        #     'extensions': ['pdf', 'py', 'ipynb']
        # },
        # {
        #     'name': 'KosarKairanvibooks',
        #     'url': 'https://archive.org/download/KosarKairanvibooks',
        #     'recurse': True,
        #     'subfolders': True,
        #     'extensions': ['pdf', 'xml', 'zip']
        # },
        # {
        #     'name': 'Public Literature',
        #     'url': 'http://publicliterature.org',
        #     'recurse': True,
        #     'recurse_depth': 4,
        #     'subfolders': True,
        #     'extensions': ['pdf']
        # },
        # {
        #     'name': 'Liens physique MP',
        #     'url': 'http://www.thierryalbertin.com/mathematiques.php',
        #     'recurse': True,
        #     'recurse_depth': 4,
        #     'subfolders': True,
        #     'extensions': ['doc']
        # },
        # {
        #     'name': 'Navistar',
        #     'url': 'http://navistar.kmsihosting.com/ihtml/application/student/interface.id/index.htm',
        #     'recurse': True,
        #     'recurse_depth': 4,
        #     'subfolders': True,
        #     'extensions': ['pdf'],
        #     'auth': {
        #         'username': 'uti1031511',
        #         'password': 'navistar'
        #     }
        # },
    ]
    scrape_files.delay(TEST_URLS, ROOT_DIR)
