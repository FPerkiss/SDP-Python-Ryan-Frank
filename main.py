import requests as r
from bs4 import BeautifulSoup
import pandas as pd
from numpy import random  # Adding sleep (prevent DDOS)
from time import sleep  # Adding sleep (prevent DDOS)

# Arrays for storing the scraped data before its converted into CSV by Pandas library.
# region Data Storage Arrays
address = []
house_price = []
property_id = []
page_number = 0  # The url goes up by 24 each time.
# endregion

print("Please type one of the following 'detached', 'semi-detached', 'terraced', 'flat', 'bungalow', 'park-home':")
property_type = input()
number_of_bedrooms = int(input("Please enter the amount of bedrooms you have: "))
location_codes = {
    "canterbury": "5E279", "faversham": "5E507", "kent": "5E61307"
}

locationTrue = 0
while locationTrue == 0:
    location = input("Please enter location: ").lower()
    if location in location_codes:
        location = location_codes[location]
        locationTrue = 1
    else:
        print("Please try a different location.")

# Uses the URL to retrieve the HTML code and uses the bs4 library to make it parseable.
# region URL and HTML requests
URL = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{location}&maxBedrooms={number_of_bedrooms}&minBedrooms={number_of_bedrooms}&radius=0.0&index={page_number}&propertyTypes={property_type}&secondaryDisplayPropertyType=detachedshouses&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
page = r.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
# endregion

# Gives us the total number of listings from search query.
numberOfListings = soup.find("span", {"class": "searchHeader-resultCount"})
numberOfListings = numberOfListings.get_text()
numberOfListings = int(numberOfListings.replace(",", ""))
lastListing = 0
urlPages = numberOfListings / 24
# Reduces the code down to make finding the correct info easier.
property_search = soup.find(id="propertySearch")
container = property_search.find(id="propertySearch-results-container")
search_results = container.find(id="l-searchResults")
house_listings = search_results.find_all('div', class_="l-searchResult is-list")


totalCount = 0
while totalCount < numberOfListings:
    URL = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{location}&maxBedrooms={number_of_bedrooms}&minBedrooms={number_of_bedrooms}&radius=0.0&index={page_number}&propertyTypes={property_type}&secondaryDisplayPropertyType=detachedshouses&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="
    waitTime = random.uniform(1, 8)  # generates a random number between 1-8 seconds.
    #print(f"wait time: {waitTime}")  # Shows the randomly generated wait time i.e X seconds.
    sleep(waitTime)  # Adds delay of between 1 - 8 seconds.

    #print(f"No of listings {totalCount} / {numberOfListings} ")
    #print(f"Url: {URL}")
    #print(f"Page no: {page_number}")
    count = 0
    page_number = page_number + 24


    while count < 24:
    # For loop scrape the info from each listing.
        for house_listing in house_listings:

            # Uses a for loop to iterate through each of the search listings and scrapes the relevant data.
            address_element = house_listing.find('meta', itemprop="streetAddress")
            price_element = house_listing.find("div", class_="propertyCard-priceValue")
            id_listing = house_listing.find('a', "propertyCard-anchor", "id")
            id_listing = id_listing.attrs['id']

            # Appends the data to the arrays at the top of the code.

            if id_listing not in property_id:
                property_id.append(id_listing)
                address.append(address_element['content'])
                house_price.append(price_element.text)
                count = count + 1
                totalCount = totalCount + 1
                #print(f"Count: {count} (Inside if statement)")
            else:
                count = count + 1

# Data export to a .CSV file using the Pandas library.
# region Pandas .CSV converter
data = {
    "Address": address,
    "Price": house_price,
    "Property ID": property_id
}
df = pd.DataFrame.from_dict(data)
df.to_csv(rf"{location}.csv", encoding="utf-8")
# endregion
