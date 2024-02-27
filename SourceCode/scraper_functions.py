from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from typing import Type
from bs4 import BeautifulSoup


def mmsi_list_to_scrape():
    """returns list of MMSI to scrape, tries to use relative path but if not existant
    user should input inside this function path to MMSI_all_AIS_data_individually"""

    "get the path to the MMSI_all_AIS_data_individually,"
    "if not in default dir, put the apropriate location"
    path_to_cimer_dir = Path(__file__).parents[2]
    dir_MMSI_all_AIS_data_individually =\
        'Ship_Route_Database_dir/Individual_MMSI_DataFrames/MMSI_all_AIS_data_individually/'
    dir_MMSI_all_AIS_data_individually = os.path.join(
        path_to_cimer_dir, dir_MMSI_all_AIS_data_individually)
    # user input here if not existant
    # dir_MMSI_all_AIS_data_individually=path_to_directory_if_not_in_default

    "use dir_MMSI_all_AIS_data_individually to create a list of current MMSI values"
    for roots, directories, files in os.walk(dir_MMSI_all_AIS_data_individually):
        temp_list_of_MMSI_values = list(files)
    temp_list_of_MMSI_values.sort()

    # list to store the int MMSI values
    list_of_MMSI_values: list[int] = []

    # remove .csv extension and cast to int
    for file in temp_list_of_MMSI_values:
        list_of_MMSI_values.append(int(file.split('.')[0]))

    return list_of_MMSI_values


# MARINE TRAFFIC PAGE SCRAPE
"html page items for: https://www.marinetraffic.com/"
marineTraf: dict[str:(str, str)] = \
    {
        "AGREE": ("id", '//button[@class=" css-47sehv"]'),
        "Filter button": ("id",
                          '//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div\
                            /div/div/div[2]/div/section[1]/div/div/div[3]\
                            /div/div[1]/div/div[3]/button'),
        "Filter button search bar": ("id", ".MuiInputBase-input.MuiInput-input.css-1xre3gi"),
        "Filter button suggestion": ("id", ".MuiButtonBase-root.MuiListItemButton-root.MuiListItemButton-gutters.MuiListItemButton-root.MuiListItemButton-gutters.css-1yqz5vb"),
        "Filter button global area input box": ("id",".MuiInputBase-input.MuiInput-input.css-1xre3gi"),
        "Filter button checkbox first": ("id",".MuiTypography-root.MuiTypography-body1.MuiListItemText-primary.css-mawvfo"),
        "Filter button checkbox west mediterranean sea": ("id","react-autowhatever-1--item-0"),
        "Filter button checkbox east mediterranean sea": ("id","react-autowhatever-1--item-1"),
        "Press ADD FILTER": ("id", '/html/body/main/div/div/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div/section[1]/div/div/div[3]/div/div[1]/div/div[3]/div/div/div/div/div[3]/div[2]/div[2]/button'),
        "Number Of Ships":('div', {'class': 'ag-cell-content'}),
        "Select Ship": ("div" ,".ag-cell-content-link"),
        "Click on first ship in list": \
            ("xpath",'//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[1]/div/div/div[3]/div/div/a'),
        "Ship Name": ("id", "shipName"),
        "Ship Type": ("id", "shipType"),
        "Ship Type Specific": ("id", "shipTypeSpecific"),
        "Lenght and Breadth": ("id", "lengthOverallBreadthExtreme"),
        "Speed Max and Average Speed": ("id", "voyageInfo-section-recordedSpeed"),
        "Missing Ship": ("id",'//*[@id="borderLayout_eGridPanel"]/div[2]/div/div/span/text()')
} 
#Number of ships ag-cell-content is so far 14 for one ship
numberOfDivsIndicatingOneShip=14

def PresenceOfElement\
    (seleniumDriverObj,seleniumByObjType:Type[By],searchType:str,marineTrafKey:str):
    """takes a type to use in selenium such as xpath, id etc. and
    then its corresponding full path, refrence etc. all is contained
    in marineTraf dict, this function explictly uses marineTraf dict inside
    of it body andcannot not run if the dict not in same .py file. returns 
    a WebDriverWait objectfile"""
    return WebDriverWait(seleniumDriverObj, 5).until(EC.presence_of_element_located(
            (seleniumByObjType, marineTraf[marineTrafKey][1])))


