"""
Functions are intended as helpers to be used in conjunction with the "getLinks.py"
script to collect links to movie pages on box office mojo so that you can scrape
data from the individual movie's pages

expected usage:
    from src.lib import mcScrapeLinksLinks

"""

from bs4 import BeautifulSoup as bs
import urllib.request
import requests
import time
from random import randint

def scrapeLinks(iYear):
    sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=10)
sess.mount('http://', adapter)

headers={"User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"}

links = []

baseURL = 'http://www.metacritic.com/browse/movies/score/metascore/year/filtered?year_selected='
iYear = '2014'
iPage = 0

## Main Link Scraper - gets links for all movies in a year
for iPage in range(0,7):
    print('This is page', iPage, 'of', iYear)

    candidateURL = baseURL + iYear + '&page=' + str(iPage)

    # get the web page as lxml data
    response = sess.get(candidateURL, headers = headers)
    page = response.text
    soup = bs(page,"lxml")

    # Find the first movie link's tag
    anchor = soup.find("div", class_="browse_list_wrapper one")
    newref = anchor.find_next(attrs={'class':re.compile(r'metascore_w')})

    # get all movie links on a page and store in links
    for iLink in range(1,101):
        try:
            movie_link = newref.find_next("a").get('href')
            #print(movie_link)
            links.append("http://www.metacritic.com" + movie_link)

            iLink = iLink + 1
            if newref is not None:
                newref = newref.find_next(attrs={'class':re.compile(r'metascore_w')})
            else:
                break
        except:
            pass

    time.sleep(randint(5,15))
    iPage = iPage + 1

# Return the links to the script calling this function
return links
