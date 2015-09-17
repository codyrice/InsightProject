__author__ = 'christopherrivera'

########################################################################################################################
# This contains functions classes for scrapping the web or parsing websites
########################################################################################################################

import requests
from bs4 import BeautifulSoup
from os.path import join
from multiprocessing.pool import ThreadPool as Pool
from validators.url import url  as validate_url


def parse_url(url):
    """Parses the string of a url and returns as a string. """
    return url.replace('.', '/').replace('//', '/').replace(':', '').split('/')


def get_host(url):
    """Parses out the host url. """
    protect = '*****'
    url = url.replace('//', protect)  # replace with this string to protect.
    index = url.find('/')
    return url[:index].replace(protect, '//')


def rename_url(url, suffix=''):
    """Renames a url by striping out punctuation and returns string.
    Parameters:
        url (str): the url
        suffix (str): a decorator.
    Returns renamed(str): the processes url"""
    return ''.join([url.replace('/', '').replace('.', '_'), suffix])


def download_html(url, savepath='/Users/christopherrivera/Desktop', suffix='', ext='txt'):
    """Accesses html and downloads to disc.
    Parameters
        """
    # set up a connection

    # error correction if can't download
    try:
        response = requests.get(url).content

    except requests.ConnectionError:
        return

    # build the file name
    filename = rename_url(url, suffix)
    filename = '.'.join([filename, ext])
    filename = join(savepath, filename)

    # save the file to desk
    with open(filename, 'w') as f:
        f.write(response)


def download_multiple_htmls(urls, threads=8):
    pool = Pool(threads)
    pool.map(download_html, urls)


def valid_download_html(url, savepath='/Volumes/Mac/GoGuardianHTMLS', ext='txt'):
    """Validates a url prior to attempting to download
    Parameters:
        url (str): the url name.
    Return:
        tupple: Url (url), downloaded (bool)"""

    # determine if the url is valid.
    old_url = url  # place holder for the url tags

    valid = validate_url(url)

    # if not valid download add an http.
    if not valid:
        url = ''.join(['http://', url])

    # try to validate it.
    try:
        response = requests.get(url).content
    except requests.ConnectionError:  # fails return the tupple
        return old_url, False

    # Build the file name

    filename = rename_url(old_url, suffix='')
    filename = '.'.join([filename, ext])
    filename = join(savepath, filename)

    # print
    print filename

    # save the file to desk
    with open(filename, 'w') as f:
        f.write(response)
    return old_url, True


########################################################################################################################
# Below are functions for getting the links
########################################################################################################################


def get_soup(url):
    """ Opens up with request and remove the style and javascript (do not want)"""

    # get the html and then convert to dom with beautiful soup
    html = requests.get(url).content
    soup = BeautifulSoup(html)

    # strip out the javascript and other stuff
    for script in soup(["script", "style"]):
        script.extract()
    return soup


def get_soup_from_text(text):
    """
    Parameters:
        text (str): location of the website.
    :return: soup
    """
    # open the text and get out the soup
    with open(text, 'r') as f:
        soup = BeautifulSoup(text)

    # strip out the javascript and other stuff
    for script in soup(['script','style']):
        script.extract()
    return soup


def get_links(soup):
    """
    Parameters:
        soup (BeautifulSoup ): the soup.
    Return:
        list of the link text.

    """
    return [link.get_text().replace('\n', '').strip() for link in soup.find_all('a')]


