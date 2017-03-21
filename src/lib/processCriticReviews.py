"""
This collection of functions scrapes metaScore and critic reviews
from a film's 'critic-reviews' page on the metacritic website.

Last Update: March, 2017
"""

# load packages - some might be obselete
import requests
from bs4 import BeautifulSoup
import re
import dateutil.parser
from string import ascii_uppercase
import pandas as pd
import time
import urllib.request
import csv
import requests

##-- Functions -- ##

### --- General Helper Functions --- ###
def get_soup(targetURL):
    """
    Take a URL and return the page source info as lxml

    Expected Usage:
        soup = get_soup(someURL)
    """
    sess = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=10)
    sess.mount('http://', adapter)
    headers={"User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"}

    try:
        response = sess.get(targetURL, headers = headers)
        page = response.text
        soup = BeautifulSoup(page,"lxml")
        return soup
    except:
        print('Cannot establish connection to', targetURL)
        return None

### --- Functions to get the metascore information --- ###

def get_metaTable(soup):
    """
    Takes the lxml source code from the get_soup function and returns the
    table that stores the metaScore information

    Expected Usage:
        (assumes lxml in variable 'soup')
        output = get_metaTable(soup)
    """
    try:
        metaTable = soup.find('table', attrs={'class':re.compile(r'score_wrapper')})
        return metaTable
    except:
        return None

def get_metaScore(metaTable):
    """
    Returns the metaScore from the table storing all meta information

    Expected Usage:
        (assumes metaTable in variable 'metaTable')
        output = get_metaScore(metaTable)
    """
    try:
        meta_Score = metaTable.find_next('span', attrs={'class':re.compile(r'^metascore')}).get_text()
        return meta_Score
    except:
        return None

def get_nReviews(metaTable):
    """
    Returns the number of reviews stored on the page from the table storing
    all meta information

    Expected Usage:
        (assumes metaTable in variable 'metaTable')
        output = get_nReviews(metaTable)
    """
    try:
        meta_nReview_str = metaTable.find_next('span', attrs={'class':re.compile(r'^based_on')}).get_text()
        meta_nReview = re.findall(r'\b\d+\b', meta_nReview_str)[0]
        return meta_nReview
    except:
        return None

def get_allMeta(soup, movieID):
    """
    Returns the metaScore and number of reviews stored on the webpage from
    the lxml markup

    Expected Usage:
        (assumes lxml in variable 'soup')
        metaScore, nReviews = get_nReviews(metaTable)
    """
    metaTable = get_metaTable(soup)

    if metaTable is not None:
        meta_Score = get_metaScore(metaTable)
        meta_nReview = get_nReviews(metaTable)
        return meta_Score, meta_nReview
    else:
        print('No MetaInfo for', movieID)
