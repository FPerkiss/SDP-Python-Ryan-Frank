import requests as r
from bs4 import BeautifulSoup
import pandas as pd
import re
from numpy import random #Adding sleep (prevent DDOS)
from time import sleep #Adding sleep (prevent DDOS)

address =[]
house_price = []

URL = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E61307&index={page_number}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
page = r.get(URL)
soup = BeautifulSoup(page.content, "html.parser")




#Gives us a number of listings
numberOfListings = soup.find("span", {"class": "searchHeader-resultCount"})
numberOfListings = numberOfListings.get_text()
numberOfListings = int(numberOfListings.replace(",", ""))

lastListing = 0

if numberOfListings >= lastListing:

    property_search = soup.find(id="propertySearch")
    container = property_search.find(id="propertySearch-results-container")
    search_results = container.find(id="l-searchResults")
    house_listings = search_results.find_all('div', class_="l-searchResult is-list")

    for house_listing in house_listings:
        address_element = house_listing.find('meta', itemprop="streetAddress")
        # bed_element = house_listing.find('div', class_="property-information")
        bed_element = house_listing.find_all('span', class_="text")
        bath_element = house_listing.find()
        price_element = house_listing.find("div", class_="propertyCard-priceValue")

        #print(address_element['content'])
        address.append(address_element['content'])
        house_price.append(price_element.text)



    waitTime = random.uniform(1, 8)  # Random number between 1-8 seconds
    print(waitTime) #Waits for x seconds
    page_number = +24 # The url goes up by 24 each time.
    lastListing = lastListing+1 #Keeps track of property number
    sleep(waitTime) # Adds delay of between 1 - 8 seconds


print(address)
print(house_price)



#Data export
data = {
    "Address": address,
    "Price" : house_price

}
df=pd.DataFrame.from_dict(data)
df.to_csv(r"TestData.csv", encoding="utf-8")


