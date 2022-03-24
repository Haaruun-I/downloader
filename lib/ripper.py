from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import requests, os.path

def makeSoup(url: str) -> BeautifulSoup:
    """Starts a bs4 parser

    Parameters
    ----------
    url: str
        The url of the page

    """
    return BeautifulSoup(requests.get(url).content, features="html.parser")

def getTitle(url: str) -> str:
    """Get the title of the book
    
    Parameters
    ----------
    url: str
        The url of the page


    """
    return makeSoup(url).title.getText().split(" - ")[0]

def getFileName(url: str) -> str:
    """Get filename from url

    Parameters
    ----------
    url: str
        The url of the file
    
    """
    return os.path.basename(unquote(urlparse(url).path))



def getPages(url: str) -> list[str]:
    """Gets a list of urls to each page of the audiobook
    
    Parameters
    ----------
    url: str
        The url of the audiobook

    """

    # Start the document parser
    soup = makeSoup(url)

    # Append all the pages to the list
    pages = [url]
    for page in soup.select('a.post-page-numbers'):
        pages.append(page.attrs['href'])

    # Return the list after taking out duplicates 
    # (Audiobook site as each page listed twice, plus prev & next buttons)
    return list(set(pages))

def getChaptersOnPage(url: str) -> list[str]:
    """Gets a list of chapter on each page of the audiobook
    
    Parameters
    ----------
    url: str
        The url of the page

    """

    # Start the document parser
    soup = makeSoup(url)

    # Append the url of each chapter to the list
    chapters = []
    for chapter in soup.select('source[type="audio/mpeg"]'):
        chapters.append(chapter.attrs['src'])

    return chapters

def getChapters(url: str) -> list[str]:
    """Gets a list of each chapter of the audiobook
    
    Parameters
    ----------
    url: str
        The url of the audiobook

    """

    # Get a list of all the sites pages
    pages = getPages(url)


    # Run each page through the chapter parser
    chapterLists = []
    chapters = []

    for page in pages:
        chapterLists.append(getChaptersOnPage(page))

    # Flatten the list
    for sublist in chapterLists:
        for chapter in sublist:
            chapters.append(chapter)
        

    return chapters
