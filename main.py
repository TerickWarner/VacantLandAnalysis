from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import pandas as pd
import time
from bs4 import BeautifulSoup

#list of websites for for sale vacant lots
# https://www.land.com/Crawford-County-GA/all-land/2-50-acres/is-active/
# https://www.zillow.com/crawford-county-ga/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Crawford%20County%2C%20GA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-84.35536400316056%2C%22east%22%3A-83.55198875901993%2C%22south%22%3A32.452387492077776%2C%22north%22%3A32.9297118218284%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A2227%2C%22regionType%22%3A4%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22lot%22%3A%7B%22min%22%3A87120%2C%22max%22%3A2178000%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D
# https://www.landwatch.com/georgia-land-for-sale/crawford-county/acres-2-50/available
# https://www.realtor.com/realestateandhomes-search/Crawford-County_GA/type-land/lot-sqft-87120
# https://www.trulia.com/for_sale/13079_c/LOT%7CLAND_type/

#list of websites for for sold vacant lots
#https://www.land.com/Crawford-County-GA/all-land/2-50-acres/is-sold/



#LANDDOTCOME WEBSCRAPE IS DONE
def get_land_dotcom_for_sale_data():
    #use the geckodriver to get to the specific url to find land.com for sale data
    options = Options()
    service = Service("C:/Users/teric/Desktop/geckodriver.exe") #path to local geckodriver file which allows selenium to run
    options.headless = False #runs it headless
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://www.land.com/Crawford-County-GA/all-land/2-50-acres/is-active/")

    #find the elements that contain relevant information
    land_dotcom_body = driver.find_elements(By.XPATH, "//div[contains(@data-qa-placardinfo, 'true')]")
    final_list = [] #make a list to be able to append the children element's data- makes a list of lists
    
    #nested for loop loops through the the elements in land_dotcom_body which is a list and identifies relevent information
    for i in land_dotcom_body:
        children = i.find_elements(By.TAG_NAME, "div")
        children_list = []
        for i in children[1:4]: #needed data in in the divs 1-4          
            children_list.append(i.text) 
        final_list.append(children_list)

    #create the dataframe that will be used for our csv
    land_dotcom_df = pd.DataFrame(final_list, columns= ['Acres and Price', 'Address', 'Description'])

    land_dotcom_df["Address"] = land_dotcom_df["Address"].str.replace("\n", "")
    print(land_dotcom_df)
    #find the location of the created column that needs split
    acres_price_column_loc = land_dotcom_df.columns.get_loc('Acres and Price')
    split_land_dotcom_df = land_dotcom_df['Acres and Price'].str.split("•", expand=True)
    #after the split need to add those columns back to the dataframe
    final_land_dotcom_df = pd.concat([land_dotcom_df.iloc[:, :acres_price_column_loc], split_land_dotcom_df, land_dotcom_df.iloc[:, acres_price_column_loc+1:]], axis=1)
    #rename the new columns
    final_land_dotcom_df.rename(columns={0:'Acres', 1: 'Price'}, inplace=True)
    print(final_land_dotcom_df)
    final_land_dotcom_df['sale_sold'] = 'For Sale'
    final_land_dotcom_df['source'] = "Land.com"
    print(final_land_dotcom_df)

    # final_land_dotcom_df.to_csv("C:/Users/teric/Desktop/vacantLandData/LandDotComForSaleDataFINAL.csv")
    
    driver.close()
    return final_land_dotcom_df

def get_land_dotcom_for_sold_data():
    #use the geckodriver to get to the specific url to find land.com for sale data
    options = Options()
    service = Service("C:/Users/teric/Desktop/geckodriver.exe") #path to local geckodriver file which allows selenium to run
    options.headless = False #runs it headless
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://www.land.com/Crawford-County-GA/all-land/no-house/2-50-acres/is-sold/")

    #find the elements that contain relevant information
    land_dotcom_body = driver.find_elements(By.XPATH, "//div[contains(@data-qa-placardinfo, 'true')]")
    final_list = [] #make a list to be able to append the children element's data- makes a list of lists
    
    #nested for loop loops through the the elements in land_dotcom_body which is a list and identifies relevent information
    for i in land_dotcom_body:
        children = i.find_elements(By.TAG_NAME, "div")
        children_list = []
        for i in children[1:4]: #needed data in in the divs 1-4          
            children_list.append(i.text) 
        final_list.append(children_list)
        
    #create the dataframe that will be used for our csv
    land_dotcom_df = pd.DataFrame(final_list, columns= ['Acres and Price', 'Address', 'Description'])

    land_dotcom_df["Address"] = land_dotcom_df["Address"].str.replace("\n", "")
    print(land_dotcom_df)
    #find the location of the created column that needs split
    acres_price_column_loc = land_dotcom_df.columns.get_loc('Acres and Price')
    split_land_dotcom_df = land_dotcom_df['Acres and Price'].str.split("•", expand=True)
    #after the split need to add those columns back to the dataframe
    final_land_dotcom_df = pd.concat([land_dotcom_df.iloc[:, :acres_price_column_loc], split_land_dotcom_df, land_dotcom_df.iloc[:, acres_price_column_loc+1:]], axis=1)
    #rename the new columns
    final_land_dotcom_df.rename(columns={0:'Acres', 1: 'Price'}, inplace=True)
    print(final_land_dotcom_df)
    final_land_dotcom_df['sale_sold'] = 'sold'
    final_land_dotcom_df['source'] = "Land.com"
    print(final_land_dotcom_df)

    # final_land_dotcom_df.to_csv("C:/Users/teric/Desktop/vacantLandData/LandDotComForSoldDataFINAL.csv")
    
    driver.close()
    return final_land_dotcom_df

