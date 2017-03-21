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
        meta_Score = metaTable.find_next('span', attrs={'class':re.compile(r'^metascore')}) \
                            .get_text()
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
        meta_nReview_str = metaTable.find_next('span', attrs={'class':re.compile(r'^based_on')})\
                                .get_text()
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

### --- Functions to One Critic Review for an individual movie --- ###

def get_title(soup):
    """
    Takes the lxml source code from the get_soup function and returns the
    title of the movie

    Expected Usage:
        (assumes lxml in variable 'soup')
        output = get_title(soup)
    """
    try:
        title = soup.find('table', attrs={'class':re.compile(r'simple_summary')}) \
                    .find_previous("h1").get_text().lower()
        return title
    except:
        return None

def get_score(refpoint):
    """
    Searches for the next critic review score from a given reference point,
    'refpoint', and returns it

    Expected Usage:
        (a reference point is set - the function 'get_allReviews' manages this)
        output = get_score(refpoint)
    """
    try:
        score = refpoint.find_next('div', attrs={'class': re.compile(r'^metascore')})\
                        .get_text()
        return score
    except:
        return None

def get_critic(refpoint):
    """
    Searches for the next critic from a given reference point,
    'refpoint', and returns it

    Expected Usage:
        (a reference point is set - the function 'get_allReviews' manages this)
        output = get_critic(refpoint)
    """
    try:
        critic = refpoint.find_next('div', attrs={'class': re.compile(r'^metascore')}) \
                        .find_next('span', attrs={'class': re.compile(r'^author')})\
                        .get_text().lower()
        return critic
    except:
        return None

def get_publication(refpoint):
    """
    Searches for the next publication from a given reference point,
    'refpoint', and returns it

    Expected Usage:
        (a reference point is set - the function 'get_allReviews' manages this)
        output = get_publication(refpoint)
    """
    try:
        publication = refpoint.find_next('div', attrs={'class': re.compile(r'^metascore')}) \
                                .find_next('span', attrs={'class': re.compile(r'^source')})\
                                .get_text().lower()
        return publication
    except:
        return None

def get_reviewLink(refpoint):
    """
    Searches for the next link to original website of a critic review from
    a given reference point, 'refpoint', and returns it

    Expected Usage:
        (a reference point is set - the function 'get_allReviews' manages this)
        output = get_reviewLink(refpoint)
    """
    try:
        reviewLink = refpoint.find_next('div', attrs={'class':re.compile(r'^metascore')}) \
                                .find_next("a", attrs={'class':re.compile(r'^read_full')})\
                                .get('href')
        return reviewLink
    except:
        return None

### --- Function to get ALL critic reviews for a given movie --- ###

def get_allReviews(soup, nReview, movieID, title):
    """
    Collects all (nReview) critic reviews for a movie from the webpage source
    stored as in lxml format in the variable soup.

    Returns a dataframe 'df_movie' that has the typical row:
        "movieID", "title", "critic", "publication", "score", "link"
    where there are nReview rows of data

    Expected usage:
        df = get_allReviews(soup, nReview, movieID, title):
    """
    df_movie = pd.DataFrame()

    # start to find reviews by searching for an anchor to start looking from
    anchor = soup.find('h2')
    # this variable will be updated in each iteration to allow us to step through
    # page and get each review
    newref = anchor

    for idx in range(1, int(nReview)+1):
        try:
            # get score
            score = get_score(newref)
            # get author
            author = get_critic(newref)
            # get publication
            publication = get_publication(newref)
            # get review link (incase we want text later - we might if we wanna do bias etc)
            reviewLink = get_reviewLink(newref)

            # write as line of data
            df_critic = pd.DataFrame([[movieID, title, author, publication, score, reviewLink]])

            # update the reference point
            if newref is not None:
                newref = newref.find_next('div',  attrs={'class':re.compile(r'^metascore')})
            else:
                break

            # append that week to existing data
            df_movie = df_movie.append(df_critic, ignore_index=True)
        except:
            break

    # package result and send back
    if not df_movie.empty:
        df_movie.columns = ["movieID", "title", "critic", "publication", "score", "link"]

        return df_movie
    else:
        return None

### --- Function to get ALL information from a page of a given movie --- ###
def scrape_metaScorePage(targetURL, df_metaScore):
    """
    We return all information about review scores for a given movie that is indexed
    by a target URL.

    Outputs:
        * (as a movie specific dataframe): All critic reviews for the movie
        * (as a row of a year specific dataframe): the metaScore Information
                * This row is appended to all metascores for movies released in
                  a year, and is managed by the main script 'main/get_movieReviews'

    Expected Usage:
        df_metaScore = scrape_metaScorePage(targetURL, df_metaScore)
    """
    soup = get_soup(targetURL)

    if soup is not None:
        try:
            # get Meta Information
            meta_Score, meta_nReview = get_allMeta(soup, movieID)
            title = get_title(soup)

            # append meta Information
            df_temp = pd.DataFrame([[movieID, title, meta_Score, meta_nReview]])
            df_metaScore = df_metaScore.append(df_temp, ignore_index=True)

            # get critic information
            if meta_nReview is not None:
                df_movie = get_allReviews(soup, meta_nReview, movieID, title)
            print('Finished collecting reviews from', targetURL )

            # pass back the updated
            return df_metaScore, df_movie
        except:
            print('No soup for', targetURL)
            df_movie = pd.DataFrame()
            return df_metaScore, df_movie
    else:
        print('No soup for', targetURL)
        pass
