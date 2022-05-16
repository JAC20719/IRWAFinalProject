# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:31:02 2022

@author: jcane
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path="C:\\Users\\jcane\\Documents\\IRWAFinalProject\\geckodriver.exe")
driver.get('https://www.sidelines.io/nba/odds')
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all('a', title=re.compile("[A-Za-z0-9 ]*vs[A-Za-z0-9 ]*odds \& prediction"))
infos = []
for link in links:
    infos.append([link['title'], link.text, link['href']])
    
spread = []
for info in infos:
    s = info[1].split(' ')
    if len(s) == 6:
        #Then there are predictions
        spread.append([info[2], [p for p in s[2:]]])
    if len(s) == 7 and s[4] != '' and s[6] != '':
        #Then there are predictions
        spread.append([info[2],[p for p in s[3:]]])


#a _ngcontent-yee-c109
print(spread)