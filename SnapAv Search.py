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
RvtURL = []
tempURL =""
attempts = 0
modelNumber = ""
noSpec = 0
noCAD = 0
noRVT = 0
shortDelay = .5


with open('SnapAvModelList.csv', 'r') as f:
    reader = csv.reader(f)
    ModelNumbersTemp = list(reader)
ModelNumbers = [j for sub in ModelNumbersTemp for j in sub]

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome() 
modelURL = f"https://www.snapav.com/shop/en/snapav/home"        
driver.get(modelURL)   
for model in ModelNumbers:
    attempts = 0
    while attempts < 3:
        searchBox = driver.find_element_by_xpath("(//input[@name='searchTerm'])")
        searchBox.send_keys(model)
        driver.find_element_by_xpath("(//a[@class='btn-search'])").click()
        attempts = 3
    specURL.insert(modelIndex,modelURL)  
    modelIndex += 1



    soup = BeautifulSoup(driver.page_source, 'lxml')   #creates a beautifulSoup object called soup
    Columns = soup.find("div", {"class":"border-table-holder"}).findAll("tbody")
    for columnIndex in range(len(Columns)):
        if columnIndex == 0:
            Entries = Columns[columnIndex].findAll()
        elif columnIndex == 1:
            Information = Columns[columnIndex].findAll()

    for entryIndex in range(len(Entries)):
        if "Dimensions (W x H x D)" in Entries[entryIndex].text:
            WxHxD = Information[entryIndex].text.split(" x ")
            for dimIndex in range(len(WxHxD)):
                if dimIndex == 0:
                    Width.insert(modelIndex, WxHxD[dimIndex])



    df = pd.DataFrame(list(zip(ModelNumbers, Height, Width, Depth, specURL)), columns =['Model Number', 'Height', 'Width', 'Depth', 'URL'])  
    #df is a panda object that contains: ModelCategory, ModelName, ModelPdf
    export_csv = df.to_csv ('PanasonicSpecSheet HxWxD URL.csv', header=True) #Don't forget to add '.csv' at the end of the path