def VisibilityOfElement\
    (seleniumDriverObj,seleniumByObjType:Type[By],searchType:str,marineTrafKey:str):
    """takes a type to use in selenium such as xpath, id etc. and
    then its corresponding full path, refrence etc. all is contained
    in marineTraf dict, this function explictly uses marineTraf dict inside
    of it body andcannot not run if the dict not in same .py file. returns 
    a WebDriverWait objectfile"""
    return WebDriverWait(seleniumDriverObj, 5).until(EC.visibility_of_element_located(
            (seleniumByObjType, marineTraf[marineTrafKey][1])))
    

def ClickableElement\
    (seleniumDriverObj,seleniumByObjType:Type[By],searchType:str,marineTrafKey:str):
    """takes a type to use in selenium such as xpath, id etc. and
    then its corresponding full path, refrence etc. all is contained
    in marineTraf dict, this function explictly uses marineTraf dict inside
    of it body andcannot not run if the dict not in same .py file. returns 
    a WebDriverWait objectfile"""
    return WebDriverWait(seleniumDriverObj, 5).until(EC.element_to_be_clickable(
            (seleniumByObjType, marineTraf[marineTrafKey][1])))
    

def SelectableElement\
    (seleniumDriverObj,seleniumByObjType:Type[By],searchType:str,marineTrafKey:str):
    """takes a type to use in selenium such as xpath, id etc. and
    then its corresponding full path, refrence etc. all is contained
    in marineTraf dict, this function explictly uses marineTraf dict inside
    of it body andcannot not run if the dict not in same .py file. returns 
    a WebDriverWait object"""
    return WebDriverWait(seleniumDriverObj, 5).until(EC.element_to_be_selected(
            (seleniumByObjType, marineTraf[marineTrafKey][1])))


def CheckIfShipInMarineTrafficAndIfSoIfOnlyOneExists(mmsi: int):
    """takes an mmsi int value as input and scrapes the first page of vessels
    search in maritimetraffic.com:
    returns: None  if no ship in database, 
    else if exists and is the only one in database 
    returns: "Only One ship in the database" and if so should be used
    in tandem with ScrapeMarineTrafficWorld function
    else:
    returns: "More than one ship in the database" """
    
    "initialize the selenium web driver"
    "webchrome driver location"
    "chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'"
    driver = webdriver.Chrome()
    "maximize window to ensure the same button location"
    driver.maximize_window()
    "open the search page "
    driver.get(
        f"https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,mmsi,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes&mmsi|eq|mmsi={mmsi}")
    
    "click on AGREE button, if not found refresh "
    buttonNotFound=True
    while(buttonNotFound):
        try:
            time.sleep(1.5)
            agreeButton = ClickableElement(driver,By.XPATH,"id","AGREE")
            agreeButton.click()
            buttonNotFound=False
        except:
            driver.refresh()
            continue
    
    time.sleep(2.)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    'find the divs'
    divs = soup.find_all(marineTraf['Number Of Ships'][0], marineTraf['Number Of Ships'][1])
    'get the number of divs'
    numberOfDivs=len(divs)
    'if larger than current marinetraffic.com settings'
    if(numberOfDivs>numberOfDivsIndicatingOneShip):
        driver.close()
        driver.quit()
        time.sleep(1.5)
        return "More than one ship in the database"
    elif(numberOfDivs==numberOfDivsIndicatingOneShip):
        driver.close()
        driver.quit()
        time.sleep(1.5)
        return "Only One ship in the database"
    else:
        driver.close()
        driver.quit()
        time.sleep(1.5)
        return None



