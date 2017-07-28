include config.mk
include init.mk

## getReviews           : scrapes critic reviews by year
.PHONY: getReviews
getReviews: $(SRC_LIB)/processCriticReviews.py #getLinks
	python $(SRC_MAIN)/getMovieReviews.py $(YEAR_START) $(YEAR_END) $(OUT_LINKS) $(OUT_DATA)

## getLinks           : scrapes weblinks to movie's pages by year
.PHONY: getLinks
getLinks: $(SRC_LIB)/mcScrapeLinks.py #init
	python $(SRC_MAIN)/getLinks.py $(YEAR_START) $(YEAR_END) $(OUT_LINKS)

.PHONY: clean
clean:
	rm -rf ./out

.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
