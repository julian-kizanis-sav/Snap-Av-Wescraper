#SAV Digital Enviroments
#Julian Kizanis
print("Powered by Anaconda")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
#from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
#from pandas import DataFrame
import pandas as pd
#import os
import time
import csv
import re

modelIndex = 0
Height = []
Width = []
Depth = []
specURL = []
RvtURL = []
WarrantiesShort = []
WarrantiesLong = []
tempURL =""
attempts = 0
modelNumber = ""
noSpec = 0
noCAD = 0
noRVT = 0
shortDelay = .5

#converts a csv file into a python list
with open('SnapAvModelList.csv', 'r') as f:
    reader = csv.reader(f)
    ModelNumbersTemp = list(reader)
ModelNumbers = [j for sub in ModelNumbersTemp for j in sub]

#opens the snapav website
webdriver.ChromeOptions().add_experimental_option('excludeSwitches', ['enable-logging'])	#removes an artifact in the command window
driver = webdriver.Chrome()	#opens a chrome browser
modelURL = f"https://www.snapav.com/shop/en/snapav/home"
driver.get(modelURL)   

for modelIndex, model in enumerate(ModelNumbers):	#loops through the models 
	attempts = 0
	while attempts < 3:	#improves stability
		searchBox = driver.find_element_by_xpath("(//input[@name='searchTerm'])")	#finds the search box
		searchBox.send_keys(model)	#Enters the model number into the search box
		driver.find_element_by_xpath("(//a[@class='btn-search'])").click()	#clicks the  search button
		attempts = 3	#exit while loop
	specURL.insert(modelIndex,modelURL)	#inserts the model's URL into the specURL list
	

	try:
		driver.find_element_by_xpath("(//div[@id='tab-specs'])").click()	#finds and clicks the specs tab
	except NoSuchElementException:	#when the specs tab doesn't exist
		#we will check if there are more than one search result
		soup = BeautifulSoup(driver.page_source, 'lxml')   #creates a beautifulSoup object called soup
		
		tempSoup = soup.findAll("div", {"class":"item-part-number"}).text#finds all the search results
		if model in tempSoup:	#checks if the result matches what we are looking for
			driver.get(tempSoup.parent.find("a", href = True)['href'])#finds and gos to the link imbedded in the search result
		
	soup = BeautifulSoup(driver.page_source, 'lxml')   #creates a beautifulSoup object called soup
	Columns = soup.find("div", {"class":"border-table-holder"}).findAll("tbody")	#finds the spec chart
	for columnIndex in range(len(Columns)):	#there should be two columns
		if columnIndex == 0:
			Entries = Columns[columnIndex].findAll()	#finds the rows in column one
		elif columnIndex == 1:
			Information = Columns[columnIndex].findAll()	#finds the rows in column two

	for entryIndex in range(len(Entries)):
		if "Dimensions (W x H x D)" in Entries[entryIndex].text:
			WxHxD = Information[entryIndex].text.split(" x ")
			for dimIndex in range(len(WxHxD)):
				if dimIndex == 0:
					Width.insert(modelIndex, WxHxD[dimIndex])

	wSoup = soup.find("div", {"id":"warranty"})
	print(wSoup)
	WarrantiesShort.insert(modelIndex, wSoup.h3.text)
	print(WarrantiesShort[modelIndex])
	WarrantiesLong.insert(modelIndex, wSoup.p.text)
	print(WarrantiesLong[modelIndex])

	df = pd.DataFrame(list(zip(ModelNumbers, Height, Width, Depth, specURL)), columns =['Model Number', 'Height', 'Width', 'Depth', 'URL'])  
    #df is a panda object that contains: ModelCategory, ModelName, ModelPdf
	export_csv = df.to_csv ('PanasonicSpecSheet HxWxD URL.csv', header=True) #Don't forget to add '.csv' at the end of the path
