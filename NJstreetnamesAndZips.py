# Before you read this code, I encourage you to go to https://geographic.org/streetview/usa/nj/index.html
# Clicking on a county will bring you to a page that has all the municipalities located within that county
# Clicking on a municipality will bring you to a page that lists all street names and corresponding zip codes in that municipality
# Zip codes in NJ all start with the number zero, but this site is not showing that leading zero
# Nonetheless I was able to add a zero onto the beginning of the zip codes, as you will see below


# all in all, this code goes through each municipality in each NJ county and grabs all the street names and corresponding zip codes
# the hard part is storing these in a data structure

import time
import re
import bs4
import requests
from selenium import webdriver
import pandas


# set up selenium and give it time to launch the browser
driver = webdriver.Firefox()
time.sleep(20) # my computer is slow, so giving it 20 seconds to launch the browser

# go to the website that has all street names in New Jersey
driver.get('https://geographic.org/streetview/usa/nj/index.html')
time.sleep(10) # giving it 10 seconds to load the site

# create a Requests object for the site that has a list of NJ counties
reqoListofCounties = requests.get('https://geographic.org/streetview/usa/nj/index.html')

# making soup for the Requests object
soupCounties = bs4.BeautifulSoup(reqoListofCounties.text, 'html.parser')

# create empty list where names of counties will be stored, will iterate through this later
listofCounties = []

# loop to grab names of counties and store them into empty list
for i in soupCounties.find_all('a'):
        listofCounties.append(i.get('alt'))
listofCounties = [i for i in listofCounties if i is not None]

# empty list where county css selectors will be stored, will iterate through this later
listofCountyCSSselectors = []

# pull css selectors of county page into list
# each county css selector is the same except for 1 integer. I'm able to insert the index number of the loop

for i in range(1,22): # there are 21 counties in NJ, and all 21 displayed on page
        listofCountyCSSselectors.append('.listspan > ul:nth-child(1) > li:nth-child(' + str(i) + ') > a:nth-child(1)')
        # the line above, line 48, stores the css selectors for each county into the empty list created in Line 42
print(listofCountyCSSselectors) # could probably comment this line out, but wanted to print to see that I'm doing it right

# now we have a list of all the county css selectors


# nested for loop that clicks on each county, stores css selectors for each municipality into an empty list, clicks on each
# municipality, and grabs the street names and corresponding zip codes.
for i in range(len(listofCounties)): # I want to iterate through each county
        driver.find_element_by_css_selector(listofCountyCSSselectors[i]).click()
        time.sleep(10) # gives page 10 seconds to load
        currentreqo = requests.get(driver.current_url) #creates a Requests object for the page that shows a county's municipalities
        currentsoup = bs4.BeautifulSoup(currentreqo.text, 'html.parser') # make soup for the above Requests object
        listofTowns = [] # empty list where the names of each municipality will be stored, will iterate through this later
        for i in currentsoup.find_all('a'): # loop that grabs the names of each municipality in the soup
                listofTowns.append(i.get('alt')) # stores names of municipalities into the empty list created on Line 62
        listofTowns = [i for i in listofTowns if i is not None] # removes None types from list of muncipalities
        print('list of towns: ', listofTowns) # could probably comment this line out
        listofTownCSSselectors = [] # create empty list where each municipality's css selector will be stored
        for i in range(1, len(listofTowns)+1): # same idea as Line 47 but had to add 1 so the index wasn't out of range
                listofTownCSSselectors.append('.listspan > ul:nth-child(1) > li:nth-child(' + str(i) + ') > a:nth-child(1)')
                print('town selectors', listofTownCSSselectors) # could comment this line out, just wanted to see the list
        if len(listofTowns) == len(listofTownCSSselectors): #checks if there are as many css selectors as there are municipalities
                print('successfully grabbed town css selectors')
        else:
                print('oh snap ', 'length of towns: ', len(listofTowns), 'length of town selectors: ', len(listofTownCSSselectors))
        # Line 74 rarely executes. I know I should use a Try block here but I will optimize this code later
        for i in range(len(listofTowns)):
                driver.find_element_by_css_selector(listofTownCSSselectors[i]).click() #clicks on the i'th municipality css selector
                time.sleep(5) # gives page 5 seconds to load
                townreqo = requests.get(driver.current_url) # creates Requests object for the i'th municipality
                townsoup = bs4.BeautifulSoup(townreqo.text, 'html.parser') # creates soup for the page of the i'th municipality
                listofStreets = [] # emtpy list where street names will be stored
                for i in townsoup.find_all('a'): # grabs street names from HTML
                        listofStreets.append(i.get('alt')) # stores street names into empty list
                listofStreets = [i for i in listofStreets if i is not None] # removes None types from list of Street Names
                print(listofStreets) # could comment this line out
                listofzips = [] # empty list to store zip codes
                for i in townsoup.find_all('li'): # grabs street names AND zip codes from soup, this is the only way I could get zip
                        listofzips.append(re.compile(r'(\xa0)(\s)(\d+)').search(i.text).group(3)) # grabs only the zips from regex
                ziplist = ['0' + i for i in ziplist] # adds a zero to the front of each zip, b/c NJ zips start with 0
#print('done town: ', listofTowns[i])    ## don't worry about this line
                driver.back() # goes back to page that displays municipalities for a given county
        driver.back() # goes back to page that displays each county in NJ

        
       
#### So basically I was able to go though each municipality in each county and grab the Street names & zip codes
#### my problem now is figuring out how to store these street names
