# Collecting Data from MetaCritic

This repo contains scripts to get information from the metacritic website.

Currently we scrape the following information:

* e movie's metascore and number of reviews
* all critic review scores and links to their full review

## Ways to Execute

Set up is to get information for a range of years.
These years are set in the config.mk file as

```bash
YEAR_START = 2000
YEAR_END   = 2015
```

These numbers can be updated, but will re-run all of the code next time you execute a make call.

### 1. Do Everything At once
This will create the necessary directories in the output folder to store the data,
get links to movies sorted by year, and then loop through the links and get all reviews

```bash
make getReviews
```

### 2. Go Step by Step

#### (a) Initialize directories for output

```bash
make init
```

#### (b) Scrape the links for all movies by year and store the resulting links

```bash
make getLinks
```

#### (c) Scrape Metascore and movie reviews

* All meta scores for a year of movies are stored in a single csv file
* Each movie has a separate csv (in a folder indexing year of release) that contains all critic review scores

```bash
make getReviews
```

## Other Info:

* Assumes that you have make installed on your machine - default for Unix system
* Tested using Python 3.5.2 (64bit)
