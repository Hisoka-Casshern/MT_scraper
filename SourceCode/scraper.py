import pandas as pd
import numpy as np
from pathlib import Path
import os
import scraper_functions as scrp_func
import time


def scrape():
    """creates a subdir that contains a ScrapedData.csv consisting of
    mmsi and needed ship keywards data if not existant.
    These MMSI are then used to determine routes"""

    "first create a subdirectory containing a .csv file that will"
    "be updated with every number of scrapes such that it preserves already "
    "scraped data in case of an error or webdriver crash"
    _realtive_dir_: str = Path(__file__).parents[0]
    # create subdirectory and switch current working directory to it
    try:
        _scrapedCsvData_dir_: str = "ScrapedData"
        _scrapedCsvData_dir_ = os.path.join(_realtive_dir_, _scrapedCsvData_dir_)
        os.mkdir(_scrapedCsvData_dir_)
    except:
        pass

    "switch current working directory"
    os.chdir(_scrapedCsvData_dir_)

    "if not existant create a ScrapedData.csv to append to"
    if os.path.isfile("ScrapedData.csv") == False:
        scraped_DataFrame = pd.DataFrame(columns=scrp_func.scrapeKeywards)
        scraped_DataFrame.to_csv("ScrapedData.csv", index=False)

    "create a temporary file that will keep all the mmsi checked while scraping"
    "this file will be used to filter the batch of mmsi in case of a crash"
    if os.path.isfile("TempProcessedMMSI.csv") == False:
        mmsi_Track_Temp_DataFrame = pd.DataFrame(columns=["MMSI"])
        mmsi_Track_Temp_DataFrame.to_csv("TempProcessedMMSI.csv", index=False)

    "load the processedMMSI to be used to filter mmsi_list_to_scrape"
    processedMMSI = list(pd.read_csv("TempProcessedMMSI.csv")["MMSI"])

    "get mmsi list to scrape"
    mmsi_list_to_scrape = scrp_func.mmsi_list_to_scrape()
    "filter the mmsi_list_to_scrape"
    mmsi_list_to_scrape = [
        mmsi for mmsi in mmsi_list_to_scrape if mmsi not in processedMMSI
    ]

    "define the number of scrapes to dump to csv"
    numberOfScrapesToDump = 2
    "store current sesion number of scraped"
    currentSessionNumberOfScrapes = 0
    "create a list that will store collect the mmsi"
    mmsiCollectionBuffer: list[int] = []
    "create empty buffers to contain specific scrapes to append in order of scrape"
    "these are filleud up to a lenght of numberOfScrapesToSave and then dumped to"
    "ScrapedData.csv and cleared empty for new batch"
    mmsiBuffer: list[int] = []
    shipNameBuffer: list[str] = []
    shipTypeBuffer: list[str] = []
    shipTypeSpecificBuffer: list[str] = []
    shipLenghtBuffer: list[float] = []
    shipBreadthBuffer: list[float] = []
    shipMaxSpeedBuffer: list[float] = []
    shipAverageSpeedBuffer: list[float] = []

    "create dictionaries used to dump .csv, one for MMSI tracking another for"
    "scraped data"
    mmsiTrack: dict[str:int] = dict.fromkeys(["MMSI"])
    scrapedShipsData: dict[
        str:int, str:str, str:str, str:float, str:float
    ] = dict.fromkeys(
        [
            "MMSI",
            "Ship Name",
            "Ship Type",
            "Ship Type Specific",
            "Lenght",
            "Breadth",
            "Max Speed",
            "Average Speed",
        ]
    )

    "Start The Scrape"
    "to include few last ships if not dump size not equaly divided a trackNumber is used"
    "such that if nedded one more dump process will start collecting only what is left"
    "for this purpuse lastBuffer bool value is used"
    trackNumberOfDumpings: int = 1
    lastBuffer: bool = False
    for mmsiToCollect in mmsi_list_to_scrape:
        "collect mmsi equal to the numberOfScrapesToSave"
        mmsiCollectionBuffer.append(mmsiToCollect)
        "if last batch size not divisible by total size of mmsiToCollect, fill up buffer with"
        "all that is left in the mmsiToCollect list and scrape this last buffer by filling until"
        "last element is same in both lists"
        if trackNumberOfDumpings == (
            int(len(mmsi_list_to_scrape) / numberOfScrapesToDump) + 1
        ):
            if mmsiCollectionBuffer[-1] == mmsi_list_to_scrape[-1]:
                lastBuffer = True
            else:
                continue
        "when collection buffer full start scrape and dump everything scraped"
        if len(mmsiCollectionBuffer) == numberOfScrapesToDump or lastBuffer:
            "increment dump tracking"
            trackNumberOfDumpings += 1
            "scrape individual mmsi in the mmsiCollectionBuffer and dump once finished"
            for mmsi in mmsiCollectionBuffer:
                "firstly check if any ship in databse under the given mmsi and if not"
                "skip this mmsi scrape, also if ship is in the databes check if it is "
                "the only one and if so use ScrapeMarineTrafficWorld immediatly "
                numbersOfShipsInDatabase = (
                    scrp_func.CheckIfShipInMarineTrafficAndIfSoIfOnlyOneExists(mmsi)
                )
                if numbersOfShipsInDatabase == None:
                    "skip this mmsi"
                    continue
                if numbersOfShipsInDatabase == "Only One ship in the database":
                    scrapedData = scrp_func.ScrapeMarineTrafficWorld(mmsi)
                    "Start filling buffers and immediatly go to new mmsi"
                    mmsiBuffer.append(int(scrapedData["MMSI"]))
                    shipNameBuffer.append(scrapedData["Ship Name"])
                    shipTypeBuffer.append(scrapedData["Ship Type"])
                    shipTypeSpecificBuffer.append(scrapedData["Ship Type Specific"])
                    shipLenghtBuffer.append(float(scrapedData["Lenght"] or 0.0))
                    shipBreadthBuffer.append(float(scrapedData["Breadth"] or 0.0))
                    shipMaxSpeedBuffer.append(float(scrapedData["Max Speed"] or 0.0))
                    shipAverageSpeedBuffer.append(
                        float(scrapedData["Average Speed"] or 0.0)
                    )
                    continue

                "in case of more than one ship in Database start scraping by areas"
                "now scrape over only adriatic sea"
                scrapedData = scrp_func.ScrapeMarineTrafficAdriaticSea(mmsi)
                "if ship not found in adriatic sea scrape west mediterranean"
                if scrapedData == None:
                    scrapedData = scrp_func.ScrapeMarineTrafficWestMediterraneanSea(
                        mmsi
                    )
                "if ship not found in west mediterranean scrape east mediterranean"
                if scrapedData == None:
                    scrapedData = scrp_func.ScrapeMarineTrafficEastMediterraneanSea(
                        mmsi
                    )
                "if ship not found in mediterranean scrape whole world"
                if scrapedData == None:
                    scrapedData = scrp_func.ScrapeMarineTrafficWorld(mmsi)

                "Start filling buffers "
                mmsiBuffer.append(int(scrapedData["MMSI"]))
                shipNameBuffer.append(scrapedData["Ship Name"])
                shipTypeBuffer.append(scrapedData["Ship Type"])
                shipTypeSpecificBuffer.append(scrapedData["Ship Type Specific"])
                shipLenghtBuffer.append(float(scrapedData["Lenght"] or 0))
                shipBreadthBuffer.append(float(scrapedData["Breadth"] or 0))
                shipMaxSpeedBuffer.append(float(scrapedData["Max Speed"] or 0.0))
                shipAverageSpeedBuffer.append(
                    float(scrapedData["Average Speed"] or 0.0)
                )

            "dump the mmsi to the TempProcessedMMSI.csv /dumped here in case of crash"
            mmsiTrack["MMSI"] = mmsiCollectionBuffer
            mmsiTrackDataFrame = pd.DataFrame(mmsiTrack)
            mmsiTrackDataFrame.to_csv(
                "TempProcessedMMSI.csv", mode="a", header=False, index=False
            )
            "create a dataFrame used to dump data adressing the already created dictionary"
            "firstly temporary fill the dictionary"
            scrapedShipsData["MMSI"] = mmsiBuffer
            scrapedShipsData["Ship Name"] = shipNameBuffer
            scrapedShipsData["Ship Type"] = shipTypeBuffer
            scrapedShipsData["Ship Type Specific"] = shipTypeSpecificBuffer
            scrapedShipsData["Lenght"] = shipLenghtBuffer
            scrapedShipsData["Breadth"] = shipBreadthBuffer
            scrapedShipsData["Max Speed"] = shipMaxSpeedBuffer
            scrapedShipsData["Average Speed"] = shipAverageSpeedBuffer
            "dump the scraped data to 'ScrapedData.csv'"
            scrapedShipsDataDataFrame = pd.DataFrame(scrapedShipsData)
            scrapedShipsDataDataFrame.to_csv(
                "ScrapedData.csv", mode="a", header=False, index=False
            )
            "get buffer size to printout number of dumped files"
            currentSessionNumberOfScrapes += len(mmsiCollectionBuffer)
            "finally empty buffers"
            mmsiCollectionBuffer.clear()
            mmsiBuffer.clear()
            shipNameBuffer.clear()
            shipTypeBuffer.clear()
            shipTypeSpecificBuffer.clear()
            shipLenghtBuffer.clear()
            shipBreadthBuffer.clear()
            shipMaxSpeedBuffer.clear()
            shipAverageSpeedBuffer.clear()
            "show progress in console"
            print()
            print("DUMPED")
            numberOfScrapedData = len(
                list(pd.read_csv("TempProcessedMMSI.csv")["MMSI"])
            )
            print("Scraped So Far:", numberOfScrapedData)

    "print done"
    print("Done Scraping, Program will close")
    return "Done Scraping"