land_sale = get_land_dotcom_for_sale_data()
land_sold = get_land_dotcom_for_sold_data()

def get_zillow_for_sale_data():
    #use the geckodriver to get to the specific url to find land.com for sale data
    options = Options()
    service = Service("C:/Users/teric/Desktop/geckodriver.exe") #path to local geckodriver file which allows selenium to run
    options.headless = False #runs it headless
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://www.zillow.com/crawford-county-ga/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Crawford%20County%2C%20GA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-84.35536400316056%2C%22east%22%3A-83.55198875901993%2C%22south%22%3A32.452387492077776%2C%22north%22%3A32.9297118218284%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A2227%2C%22regionType%22%3A4%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22lot%22%3A%7B%22min%22%3A87120%2C%22max%22%3A2178000%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D")
    #let the data load into the browser with the sleep function
    time.sleep(5)
    #the data in located in a ul element within a bunch of li elements find the ul then find the li elements
    zillow_ul = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/div/div[1]/div[1]/ul")
    zillow_children = zillow_ul.find_elements(By.TAG_NAME, "li")
    print(len(zillow_children))
    empty_list = []
    #create a list of lists with the appropriate data
    for items in zillow_children:
        string_items = items.get_attribute("innerText")
        split_string_items = string_items.split('\n')
        print(type(string_items))
        empty_list.append(split_string_items)
        
    print(empty_list)

    #transforming data, eleminating unneccssary data
    substring = "Listing provided"
    substring2 = 'Loading'
    substring3 = 'Price cut'
    for i in range(len(empty_list)):
        x = empty_list[i]
        for item in x.copy():
            if substring in item:
                x.remove(item)
        for item in x.copy():
            if substring2 in item:
                x.remove(item)
        for item in x.copy():
            if substring3 in item:
                x.remove(item)

    #getting rid of empty lists within the list of lists
    delete_empty_lists = [ele for ele in empty_list if ele != []]
    delete_empty_lists2 = [ele for ele in delete_empty_lists if ele != ['']]
    print(f"THIS IS THE FINAL LIST: {delete_empty_lists2}")
    #creating the initial dataframe before transforming
    initial_zillow_df = pd.DataFrame(delete_empty_lists2, columns=['Address', 'Price', 'Acres', 'days_on_zillow'])
    print(initial_zillow_df)
    #locating the acres column to split it by a seperator
    acres_column_loc = initial_zillow_df.columns.get_loc('Acres')
    seperator = 's'
    split_initial_zillow_df = initial_zillow_df['Acres'].str.split(seperator, 1, expand=True)[0] + seperator
    print(split_initial_zillow_df)
    #creating final df
    final_zillow_dotcom_df = pd.concat([initial_zillow_df.iloc[:, :acres_column_loc], split_initial_zillow_df, initial_zillow_df.iloc[:, acres_column_loc+1:]], axis=1)
    print(final_zillow_dotcom_df)
    final_zillow_dotcom_df.rename(columns={0:'Acres'}, inplace=True)
    print(final_zillow_dotcom_df)
    #adding data that shows if it was for sale or sold and source of info
    final_zillow_dotcom_df['sale_sold'] = 'sale'
    final_zillow_dotcom_df['source'] = "zillow.com"
    print(final_zillow_dotcom_df)

    # final_zillow_dotcom_df.to_csv("C:/Users/teric/Desktop/vacantLandData/ZillowDOTcomLandForSaleFINAL.csv")
    driver.close()
    return final_zillow_dotcom_df


