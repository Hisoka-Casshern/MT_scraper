import scraper
import postScrapeProcessing

"""main scraper function, uses while loop to counter crashes
due te web instabilities, scrape function once finished
returns "Done Scraping"""

if __name__ == "__main__":
    "scrape"
    scrapeStatus: str = "Not Done Scraping"
    while scrapeStatus != "Done Scraping":
        try:
            scrapeStatus = scraper.scrape()
        except:
            pass

    "one more scrape for coerupted data"
    scrapeStatus: str = "Not Done Scraping"
    while scrapeStatus != "Done Scraping":
        try:
            scrapeStatus = scraper.ScrapeAgainErroredData()
        except:
            pass

    "clean up .csv with further proccessing"
    postScrapeProcessing.CleanUpScrapeData()
    postScrapeProcessing.AugmentDataAndRemoveNonShips()
