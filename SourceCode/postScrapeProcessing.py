import pandas as pd
from pathlib import Path
import os
import random
from shipHierarchy import shipTypeHierarchy


def CleanUpScrapeData():
    """Removes every row in ScrapedDate csv that contains 0 lenght ,'-' shipType
    and 'Unspecified' or '-' Ship Type Specific with first removing an empty " " space
    in front of every string data that is a byproduct of scrape from marineTraffic
    (if server changes string input data this should be changed appropriately).
    Ships that do have '-' shipType and '-'/Unspecified ShipTypeSpecific but valid
    dimensions are given 'Other' as ShipType and ShipTypeSpecific classification.
    Remaining ships with '-' ShipType but valid ShipTypeSpecific are
    given shiptype defined as in shipTypeHeirarchy."""

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

    "open file"
    ScrapedData = pd.read_csv("ScrapedData.csv")

    "remove a space in front of each word that is a byproduct of scrape on marineTraffic"
    "could be changed in future if code on website changes"
    "check if backup was created to keep track if this function was run already"
    if os.path.isfile("BackupBackupScrapedData.csv") == False:
        ScrapedData["Ship Name"] = ScrapedData["Ship Name"].str[1:]
        ScrapedData["Ship Type"] = ScrapedData["Ship Type"].str[1:]
        ScrapedData["Ship Type Specific"] = ScrapedData["Ship Type Specific"].str[1:]

    "get indeces of MMSI that returned None as ship type ,0 lenght and Unspecified or "
    "'-' Ship Type Specific "
    indecesOfShipsToRemove = ScrapedData[
        (ScrapedData["Lenght"] == 0.0)
        & (ScrapedData["Ship Type"] == "-")
        & (
            (ScrapedData["Ship Type Specific"] == "Unspecified")
            | (ScrapedData["Ship Type Specific"] == "-")
        )
    ].index

    "create a backup of ScrapedData.csv then drop every row with corrupted MMSI from DataFrame"
    if os.path.isfile("BackupBackupScrapedData.csv") == False:
        ScrapedData.to_csv("BackupBackupScrapedData.csv", index=False)
    ScrapedData.drop(indecesOfShipsToRemove, inplace=True)
    "reset indeces"
    ScrapedData.reset_index(drop=True)

    "get indeces of ships with valid dimensions but error ShipType/Specific data"
    indecesOfShipsToAssignAsOthers = ScrapedData[
        (ScrapedData["Ship Type"] == "-")
        & (
            (ScrapedData["Ship Type Specific"] == "Unspecified")
            | (ScrapedData["Ship Type Specific"] == "-")
        )
    ].index

    "Assign ShipType/Specific as Other"
    ScrapedData.loc[
        indecesOfShipsToAssignAsOthers, ["Ship Type", "Ship Type Specific"]
    ] = "OTHER"

    "get remaining ships with '-' as ShipType"
    indecesOfRemainingShipsWithInvalidShipTypeButValidShipTypeSpecific = ScrapedData[
        ScrapedData["Ship Type"] == "-"
    ].index

    "assign ShipType based on ShipTypeSpecific"
    "iterate the indeces of ships"
    for shipIndex in indecesOfRemainingShipsWithInvalidShipTypeButValidShipTypeSpecific:
        "get shipType that corresponds to the ShipTypeSpecific of the ship"
        "at the current index using shipHierarchy"
        currentShipTypeSpecific = ScrapedData.at[shipIndex, "Ship Type Specific"]
        shipTypeToAssign: str = ""
        foundShipType: bool = False
        for globalShipType in shipTypeHierarchy.keys():
            if foundShipType:
                break
            for shipType in shipTypeHierarchy[globalShipType]:
                if foundShipType:
                    break
                for shipTypeSpecific in shipTypeHierarchy[globalShipType][shipType]:
                    "check for matching shipTypeSpecific"
                    if shipTypeSpecific == currentShipTypeSpecific:
                        shipTypeToAssign = shipType
                        foundShipType = True
                        break
        "assign ship type"
        ScrapedData.at[shipIndex, "Ship Type"] = shipTypeToAssign

    "save the new updated csv"
    ScrapedData.to_csv("ScrapedData.csv", index=False)

    "printout return"
    print("Removed corrupted mmsi")
    print("Given 'Other' classification to ships with valid dimensions.")
    print("Augmented remaining '-' ship types with valid ship type")