def get_zillow_for_sold_data():
    #use the geckodriver to get to the specific url to find land.com for sale data
    options = Options()
    service = Service("C:/Users/teric/Desktop/geckodriver.exe") #path to local geckodriver file which allows selenium to run
    options.headless = False #runs it headless
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://www.zillow.com/crawford-county-ga/sold/?searchQueryState=%7B%22usersSearchTerm%22%3A%22Crawford%20County%2C%20GA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-85.5604268693715%2C%22east%22%3A-82.346925892809%2C%22south%22%3A31.74799152969877%2C%22north%22%3A33.62488170826132%7D%2C%22mapZoom%22%3A9%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A2227%2C%22regionType%22%3A4%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22lot%22%3A%7B%22min%22%3A87120%2C%22max%22%3A2178000%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22rs%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D")
    #let the data load into the browser with the sleep function
    time.sleep(5)
    #the data in located in a ul element within a bunch of li elements find the ul then find the li elements
    zillow_ul = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/div/div[1]/div[1]/ul")
    zillow_children = zillow_ul.find_elements(By.TAG_NAME, "li")
    print(len(zillow_children))
    empty_list = []
    #create a list of lists with the appropriate data
    for items in zillow_children:
        string_items = items.get_attribute("innerText")
        split_string_items = string_items.split('\n')
        print(type(string_items))
        empty_list.append(split_string_items)
        
    print(empty_list)

    #transforming data, eleminating unneccssary data
    substring = "Listing provided"
    substring2 = 'Loading'
    substring3 = 'Price cut'
    for i in range(len(empty_list)):
        x = empty_list[i]
        for item in x.copy():
            if substring in item:
                x.remove(item)
        for item in x.copy():
            if substring2 in item:
                x.remove(item)
        for item in x.copy():
            if substring3 in item:
                x.remove(item)

    #getting rid of empty lists within the list of lists
    delete_empty_lists = [ele for ele in empty_list if ele != []]
    delete_empty_lists2 = [ele for ele in delete_empty_lists if ele != ['']]
    print(f"THIS IS THE FINAL LIST: {delete_empty_lists2}")
    #creating the initial dataframe before transforming
    initial_zillow_df = pd.DataFrame(delete_empty_lists2, columns=['Address', 'Price', 'Acres', 'days_on_zillow'])
    print(initial_zillow_df)
    #locating the acres column to split it by a seperator
    acres_column_loc = initial_zillow_df.columns.get_loc('Acres')
    seperator = 's'
    split_initial_zillow_df = initial_zillow_df['Acres'].str.split(seperator, 1, expand=True)[0] + seperator
    print(split_initial_zillow_df)
    #creating final df
    final_zillow_dotcom_df = pd.concat([initial_zillow_df.iloc[:, :acres_column_loc], split_initial_zillow_df, initial_zillow_df.iloc[:, acres_column_loc+1:]], axis=1)
    print(final_zillow_dotcom_df)
    final_zillow_dotcom_df.rename(columns={0:'Acres'}, inplace=True)
    print(final_zillow_dotcom_df)
    #adding data that shows if it was for sale or sold and source of info
    final_zillow_dotcom_df['sale_sold'] = 'sold'
    final_zillow_dotcom_df['source'] = "zillow.com"
    print(final_zillow_dotcom_df)

    # final_zillow_dotcom_df.to_csv("C:/Users/teric/Desktop/vacantLandData/ZillowDOTcomLandForSoldFINAL.csv")
    driver.close()
    return final_zillow_dotcom_df


zil_sale = get_zillow_for_sale_data()
zil_sold = get_zillow_for_sold_data()

