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
    final_land_dotcom_df['Source'] = "Land.com"
    print(final_land_dotcom_df)

    final_land_dotcom_df.to_csv("C:/Users/teric/Desktop/vacantLandData/LandDotComForSaleDataFINAL.csv")
    driver.close()

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
    final_land_dotcom_df['Source'] = "Land.com"
    print(final_land_dotcom_df)

    final_land_dotcom_df.to_csv("C:/Users/teric/Desktop/vacantLandData/LandDotComForSoldDataFINAL.csv")
    driver.close()

# get_land_dotcom_for_sale_data()
# get_land_dotcom_for_sold_data()


def get_land_watch_for_sale_data():
    # use the geckodriver to get to the specific url to find land.com for sale data
    options = Options()
    service = Service("C:/Users/teric/Desktop/geckodriver.exe") #path to local geckodriver file which allows selenium to run
    options.headless = False #runs it headless
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://www.trulia.com/for_sale/13079_c/LOT%7CLAND_type/")

get_land_watch_for_sale_data()





























# def get_zillow_for_sale_data():
#     #use the geckodriver to get to the specific url to find land.com for sale data
#     options = Options()
#     service = Service("C:/Users/teric/Desktop/geckodriver.exe") #path to local geckodriver file which allows selenium to run
#     options.headless = False #runs it headless
#     driver = webdriver.Firefox(service=service, options=options)
#     driver.get("https://www.zillow.com/crawford-county-ga/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Crawford%20County%2C%20GA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-84.35536400316056%2C%22east%22%3A-83.55198875901993%2C%22south%22%3A32.452387492077776%2C%22north%22%3A32.9297118218284%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A2227%2C%22regionType%22%3A4%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22lot%22%3A%7B%22min%22%3A87120%2C%22max%22%3A2178000%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D")
#     zillow_body = driver.find_elements(By.XPATH, "//div[contains(@class, 'property-card-data')]")
    
#     time.sleep(5)
#     print(zillow_body)
#     print(f"THIS IS THE LENGTH OF THE ZILLOW BODY {len(zillow_body)}")
#     counter = 1
#     for i in zillow_body:
#         print(i.text)
#         counter += 1

#     print(f"FINAL COUNTER {counter}")
    # final_list = []
    # for i in zillow_body:
    #     acre = i.find_element(By.XPATH, "//*[contains(text(), 'acre')]").text
    #     address = i.find_element(By.XPATH, "//address[contains(@data-test, 'property-card-addr')]").text
    #     price = i.find_element(By.XPATH, "//span[contains(@data-test, 'property-card-price')]").text
    #     child_list = [acre, address, price]
    #     final_list.append(child_list)
    
    # zillow_for_sale_df = pd.DataFrame(final_list, columns=['Acres', 'Address', 'Price'])
    # print(zillow_for_sale_df)


# get_zillow_for_sale_data()



