import requests as r
from bs4 import BeautifulSoup
import pandas as pd
import json
from numpy import random #Adding sleep (prevent DDOS)
from time import sleep #Adding sleep (prevent DDOS)

# Arrays for storing the scraped data before its converted into CSV by Pandas library.
#region Data Storage Arrays
address =[]
house_price = []
property_id = []
page_number = 0 # The url goes up by 24 each time.
#endregion



property_type = input("Please type one of the following 'detached', 'semi-detached', 'terraced', 'flat', 'bungalow', 'park-home': ")

number_of_bedrooms = int(input("Please enter the amount of bedrooms you have: "))



location_code = {
    "canterbury" : "5E279",
    "faversham" : "5E507"
}
print(location_code["canterbury"])

location = (input("Please enter location: "))
if location in location_code:
    location = location_code[location]
else:
    print("Please try a different location")



# Uses the URL to retrieve the HTML code and uses the bs4 library to make it parseable.
#region URL and HTML requests
URL = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{location}&maxBedrooms={number_of_bedrooms}&minBedrooms={number_of_bedrooms}&propertyTypes={property_type}&secondaryDisplayPropertyType=detachedshouses&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
page = r.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
#endregion
print(URL)          #TESTING - TO BE REMOVED.======================================================
# Gives us the total number of listings from search query.
numberOfListings = soup.find("span", {"class": "searchHeader-resultCount"})
numberOfListings = numberOfListings.get_text()
numberOfListings = int(numberOfListings.replace(",", ""))
lastListing = 0


    # Reduces the code down to make finding the correct info easier.
property_search = soup.find(id="propertySearch")
container = property_search.find(id="propertySearch-results-container")
search_results = container.find(id="l-searchResults")
house_listings = search_results.find_all('div', class_="l-searchResult is-list")

for house_listing in house_listings:

        # Uses a for loop to iterate through each of the search listings and scrapes the relevant data.
        address_element = house_listing.find('meta', itemprop="streetAddress")
        #bed_element = house_listing.find_all('span', class_="text")
        bath_element = house_listing.find()
        price_element = house_listing.find("div", class_="propertyCard-priceValue")
        id_listing = house_listing.find('a',"propertyCard-anchor","id")
        id_listing = id_listing.attrs['id']

        #ADD BED
        #test1 = r.get(house_listing.find('div', class_='property-information'))

       # print(test1)


        #bed_element = house_listing.find('div', class_='property-information')
        #bed_tag = bed_element.find('span')
        #bed_no = bed_tag.attrs['class':'text']
        #print(bed_amount)

        # Appends the data to the arrays at the top of the code.
        property_id.append(id_listing)
        address.append(address_element['content'])
        house_price.append(price_element.text)






waitTime = random.uniform(1, 8)  # generates a random number between 1-8 seconds.
print(waitTime) # Shows the randomly generated wait time i.e X seconds.
page_number = 48 # The URL page number goes up by 24 each time.
lastListing = lastListing+1 # Keeps track of property numbers.
sleep(waitTime) # Adds delay of between 1 - 8 seconds.


#Data export to a .CSV file using the Pandas library.
data = {
    "Address": address,
    "Price" : house_price,
    "Property ID" : property_id
}
df=pd.DataFrame.from_dict(data)
df.to_csv(r"TestData.csv", encoding="utf-8")