def get_trulia_for_sale_data():
    # use the geckodriver to get to the specific url to find land.com for sale data
    options = Options()
    service = Service("C:/Users/teric/Desktop/geckodriver.exe") #path to local geckodriver file which allows selenium to run
    options.headless = False #runs it headless
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://www.trulia.com/for_sale/13079_c/LOT%7CLAND_type/2p_ls/")
    time.sleep(5)
    #first we find the ul with the list of data that we need
    trulia_ul = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/ul")
    #the length of the trulia_li will tell us how much data we have without getting into the 'Similar vacant lots near you" data
    trulia_li = trulia_ul.find_elements(By.TAG_NAME, 'li')
    time.sleep(3)
    #Get a list of the acres data
    acres_list = []
    for i in range(len(trulia_li)):
        try:
            acres = trulia_ul.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/ul/li[{i+1}]/div/div/div/div/div[1]/div[3]/span[2]/span")
            acres_list.append(acres.text)
        except:
            try:
                acres = trulia_ul.find_element(By.CSS_SELECTOR, f"div.SearchResultsList__Container-sc-14hv67h-0:nth-child(1) > ul:nth-child(2) > li:nth-child({i+1}) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > span:nth-child(1) > span:nth-child(1)")
                acres_list.append(acres.text)
            except:
                pass
    print(acres_list)
    #get a list of the price data
    time.sleep(5)
    price_list = []
    for i in range(len(trulia_li)):
        try:
            price = trulia_ul.find_element(By.CSS_SELECTOR, f"div.SearchResultsList__Container-sc-14hv67h-0:nth-child(1) > ul:nth-child(2) > li:nth-child({i+1}) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
            price_list.append(price.text)
        except:
            pass
    print(price_list)
    #get a list of the address data
    time.sleep(3)
    address_list = []
    for i in range(len(trulia_li)):
        try:
            address = trulia_ul.find_element(By.CSS_SELECTOR, f"div.SearchResultsList__Container-sc-14hv67h-0:nth-child(1) > ul:nth-child(2) > li:nth-child({i+1}) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(3) > div:nth-child(1)")
            address_list.append(address.text)
        except:
            pass
    print(address_list)
    trulia_df = pd.DataFrame()
    trulia_df['Acres'] = acres_list
    trulia_df['Price'] = price_list
    trulia_df['Address'] = address_list
    trulia_df["Address"] = trulia_df["Address"].str.replace("\n", " ")
    trulia_df['sale_sold'] = 'sale'
    trulia_df['source'] = 'trulia.com'

    # trulia_df.to_csv("C:/Users/teric/Desktop/vacantLandData/TruliaForSaleFinal.csv")
    driver.close()
    return trulia_df


def get_trulia_for_sold_data():
    # use the geckodriver to get to the specific url to find land.com for sale data
    options = Options()
    service = Service("C:/Users/teric/Desktop/geckodriver.exe") #path to local geckodriver file which allows selenium to run
    options.headless = False #runs it headless
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://www.trulia.com/sold/13079_c/LOT%7CLAND_type/2p_ls/6_srl/")
    time.sleep(5)
    #first we find the ul with the list of data that we need
    trulia_ul = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/ul")
    #the length of the trulia_li will tell us how much data we have without getting into the 'Similar vacant lots near you" data
    trulia_li = trulia_ul.find_elements(By.TAG_NAME, 'li')
    time.sleep(5)
    #Get a list of the acres data
    acres_list = []
    for i in range(len(trulia_li)):
        try:
            acres = trulia_ul.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/ul/li[{i+1}]/div/div/div/div/div[1]/div[3]/span[2]/span")
            acres_list.append(acres.text)
        except:
            try:
                acres = trulia_ul.find_element(By.CSS_SELECTOR, f"div.SearchResultsList__Container-sc-14hv67h-0:nth-child(1) > ul:nth-child(2) > li:nth-child({i+1}) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > span:nth-child(1) > span:nth-child(1)")
                acres_list.append(acres.text)
            except:
                pass
    print(acres_list)
    #get a list of the price data
    time.sleep(3)
    price_list = []
    for i in range(len(trulia_li)):
        try:
            price = trulia_ul.find_element(By.CSS_SELECTOR, f"div.SearchResultsList__Container-sc-14hv67h-0:nth-child(1) > ul:nth-child(2) > li:nth-child({i+1}) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
            price_list.append(price.text)
        except:
            pass
    print(price_list)
    #get a list of the address data
    time.sleep(3)
    address_list = []
    for i in range(len(trulia_li)):
        try:
            address = trulia_ul.find_element(By.CSS_SELECTOR, f"div.SearchResultsList__Container-sc-14hv67h-0:nth-child(1) > ul:nth-child(2) > li:nth-child({i+1}) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(3) > div:nth-child(1)")
            address_list.append(address.text)
        except:
            pass
    print(address_list)
    trulia_df = pd.DataFrame()
    trulia_df['Acres'] = acres_list
    trulia_df['Acres'] = 'None Found'
    trulia_df['Price'] = price_list
    trulia_df['Address'] = address_list
    trulia_df["Address"] = trulia_df["Address"].str.replace("\n", " ")
    trulia_df['sale_sold'] = 'sale'
    trulia_df['source'] = 'trulia.com'
    print(trulia_df)

    # trulia_df.to_csv("C:/Users/teric/Desktop/vacantLandData/TruliaForSoldFinal.csv")
    driver.close()
    return trulia_df

tru_sale = get_trulia_for_sale_data()
tru_sold = get_trulia_for_sold_data()

def concat_data(frames = [tru_sale, tru_sold, zil_sold, zil_sale, land_sale, land_sold]):
    all_data_df = pd.concat(frames)
    all_data_df.to_csv("C:/Users/teric/Desktop/vacantLandData/ALLDataFinal.csv")

concat_data()


