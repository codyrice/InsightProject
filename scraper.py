__author__ = 'christopherrivera'

########################################################################################################################
# This contains functions classes for scrapping the web or parsing websites
########################################################################################################################

import requests
from bs4 import BeautifulSoup
from os.path import join
from multiprocessing.pool import ThreadPool as Pool
from validators.url import url as validate_url
import string

import pycurl
import StringIO
from requests.exceptions import Timeout, ReadTimeout, TooManyRedirects, ConnectionError


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


def valid_download_html(url, savepath='/Volumes/Mac/GoGuardianHTMLS', ext='txt', validate=False):
    """Validates a url prior to attempting to download
    Parameters:
        url (str): the url name.
    Return:
        tupple: Url (url), downloaded (bool)"""

    # determine if the url is valid.
    old_url = url  # place hoder for the url tags

    # If validate true, validate the url and add a protocol if needed.
    if validate:
        valid = validate_url(url)
        # if not valid download add an http.
        if not valid:
            url = ''.join(['http://', url])

    # try to validate it.
    try:
        response = requests.get(url, timeout=(10, 10)).content  # allow to time out for only 10 seconds.
    except (Timeout, ReadTimeout, TooManyRedirects, ConnectionError):  # fails return the tupple
        return old_url, False

    # Build the file name

    filename = rename_url(old_url, suffix='')
    filename = '.'.join([filename, ext])
    filename = join(savepath, filename)

    # save the file to desk
    with open(filename, 'w') as f:
        f.write(response)
    return old_url, True


def download_multiple_html_with_pycurl(urls, savepath='/Volumes/Mac/Insight/GoGuardianHTMLS-9-17-2015-b', ext='txt'):
    """Takes a list of urls and downloads and writes a save path.
    Parameters:
        urls (list): list of url strings
        savepath (str): path to save location
        ext (str) extension to the string
    Returns None
    """

    # set up a curl object and set up some options
    curl = pycurl.Curl()
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, 5)

    # use a for loop to get the urls and download
    for url in urls:
        # place holder for the old url
        old_url = url

        # validate the url and append and http: to it if needed
        valid = validate_url(url)

        # if not add an http.
        if not valid:
            url = ''.join(['http://', url])

        # set the url
        curl.setopt(pycurl.URL, url)

        # try to download it and save it.
        try:
            # create a new string io object and set it.
            b = StringIO.StringIO()
            curl.setopt(pycurl.WRITEFUNCTION, b.write)

            # perform the getting and streaming
            curl.perform()
            response = b.getvalue()
            b.close()

            # handle download
            # Build the file name
            filename = rename_url(old_url, suffix='')
            filename = '.'.join([filename, ext])
            filename = join(savepath, filename)

            # save the file
            with open(filename, 'w') as f:
                f.write(response)
        except:
            pass

    curl.close()


def make_url_valid(url):
    """Validates a url, and add an http protocol if not valid.
    Parameters:
        url (str): a url string.
    Return:
        new url(str)
    """
    valid = validate_url(url)
    # if not valid download add an http.
    if not valid:
        url = ''.join(['http://', url])
    return url


########################################################################################################################
# Below are functions for using Beatiful soup.
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
    Extracts soup from the text and removes script and style.
    Parameters:
        text (str): location of the website.
    :return: soup
    """
    # open the text and get out the soup
    with open(text, 'r') as f:
        soup = BeautifulSoup(f)

    # strip out the javascript and other stuff
    for script in soup(['script', 'style']):
        script.extract()
    return soup


def get_tag_text(soup, tag='a', count_tags=True):
    """
    Parameters:
        soup (BeautifulSoup ): the soup.
        tag (str): the tag to get
        count_tags (bool): count the number of tags if true.
    Return:
        list of the link text.
    """
    # search for all the tags, get the text and place in a list.
    tags = [t.get_text().strip() for t in soup.find_all(tag)]

    # convert to a large string
    text = ' '.join(tags)

    # do encode decode to remove all the unusual text
    text = text.encode('utf8').decode('unicode_escape').encode('ascii', 'ignore')

    # get rid of the punctuation
    for p in string.punctuation:
        text = text.replace(p, ' ')
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    # Count the tags if need and return.
    if count_tags:
        number = len(tags)  # get the number
        return text, number
    else:
        return text


def get_paragraphs(soup, count_tags=True):
    """ gets the body text"""
    tag = 'p'
    return get_tag_text(soup, tag, count_tags)


def get_title(soup, count_tags=True):
    """ gets the body text"""
    tag = 'title'
    return get_tag_text(soup, tag, count_tags)


def get_links(soup, count_tags=True):
    """ gets the body text"""
    tag = 'a'
    return get_tag_text(soup, tag, count_tags)


def get_images(soup, count_tags=True):
    """ gets the body text"""
    tag = 'img'
    return get_tag_text(soup, tag, count_tags)


def get_meta(soup, count_tags=True):
    """ gets the body text"""
    tag = 'meta'
    return get_tag_text(soup, tag, count_tags)


def get_header(soup, count_tags=True):
    """ gets the body text"""
    tag = 'header'
    return get_tag_text(soup, tag, count_tags)


def scrape_all_text(text):
    """ Uses beautiful soup to scrape all the text from an html text document.
    Parameters. This gets the text for the paragraphs, title, links, img, meta data and header.
        text (str): Path to the text file (html)
    Returns:
        (str): a string with all the text for parsing later by sklearn.
    """

    soup = get_soup_from_text(text)

    # search for all the tags, get the text and place in a list.
    def get_tag_text(tag):
        # internal function to get the text for a given text and return as a text.
        return ' '.join([t.get_text() for t in soup.find_all(tag)])

    # scrape for the desired text tag and join.
    tags = [get_tag_text(tagd) for tagd in ['p', 'title', 'a', 'img', 'meta', 'header']]
    text = ' '.join(tags)

    # do encode decode to remove all the unusual text
    text = text.encode('utf8').decode('unicode_escape').encode('ascii', 'ignore')

    # get rid of the punctuation
    for p in string.punctuation:
        text = text.replace(p, ' ')

    # replace some unwanted stuff.
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    return text


remove_strings = ' '.join([string.punctuation,'1234567890'])

def scrape_text_and_count_tags(text):
    """ Uses beautiful soup to scrape all the text from an html text document.
    Parameters. This gets the text for the paragraphs, title, links, img, meta data and header. It also
    counts the number of tags.  
        text (str): Path to the text file (html)
    Returns:
        (str): a string with all the text for parsing later by sklearn.
    """

    soup = get_soup_from_text(text)
    text = soup.get_text()

    # Coun the then number of tags
    def get_tag_count(tag):
        # Counts the number of tags
        return len(soup.find_all(tag))

    tags = ['p', 'title', 'a', 'img', 'meta', 'header']
    counts = [get_tag_count(t) for t in tags]

    # do encode decode to remove all the unusual text
    text = text.encode('utf8').decode('unicode_escape').encode('ascii', 'ignore')

    # get rid of the punctuation

    for p in remove_strings:
        text = text.replace(p, ' ')

    # replace some unwanted stuff.
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text_len = len(text.split())
    return text, counts, text_len