def ScrapeMarineTrafficAdriaticSea(mmsi: int):
    """takes an mmsi int value as input and scrapes for necessary infromation using the
    area around adriatic sea, if multiple ships with same mmsi are found in this area
    the first one is chosen as a referent for scrape,
    if ship found returns a list formated by: [shipName, ShipType, Lenght, Breadth] 
    else returns None"""

    "time to wait in second"
    sleep_time=2.

    "initialize the selenium web driver"
    "webchrome driver location"
    "chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'"
    driver = webdriver.Chrome()
    "maximize window to ensure the same button location"
    driver.maximize_window()
    "open the search page "
    driver.get(
        f"https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,mmsi,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes&mmsi|eq|mmsi={mmsi}")
    
    "click on AGREE button, if not found refresh "
    buttonNotFound=True
    while(buttonNotFound):
        try:
            time.sleep(1.5)
            agreeButton = ClickableElement(driver,By.XPATH,"id","AGREE")
            agreeButton.click()
            buttonNotFound=False
        except:
            driver.refresh()
            continue   

    time.sleep(1.5)
   
    "Fill out the filter button with Adriatc Sea as global area"                                                         
    "check for presence and click on the Filter button"
    filterButtonNotFound=True
    while(filterButtonNotFound):
        try:
            time.sleep(0.65)
            filterButton = ClickableElement(driver,By.XPATH, "id","Filter button")
            filterButton.click()
            "update presence"
            filterButtonNotFound=False
        except:
            driver.refresh()
            continue
    
    "find search bar and fill it with Global Area"
    searchBarNotFound=True
    while(searchBarNotFound):
        try:
            time.sleep(0.65)
            inputToFilter = driver.find_element(By.CSS_SELECTOR,marineTraf['Filter button search bar'][1])
            "send the input"
            time.sleep(0.25)
            inputToFilter.send_keys("Global Area")
            time.sleep(0.25)
            "click on suggestion"
            inputToFilter = driver.find_elements(By.CSS_SELECTOR,marineTraf["Filter button suggestion"][1])
            inputToFilter[0].click()
            "update presence"
            searchBarNotFound=False
        except:
            continue
 
    "check for presence of Gloabl Area input search bar and fill it with Adriatic Sea"
    "and check the checkbox for Adriatic Sea"
    searchBarNotFound=True
    while(searchBarNotFound):
        try:
            time.sleep(0.65)            
            inputToFilter =\
                  driver.find_element(By.CSS_SELECTOR,marineTraf["Filter button global area input box"][1])
            "send the input"
            time.sleep(0.65) 
            inputToFilter.send_keys("Adriatic Sea")
            "click on suggestion"
            time.sleep(0.25)
            inputToFilter =  driver.find_elements(By.CSS_SELECTOR,marineTraf["Filter button checkbox first"][1])
            inputToFilter[0].click()  
            "update presence"
            searchBarNotFound=False
        except:
            continue
    
    "check for presence of the AddTheFilterButton"
    filterButtonNotFound=True
    while(filterButtonNotFound):
        try:
            time.sleep(0.5)
            addFilterButton = \
                ClickableElement(driver,By.XPATH,None,"Press ADD FILTER")
            addFilterButton.click()
            "update presence"
            filterButtonNotFound=False
        except:
            continue

    "sleep"
    "click on the first ship in the list if found, else return none "
    time.sleep(1.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    'find the divs'
    divs = soup.find_all(marineTraf['Number Of Ships'][0], marineTraf['Number Of Ships'][1])
    'get the number of divs'
    numberOfDivs=len(divs)
    'check the number of elements'
    if(numberOfDivs>=numberOfDivsIndicatingOneShip):
        'load ship'
        time.sleep(0.5)
        izaberiShip=driver.find_element(By.CSS_SELECTOR,marineTraf['Select Ship'][1])
        izaberiShip.click()
    else:
        return None
    
    "sleep to wait for full load of ship page"
    "scroll to load javascript"
    time.sleep(sleep_time)
    scroll_positon=50
    for _ in range(50):
        driver.execute_script(f"window.scrollTo(0, {scroll_positon})")
        "smooth scroll"
        time.sleep(0.05)
        scroll_positon+=50
    time.sleep(.5)

    "Finally scrape the data, return None for every missing data"
    "SHIP NAME"
    try:
        shipName=driver.find_element("id",marineTraf["Ship Name"][1]).text
        shipName=shipName.split(":")[1]
    except:
        shipName=None
    "SHIP TYPE"
    try:
        shipType=driver.find_element("id",marineTraf["Ship Type"][1]).text
        shipType=shipType.split(":")[1]
    except:
        shipType=None
    "SHIP TYPE SPECIFIC"
    try:
        shipTypeSpecific=driver.find_element("id",marineTraf["Ship Type Specific"][1]).text
        shipTypeSpecific=shipTypeSpecific.split(":")[1]
    except:
        shipTypeSpecific=None
    "LENGHT AND BREADTH"
    try:
        lenghtBreadth=driver.find_element("id",marineTraf["Lenght and Breadth"][1]).text
        try:
            "second check if not filled in correctly data on web page"
            "re used to etract float numbers, thx to John Machin"
            numeric_const_pattern = \
                '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
            rx = re.compile(numeric_const_pattern, re.VERBOSE)
            lenght, breadth=rx.findall(lenghtBreadth)
        except:
            lenght=None
            breadth=None
    except:
        lenght=None
        breadth=None
    "SPEED MAX AND AVERAGE SPEED"
    try:
        speed=driver.find_element("id",marineTraf["Speed Max and Average Speed"][1]).text
        try:
            "second check if not filled in correctly data on web page"
            "re used to etract float numbers, thx to John Machin"
            numeric_const_pattern = \
                '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
            rx = re.compile(numeric_const_pattern, re.VERBOSE)
            speeds=rx.findall(speed)
            if(len(speeds)==2):
                maxSpeed, averageSpeed=speeds
            elif(len(speeds)==1):
                averageSpeed=speeds[0]
                maxSpeed=0
            else:
                maxSpeed=None
                averageSpeed=None
        except:
            maxSpeed=None
            averageSpeed=None
    except:
        maxSpeed=None
        averageSpeed=None

    "cleanup"
    driver.close()
    driver.quit()
    time.sleep(1.5)
    
    "return a dictionary"
    return \
        {"MMSI":mmsi,"Ship Name":shipName,"Ship Type": shipType,\
            "Ship Type Specific":shipTypeSpecific,"Lenght":lenght,"Breadth": breadth,
            "Max Speed":maxSpeed,"Average Speed":averageSpeed}


def ScrapeMarineTrafficWestMediterraneanSea(mmsi: int):
    """takes an mmsi int value as input and scrapes for necessary infromation using the
    a wider area composing of whole WestMediterraneanSea, if multiple ships with same mmsi 
    are found in this area the first one is chosen as a referent for scrape,
    if ship found returns a list formated by: [shipName, ShipType, Lenght, Breadth] 
    else returns None"""

    "time to wait in second"
    sleep_time=2.

    "initialize the selenium web driver"
    "webchrome driver location"
    "chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'"
    driver = webdriver.Chrome()
    "maximize window to ensure the same button location"
    driver.maximize_window()
    "open the search page "
    driver.get(
        f"https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,mmsi,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes&mmsi|eq|mmsi={mmsi}")
    
    "click on AGREE button, if not found refresh "
    buttonNotFound=True
    while(buttonNotFound):
        try:
            time.sleep(1.5)
            agreeButton = ClickableElement(driver,By.XPATH,"id","AGREE")
            agreeButton.click()
            buttonNotFound=False
        except:
            driver.refresh()
            continue    

    time.sleep(1.5)

    "Fill out the filter button with Mediterranean as global area"                                                         
    "check for presence and click on the Filter button"
    filterButtonNotFound=True
    while(filterButtonNotFound):
        try:
            time.sleep(0.65)
            filterButton = ClickableElement(driver,By.XPATH, "id","Filter button")
            filterButton.click()
            "update presence"
            filterButtonNotFound=False
        except:
            driver.refresh()
            continue
    
    "check for presence of search bar and fill it with Global Area"
    searchBarNotFound=True
    while(searchBarNotFound):
        try:
            time.sleep(0.65)
            inputToFilter = driver.find_element(By.CSS_SELECTOR,marineTraf['Filter button search bar'][1])
            "send the input"
            time.sleep(0.25)
            inputToFilter.send_keys("Global Area")
            time.sleep(0.25)
            "click on suggestion"
            inputToFilter = driver.find_elements(By.CSS_SELECTOR,marineTraf["Filter button suggestion"][1])
            inputToFilter[0].click()
            "update presence"
            searchBarNotFound=False
        except:
            continue
 
    "check for presence of Gloabl Area input search bar and fill it with Mediterranean"
    "and check the checkbox for West Mediterranean "
    searchBarNotFound=True
    while(searchBarNotFound):
        try:
            time.sleep(0.65)            
            inputToFilter =\
                  driver.find_element(By.CSS_SELECTOR,marineTraf["Filter button global area input box"][1])
            "send the input"
            time.sleep(0.65)
            inputToFilter.send_keys("Mediterranean")
            "click on suggestions"
            time.sleep(0.25)
            inputToFilter = driver.find_elements(By.CSS_SELECTOR,marineTraf["Filter button checkbox first"][1] )
            'press on firstd element'
            inputToFilter[0].click()
            "update presence"
            searchBarNotFound=False
        except:
            continue
    
    "check for presence of the AddTheFilterButton"
    filterButtonNotFound=True
    while(filterButtonNotFound):
        try:
            time.sleep(0.5)
            addFilterButton = \
                ClickableElement(driver,By.XPATH,None,"Press ADD FILTER")
            addFilterButton.click()
            "update presence"
            filterButtonNotFound=False
        except:
            continue

    "sleep"
    time.sleep(1.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    'find the divs'
    divs = soup.find_all(marineTraf['Number Of Ships'][0], marineTraf['Number Of Ships'][1])
    'get the number of divs'
    numberOfDivs=len(divs)
    'check the number of elements'
    if(numberOfDivs>=numberOfDivsIndicatingOneShip):
        'load ship'
        time.sleep(0.5)
        izaberiShip=driver.find_element(By.CSS_SELECTOR,marineTraf['Select Ship'][1])
        izaberiShip.click()
    else:
        return None

    "sleep to wait for full load of ship page"
    "scroll to load javascript"
    time.sleep(sleep_time)
    scroll_positon=50
    for _ in range(50):
        driver.execute_script(f"window.scrollTo(0, {scroll_positon})")
        "smooth scroll"
        time.sleep(0.05)
        scroll_positon+=50
    time.sleep(.5)

    "Finally scrape the data, return None for every missing data"
    "SHIP NAME"
    try:
        shipName=driver.find_element("id",marineTraf["Ship Name"][1]).text
        shipName=shipName.split(":")[1]
    except:
        shipName=None
    "SHIP TYPE"
    try:
        shipType=driver.find_element("id",marineTraf["Ship Type"][1]).text
        shipType=shipType.split(":")[1]
    except:
        shipType=None
    "SHIP TYPE SPECIFIC"
    try:
        shipTypeSpecific=driver.find_element("id",marineTraf["Ship Type Specific"][1]).text
        shipTypeSpecific=shipTypeSpecific.split(":")[1]
    except:
        shipTypeSpecific=None
    "LENGHT AND BREADTH"
    try:
        lenghtBreadth=driver.find_element("id",marineTraf["Lenght and Breadth"][1]).text
        try:
            "second check if not filled in correctly data on web page"
            "re used to etract float numbers, thx to John Machin"
            numeric_const_pattern = \
                '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
            rx = re.compile(numeric_const_pattern, re.VERBOSE)
            lenght, breadth=rx.findall(lenghtBreadth)
        except:
            lenght=None
            breadth=None
    except:
        lenght=None
        breadth=None
    "SPEED MAX AND AVERAGE SPEED"
    try:
        speed=driver.find_element("id",marineTraf["Speed Max and Average Speed"][1]).text
        try:
            "second check if not filled in correctly data on web page"
            "re used to etract float numbers, thx to John Machin"
            numeric_const_pattern = \
                '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
            rx = re.compile(numeric_const_pattern, re.VERBOSE)
            speeds=rx.findall(speed)
            if(len(speeds)==2):
                maxSpeed, averageSpeed=speeds
            elif(len(speeds)==1):
                averageSpeed=speeds[0]
                maxSpeed=0
            else:
                maxSpeed=None
                averageSpeed=None
        except:
            maxSpeed=None
            averageSpeed=None
    except:
        maxSpeed=None
        averageSpeed=None

    "cleanup"
    driver.close()
    driver.quit()
    time.sleep(1.5)
    
    "return a dictionary"
    return \
        {"MMSI":mmsi,"Ship Name":shipName,"Ship Type": shipType,\
            "Ship Type Specific":shipTypeSpecific,"Lenght":lenght,"Breadth": breadth,
            "Max Speed":maxSpeed,"Average Speed":averageSpeed}


def ScrapeMarineTrafficEastMediterraneanSea(mmsi: int):
    """takes an mmsi int value as input and scrapes for necessary infromation using the
    a wider area composing of whole EastMediterraneanSea, if multiple ships with same mmsi 
    are found in this area the first one is chosen as a referent for scrape,
    if ship found returns a list formated by: [shipName, ShipType, Lenght, Breadth] 
    else returns None"""

    "time to wait in second"
    sleep_time=2.

    "initialize the selenium web driver"
    "webchrome driver location"
    "chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'"
    driver = webdriver.Chrome()
    "maximize window to ensure the same button location"
    driver.maximize_window()
    "open the search page "
    driver.get(
        f"https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,mmsi,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes&mmsi|eq|mmsi={mmsi}")
    
    "click on AGREE button, if not found refresh "
    buttonNotFound=True
    while(buttonNotFound):
        try:
            time.sleep(1.5)
            agreeButton = ClickableElement(driver,By.XPATH,"id","AGREE")
            agreeButton.click()
            buttonNotFound=False
        except:
            driver.refresh()
            continue

    time.sleep(1.5)

    "Fill out the filter button with Mediterranean as global area"                                                         
    "check for presence and click on the Filter button"
    filterButtonNotFound=True
    while(filterButtonNotFound):
        try:
            time.sleep(0.65)
            filterButton = ClickableElement(driver,By.XPATH, "id","Filter button")
            filterButton.click()
            "update presence"
            filterButtonNotFound=False
        except:
            driver.refresh()
            continue
    
    "check for presence of search bar and fill it with Global Area"
    searchBarNotFound=True
    while(searchBarNotFound):
        try:
            time.sleep(0.65)
            inputToFilter = driver.find_element(By.CSS_SELECTOR,marineTraf['Filter button search bar'][1])
            "send the input"
            time.sleep(0.25)
            inputToFilter.send_keys("Global Area")
            time.sleep(0.25)
            "click on suggestion"
            inputToFilter = driver.find_elements(By.CSS_SELECTOR,marineTraf["Filter button suggestion"][1])
            inputToFilter[0].click()
            "update presence"
            searchBarNotFound=False
        except:
            continue
 
    "check for presence of Gloabl Area input search bar and fill it with Mediterranean"
    "and check the checkbox for East Mediterranean "
    searchBarNotFound=True
    while(searchBarNotFound):
        try:
            time.sleep(0.65)            
            inputToFilter =\
                  driver.find_element(By.CSS_SELECTOR,marineTraf["Filter button global area input box"][1])
            "send the input"
            time.sleep(0.65)
            inputToFilter.send_keys("Mediterranean")
            "click on suggestions"
            time.sleep(0.25)
            inputToFilter = driver.find_elements(By.CSS_SELECTOR,marineTraf["Filter button checkbox first"][1] )
            'press on second element'
            inputToFilter[1].click()
            "update presence"
            searchBarNotFound=False
        except:
            continue
    
    "check for presence of the AddTheFilterButton"
    filterButtonNotFound=True
    while(filterButtonNotFound):
        try:
            time.sleep(0.5)
            addFilterButton = \
                ClickableElement(driver,By.XPATH,None,"Press ADD FILTER")
            addFilterButton.click()
            "update presence"
            filterButtonNotFound=False
        except:
            continue

    "sleep"
    time.sleep(1.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    'find the divs'
    divs = soup.find_all(marineTraf['Number Of Ships'][0], marineTraf['Number Of Ships'][1])
    'get the number of divs'
    numberOfDivs=len(divs)
    'check the number of elements'
    if(numberOfDivs>=numberOfDivsIndicatingOneShip):
        'load ship'
        time.sleep(0.5)
        izaberiShip=driver.find_element(By.CSS_SELECTOR,marineTraf['Select Ship'][1])
        izaberiShip.click()
    else:
        return None

    "sleep to wait for full load of ship page"
    "scroll to load javascript"
    time.sleep(sleep_time)
    scroll_positon=50
    for _ in range(50):
        driver.execute_script(f"window.scrollTo(0, {scroll_positon})")
        "smooth scroll"
        time.sleep(0.05)
        scroll_positon+=50
    time.sleep(.5)

    "Finally scrape the data, return None for every missing data"
    "SHIP NAME"
    try:
        shipName=driver.find_element("id",marineTraf["Ship Name"][1]).text
        shipName=shipName.split(":")[1]
    except:
        shipName=None
    "SHIP TYPE"
    try:
        shipType=driver.find_element("id",marineTraf["Ship Type"][1]).text
        shipType=shipType.split(":")[1]
    except:
        shipType=None
    "SHIP TYPE SPECIFIC"
    try:
        shipTypeSpecific=driver.find_element("id",marineTraf["Ship Type Specific"][1]).text
        shipTypeSpecific=shipTypeSpecific.split(":")[1]
    except:
        shipTypeSpecific=None
    "LENGHT AND BREADTH"
    try:
        lenghtBreadth=driver.find_element("id",marineTraf["Lenght and Breadth"][1]).text
        try:
            "second check if not filled in correctly data on web page"
            "re used to etract float numbers, thx to John Machin"
            numeric_const_pattern = \
                '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
            rx = re.compile(numeric_const_pattern, re.VERBOSE)
            lenght, breadth=rx.findall(lenghtBreadth)
        except:
            lenght=None
            breadth=None
    except:
        lenght=None
        breadth=None
    "SPEED MAX AND AVERAGE SPEED"
    try:
        speed=driver.find_element("id",marineTraf["Speed Max and Average Speed"][1]).text
        try:
            "second check if not filled in correctly data on web page"
            "re used to etract float numbers, thx to John Machin"
            numeric_const_pattern = \
                '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
            rx = re.compile(numeric_const_pattern, re.VERBOSE)
            speeds=rx.findall(speed)
            if(len(speeds)==2):
                maxSpeed, averageSpeed=speeds
            elif(len(speeds)==1):
                averageSpeed=speeds[0]
                maxSpeed=0
            else:
                maxSpeed=None
                averageSpeed=None
        except:
            maxSpeed=None
            averageSpeed=None
    except:
        maxSpeed=None
        averageSpeed=None

    "cleanup"
    driver.close()
    driver.quit()
    time.sleep(1.5)
    
    "return a dictionary"
    return \
        {"MMSI":mmsi,"Ship Name":shipName,"Ship Type": shipType,\
            "Ship Type Specific":shipTypeSpecific,"Lenght":lenght,"Breadth": breadth,
            "Max Speed":maxSpeed,"Average Speed":averageSpeed}

def ScrapeMarineTrafficWorld(mmsi: int):
    """takes an mmsi int value as input and scrapes for necessary infromation using the
    a whole datatbse, if multiple ships with same mmsi are found in this area the 
    first one is chosen as a referent for scrape,
    if ship found returns a list formated by: [shipName, ShipType, Lenght, Breadth] 
    else returns None"""

    "time to wait in second"
    sleep_time=2.

    "initialize the selenium web driver"
    "webchrome driver location"
    "chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'"
    driver = webdriver.Chrome()
    "maximize window to ensure the same button location"
    driver.maximize_window()
    "open the search page "
    driver.get(
        f"https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,mmsi,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes&mmsi|eq|mmsi={mmsi}")
    
    "click on AGREE button, if not found refresh "
    buttonNotFound=True
    while(buttonNotFound):
        try:
            time.sleep(1.5)
            agreeButton = ClickableElement(driver,By.XPATH,"id","AGREE")
            agreeButton.click()
            buttonNotFound=False
        except:
            driver.refresh()
            continue

    "sleep"
    time.sleep(1.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.find_all(marineTraf['Number Of Ships'][0], marineTraf['Number Of Ships'][1])
    numberOfDivs=len(divs)
    'check the number of elements'
    if(numberOfDivs>=numberOfDivsIndicatingOneShip):
        'load ship'
        time.sleep(0.5)
        izaberiShip=driver.find_element(By.CSS_SELECTOR,marineTraf['Select Ship'][1])
        izaberiShip.click()
    else:
        return None

    "sleep to wait for full load of ship page"
    "scroll to load javascript"
    time.sleep(sleep_time)
    scroll_positon=50
    for _ in range(50):
        driver.execute_script(f"window.scrollTo(0, {scroll_positon})")
        "smooth scroll"
        time.sleep(0.05)
        scroll_positon+=50
    time.sleep(.5)

    "Finally scrape the data, return None for every missing data"
    "SHIP NAME"
    try:
        shipName=driver.find_element("id",marineTraf["Ship Name"][1]).text
        shipName=shipName.split(":")[1]
    except:
        shipName=None
    "SHIP TYPE"
    try:
        shipType=driver.find_element("id",marineTraf["Ship Type"][1]).text
        shipType=shipType.split(":")[1]
    except:
        shipType=None
    "SHIP TYPE SPECIFIC"
    try:       
        shipTypeSpecific=driver.find_element("id",marineTraf["Ship Type Specific"][1]).text
        shipTypeSpecific=shipTypeSpecific.split(":")[1]
    except:
        shipTypeSpecific=None
    "LENGHT AND BREADTH"
    try:
        lenghtBreadth=driver.find_element("id",marineTraf["Lenght and Breadth"][1]).text
        try:
            "second check if not filled in correctly data on web page"
            "re used to etract float numbers, thx to John Machin"
            numeric_const_pattern = \
                '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
            rx = re.compile(numeric_const_pattern, re.VERBOSE)
            lenght, breadth=rx.findall(lenghtBreadth)
        except:
            lenght=None
            breadth=None
    except:
        lenght=None
        breadth=None
    "SPEED MAX AND AVERAGE SPEED"
    try:
        speed=driver.find_element("id",marineTraf["Speed Max and Average Speed"][1]).text
        try:
            "second check if not filled in correctly data on web page"
            "re used to etract float numbers, thx to John Machin"
            numeric_const_pattern = \
                '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
            rx = re.compile(numeric_const_pattern, re.VERBOSE)
            speeds=rx.findall(speed)
            if(len(speeds)==2):
                maxSpeed, averageSpeed=speeds
            elif(len(speeds)==1):
                averageSpeed=speeds[0]
                maxSpeed=0
            else:
                maxSpeed=None
                averageSpeed=None
        except:
            maxSpeed=None
            averageSpeed=None
    except:
        maxSpeed=None
        averageSpeed=None

    "cleanup"
    driver.close()
    driver.quit()
    time.sleep(1.5)
    
    "return a dictionary"
    return \
        {"MMSI":mmsi,"Ship Name":shipName,"Ship Type": shipType,\
            "Ship Type Specific":shipTypeSpecific,"Lenght":lenght,"Breadth": breadth,
            "Max Speed":maxSpeed,"Average Speed":averageSpeed}

scrapeKeywards:list[str,str,str,str]=\
            [
            "MMSI",
            "Ship Name",
            "Ship Type",
            "Ship Type Specific",
            "Lenght",
            "Breadth",
            "Max Speed",
            "Average Speed"  
            ]