def AugmentDataAndRemoveNonShips():
    """this function augments the scraped data as it contains mismatched and erroneus data.
    Ships are further categorised (added new csv column) by having a global shipType
    as defined in shipHierarchy.py, ships with mismatched shipType classification as
    defined in said .py file are cleaned by using their ShipTypeSpecific as a base upon which
    their ShipType is reassigned but for special case of 'INLAND, UNKNOWN' ShipTypeSpecific
    these ships are given ShipTypeSPecific based on their ShipType.
    Afterwards based on ShipType, ships are given GlobalShipType.
    Remaining ships with 0 lenght and breadth are given lenght and breadth
    randomly of another ships with same ShipTypeSpecific
    Lastly any mmsi with shipType that is not in shipTypeHierarachy is removed"""

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

    "open file"
    ScrapedData = pd.read_csv("ScrapedData.csv")

    "shipTypeHierarchy is defined on all uppercase so first every ShipType/Specific"
    "entry ScrapeData is raised to uppercase"
    ScrapedData["Ship Type"] = ScrapedData["Ship Type"].str.upper()
    ScrapedData["Ship Type Specific"] = ScrapedData["Ship Type Specific"].str.upper()

    "search for ShipTypeSpecific not defined in shipTypeHierarchy"
    "first get the list of all defined shipTypeSpecifics"
    listOfAllShipTyeSpecific: list[str] = []
    for globalShipType in shipTypeHierarchy.keys():
        for shipType in shipTypeHierarchy[globalShipType]:
            for shipTypeSpecific in shipTypeHierarchy[globalShipType][shipType]:
                listOfAllShipTyeSpecific.append(shipTypeSpecific)

    "give 'INLAND, UNKNOWN' ShipTypeSpecific special case type based on their ShipType"
    "indeces of 'INLAND, UNKNOWN' ships "
    indecesOfINLANDUNKNOWNShipTypeSpecific = ScrapedData[
        ScrapedData["Ship Type Specific"] == "INLAND, UNKNOWN"
    ].index
    "assign them ShipTypeSpecific"
    for row in ScrapedData.itertuples():
        if row.Index in indecesOfINLANDUNKNOWNShipTypeSpecific:
            ScrapedData.at[row.Index, "Ship Type Specific"] = ScrapedData.at[
                row.Index, "Ship Type"
            ]

    "get indeces of not defined shipTypeSpecifics"
    "here print() exit() comments can be used to further improve shipTypeHierarchy"
    indecesOfMMSIsWithShipTypingNotInShipTypeHierarchy: list[int] = []
    for row in ScrapedData.itertuples():
        currentRowIndex = row.Index
        currentRowShipTypeSpecific = row._4
        if currentRowShipTypeSpecific not in listOfAllShipTyeSpecific:
            # print(currentRowShipTypeSpecific)
            # print(currentRowIndex)
            indecesOfMMSIsWithShipTypingNotInShipTypeHierarchy.append(currentRowIndex)
    # exit()
    "drop these MMSI"
    ScrapedData.drop(indecesOfMMSIsWithShipTypingNotInShipTypeHierarchy, inplace=True)
    "reset indeces"
    ScrapedData = ScrapedData.reset_index(drop=True)

    "correct mismatched ShipType and ShipTypeSpecifc as defined in shipTypeHierarchy"
    "firstly check every row and store indeces with rows that have mistmatched data"
    indecesOfShipsWithMistmatchedShipTypeShipTypeSpecific: list[int] = []
    for row in ScrapedData.itertuples():
        currentRowIndex = row.Index
        currentRowShipType = row._3
        currentRowShipTypeSpecific = row._4
        "now check based upon shipTypeHierarchy"
        checked: bool = False
        for globalShipType in shipTypeHierarchy.keys():
            if checked:
                break
            for shipType in shipTypeHierarchy[globalShipType]:
                if checked:
                    break
                for shipTypeSpecific in shipTypeHierarchy[globalShipType][shipType]:
                    if shipTypeSpecific == currentRowShipTypeSpecific:
                        if shipType != currentRowShipType:
                            indecesOfShipsWithMistmatchedShipTypeShipTypeSpecific.append(
                                currentRowIndex
                            )
                            checked = True
                            break
                        else:
                            checked = True
                            break
    "now assign ShipType"
    for row in ScrapedData.itertuples():
        currentRowIndex = row.Index
        currentRowShipTypeSpecific = row._4
        if currentRowIndex in indecesOfShipsWithMistmatchedShipTypeShipTypeSpecific:
            "find ShipType to assign"
            checked: bool = False
            for globalShipType in shipTypeHierarchy.keys():
                if checked:
                    break
                for shipType in shipTypeHierarchy[globalShipType]:
                    if checked:
                        break
                    for shipTypeSpecific in shipTypeHierarchy[globalShipType][shipType]:
                        if shipTypeSpecific == currentRowShipTypeSpecific:
                            ScrapedData.at[currentRowIndex, "Ship Type"] = shipType
                            checked = True
                            break

    "Augment ships with 0 lenght/breadth but valid ship type"
    "fill the buffer of unique shipTypes with known dimensions"
    shipTypes = list(ScrapedData["Ship Type"].unique())
    for shipType in shipTypes:
        "temporary buffer for a list of tuples"
        tempListOfTuplesLenghtBreadth = []
        "temporary dataframe containing only current shiptype"
        tempDataFrameOfCurrentShipType = ScrapedData[
            ScrapedData["Ship Type"] == shipType
        ]
        "append temporary list with tuples of lenght and breadth of current shiptype"
        "using vaild non zero lenght breadth"
        for row in tempDataFrameOfCurrentShipType.itertuples():
            "skip invalid ship dimensions"
            if row.Lenght == 0.0 or row.Breadth == 0.0:
                continue
            "append the list with tuples of lenght and breadth"
            tempListOfTuplesLenghtBreadth.append((row.Lenght, row.Breadth))
        "append rows of ScrapedData with zero lenght breadth of current shiptype with "
        "random value from a tempListOfTuplesLenghtBreadth"
        for row in ScrapedData.itertuples():
            "now find ships with 0 dimension"
            if row._3 == shipType and (row.Lenght == 0.0 or row.Breadth == 0.0):
                "take a random tuple from list"
                "in case of ship being the only one with 0 lenght and valid shipType"
                "of that ship type drop it,this equates to empty randomTupleLenghtBreadth"
                try:
                    randomTupleLenghtBreadth = random.choice(
                        tempListOfTuplesLenghtBreadth
                    )
                    "set values"
                    ScrapedData.at[row.Index, "Lenght"] = randomTupleLenghtBreadth[0]
                    ScrapedData.at[row.Index, "Breadth"] = randomTupleLenghtBreadth[1]
                except:
                    "drop the invalid ship"
                    ScrapedData.drop(row.Index, inplace=True)
                    ScrapedData.reset_index(drop=True)

    "Finally add the GeneralShipType column"
    "first get the list corresponding to a ShipType column in ScrapedData"
    shipTypeColumn = list(ScrapedData["Ship Type"])
    "column buffer for globalShipType"
    globalShipTypeColumn: list[str] = []
    "fill the column buffer by shipTypeHierarchy"
    for shipTypeInRow in shipTypeColumn:
        filled: bool = False
        for globalShipType in shipTypeHierarchy.keys():
            if filled:
                break
            for shipType in shipTypeHierarchy[globalShipType]:
                if shipTypeInRow == shipType:
                    globalShipTypeColumn.append(globalShipType)
                    filled = True
                    break
    "insert column in DataFrame"
    ScrapedData.insert(2, "Global Ship Type", globalShipTypeColumn, True)

    "finally save the new updated ScrapedData"
    ScrapedData.to_csv("ScrapedData.csv", index=False)
    "console out"
    print("Completed full Augmentation")