def ScrapeAgainErroredData():
    """scrapes one more time to go over mmsi data that was corrupted due to unkown error"""

    "switch to ScrapedData directory"
    try:
        pathToScrapeDataCSV = Path(__file__).parent
        pathToScrapeDataCSV = os.path.join(pathToScrapeDataCSV, "ScrapedData")
        os.chdir(pathToScrapeDataCSV)
    except:
        print(
            'Directory "ScrapedData" does not exist, you need to scrape first.\
             \n Program will exit!!'
        )

    "get MMSI list that returned None as ship type and store in a list"
    ScrapedData = pd.read_csv("ScrapedData.csv")
    indexOfNoneShipTypeRowsInScrapedDate = ScrapedData[
        ScrapedData["Ship Type"].isnull()
    ].index
    corruptedDataMMSI: list[int] = list(
        ScrapedData[ScrapedData["Ship Type"].isnull()]["MMSI"]
    )

    "create a backup of ScrapedData.csv then drop every row with corrupted MMSI from DataFrame"
    "finally remove the file and create new updated"
    ScrapedData.to_csv("BackupScrapedData.csv", index=False)
    ScrapedData.drop(indexOfNoneShipTypeRowsInScrapedDate, inplace=True)
    os.remove("ScrapedData.csv")
    ScrapedData.to_csv("ScrapedData.csv", index=False)

    "create a backup of TempProcessedMMSI.csv then drop every row with corrupted MMSI from DataFrame"
    "finally remove the file and create new updated"
    TempProccessedData = pd.read_csv("TempProcessedMMSI.csv")
    TempProccessedData.to_csv("BackupTempProcessedMMSI.csv", index=False)
    TempProccessedData = TempProccessedData[
        ~TempProccessedData["MMSI"].isin(corruptedDataMMSI)
    ]
    os.remove("TempProcessedMMSI.csv")
    TempProccessedData.to_csv("TempProcessedMMSI.csv", index=False)

    "Now use the scrape function over the error MMSI"
    scrapeStatus = scrape()
    time.sleep(1.5)

    "finally clean up ScrapedData.csv of error data that was not corrected"
    "get MMSI list that returned None as ship type and store in a list"
    ScrapedData = pd.read_csv("ScrapedData.csv")
    indexOfNoneShipTypeRowsInScrapedDate = ScrapedData[
        ScrapedData["Ship Type"].isnull()
    ].index

    "create a backup of ScrapedData.csv then drop every row with corrupted MMSI from DataFrame"
    "finally remove the file and create new updated"
    ScrapedData.to_csv("BackupScrapedData.csv", index=False)
    ScrapedData.drop(indexOfNoneShipTypeRowsInScrapedDate, inplace=True)
    os.remove("ScrapedData.csv")
    ScrapedData.to_csv("ScrapedData.csv", index=False)

    return scrapeStatus
