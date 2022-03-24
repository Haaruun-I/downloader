from linecache import getline
from multiprocessing.sharedctypes import Array
import os, lib.download
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import requests, os.path

from lib.ripper import getFileName

booklist = 'https://ia903001.us.archive.org/view_archive.php?archive=/26/items/tntvillage_118562/Terry%20Pratchett.rar'

def makeSoup(url: str) -> BeautifulSoup:
    """Starts a bs4 parser

    Parameters
    ----------
    url: str
        The url of the page

    """
    return BeautifulSoup(requests.get(url).content, features="html.parser")

def getLinks(url: str):
    return map(lambda e: "https:" + e.attrs['href'], makeSoup(url).select('td > a'))
    
for chapter in filter(lambda e: '02.' in e, getLinks(booklist)):
    file = getFileName(chapter)
    lib.download.downloadFile(chapter, file)