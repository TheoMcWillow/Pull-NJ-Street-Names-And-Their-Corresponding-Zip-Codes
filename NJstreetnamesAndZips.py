import time
import re
import bs4
import requests
from selenium import webdriver
import pandas


time.sleep(5)

driver = webdriver.Firefox()
time.sleep(20)

driver.get('https://geographic.org/streetview/usa/nj/index.html')
time.sleep(10)

reqoListofCounties = requests.get('https://geographic.org/streetview/usa/nj/index.html')

soupCounties = bs4.BeautifulSoup(reqoListofCounties.text, 'html.parser')
listofCounties = []

for i in soupCounties.find_all('a'):
        listofCounties.append(i.get('alt'))
listofCounties = [i for i in listofCounties if i is not None]


listofCountyCSSselectors = []

#pull css selectors of county page into list
for i in range(1,22):
        listofCountyCSSselectors.append('.listspan > ul:nth-child(1) > li:nth-child(' + str(i) + ') > a:nth-child(1)')
print(listofCountyCSSselectors)
#
for i in range(len(listofCounties)):
        driver.find_element_by_css_selector(listofCountyCSSselectors[i]).click()
        time.sleep(10)
        currentreqo = requests.get(driver.current_url)
        currentsoup = bs4.BeautifulSoup(currentreqo.text, 'html.parser')
        listofTowns = []
        for i in currentsoup.find_all('a'):
                listofTowns.append(i.get('alt'))
        listofTowns = [i for i in listofTowns if i is not None]
        print('list of towns: ', listofTowns)
        listofTownCSSselectors = []
        for i in range(1, len(listofTowns)+1):
                listofTownCSSselectors.append('.listspan > ul:nth-child(1) > li:nth-child(' + str(i) + ') > a:nth-child(1)')
                print('town selectors', listofTownCSSselectors)
        if len(listofTowns) == len(listofTownCSSselectors):
                print('successfully grabbed town css selectors')
        else:
                print('fuck ', 'length of towns: ', len(listofTowns), 'length of town selectors: ', len(listofTownCSSselectors))
        for i in range(len(listofTowns)):
                driver.find_element_by_css_selector(listofTownCSSselectors[i]).click()
                time.sleep(5)
                townreqo = requests.get(driver.current_url)
                townsoup = bs4.BeautifulSoup(townreqo.text, 'html.parser')
                listofStreets = []
                for i in townsoup.find_all('a'):
                        listofStreets.append(i.get('alt'))
                listofStreets = [i for i in listofStreets if i is not None]
                print(listofStreets)
                listofzips = []
                for i in townsoup.find_all('li'):
                        listofzips.append(re.compile(r'(\xa0)(\s)(\d+)').search(i.text).group(3))
                ziplist = ['0' + i for i in ziplist]
#print('done town: ', listofTowns[i])
                driver.back()
        driver.back()

## regex to pull zips along with street names

#probabaly need to put this loop into the nested for loop b/c local variables
listofstreetswithzips = []
for i in townsoup.find_all('li'):
        lsitofstreetswithzips.append(i.text)


rego = re.compile(r'(\xa0)(\s)(\d+)')
