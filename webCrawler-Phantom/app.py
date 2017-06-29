#!/bin/sh
# coding: utf-8

# In[1]:
from flask import Flask, render_template, request, jsonify, abort, make_response, Response, redirect
from selenium import webdriver
import time
import unicodecsv as csv
import sys;
reload(sys);
sys.setdefaultencoding("utf8")
import codecs

import re
import os
from bs4 import BeautifulSoup
from urllib import urlretrieve
import chardet
from aip import AipFace
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import string

app = Flask(__name__)

caps = DesiredCapabilities.PHANTOMJS
caps["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
    
def search_top(search_string, array, site):
    driver.get(search_string)


    # In[2]:

    source = driver.page_source
    bsObj = BeautifulSoup(source, "html.parser")
    sibling = bsObj.findAll("h3", { "class" : "r" })
    
    if len(sibling) >= 1:
        link = sibling[0].a['href']
        link
        print(link)
    else:
        return 'search not found'

    correct_link = True

    #check if correct link
    for word in array:
        if is_number(word) == True:
            if word in link:
                correct_link = True
            else:
                correct_link = False
                break

    if correct_link == True:
        driver.get(link)


        source = driver.page_source
        bsObj = BeautifulSoup(source, "html.parser")

        if site == 0:
            #redfin
            sibling = bsObj.findAll("div", { "class" : "info-block avm" })
            text = "Price Unknown"
            if len(sibling) >= 1:
                text = sibling[0].find("div", { "class" : "statsValue" }).get_text()


            print(text)
            return text

        elif site == 1:
            value = 0
            #zillow
            sibling = bsObj.findAll("div", { "class" : "home-summary-row" })
            for item in sibling:
                if 'Zestimate' in item.get_text():
                    if len(item.get_text().split('$')) >= 2:
                        value = item.get_text().split('$')[1]

            return value


            '''text = sibling[0].span.get_text()
            print text
            return text'''
            
   
    return 'not found'
driver = webdriver.PhantomJS('./linux/phantomjs', desired_capabilities=caps)  # Optional argument, if not specified will search path.

@app.route('/getprice', methods=['POST'])
def getPrice():
    address = request.json.get('address').lower()
 
    array = address.split()
    searchString = ""
    
    for word in array:
        searchString+=word 
        searchString+="+"
        
    searchString = "https://www.google.com/#q="+searchString
    
    redfinString=searchString +"redfin"
    zillowString=searchString +"zillow"
    
    

        
    result = search_top(redfinString, array, 0)
    if result != 'not found':
        return(jsonify({"estimate":result}))
    else:
        zresult = search_top(zillowString, array, 1)
        if zresult != 'not found':
            return(jsonify({"estimate":zresult}))
        else:
            return 'Address not found'
    
    
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
    
    
