#!/bin/sh
# coding: utf-8
#https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyBNphpzmEaN30wVqQnOKYf0ATlXcnyDzX0&location=37.7823283,-122.2893865&radius=200
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
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string
import requests
import json
import signal
from xml.etree import ElementTree
app = Flask(__name__)

caps = DesiredCapabilities.PHANTOMJS
caps["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"


varAndXPath = {
                "estimate": "//*[@id='content']/div[5]/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div",
                'beds':"//*[@id='basicInfo']/div[2]/div[1]/div[1]/div",
                'baths':"//*[@id='basicInfo']/div[2]/div[1]/div[2]/div",
                'finishedSqFt':"//*[@id='basicInfo']/div[2]/div[1]/div[3]/div",
                #'unfinishedSqFt':"//*[@id='basicInfo']/div[2]/div[1]/div[4]/div",
                'totalSqFt':"//*[@id='basicInfo']/div[2]/div[1]/div[5]/div",
                'floors':"//*[@id='basicInfo']/div[2]/div[1]/div[6]/div",
                'lotSize':"//*[@id='basicInfo']/div[2]/div[1]/div[7]/div",
                #'style':"//*[@id='basicInfo']/div[2]/div[1]/div[7]/div",
                'yearRenovated':"//*[@id='basicInfo']/div[2]/div[1]/div[10]/div",
                'county':"//*[@id='basicInfo']/div[2]/div[1]/div[11]/div",
                'apn':"//*[@id='basicInfo']/div[2]/div[1]/div[12]/div",
                #"units":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[1]/div[2]/div[1]/ul/div/li/span",
                "rooms":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[1]/div[2]/div[2]/ul/div/li/span",
                #"primaryGarageType":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[2]/div[2]/div[1]/ul/div/li[1]/span",
                #"parkingType":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[2]/div[2]/div[1]/ul/div/li[2]/span",
               # "structuralStyle":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[2]/div[2]/div[2]/ul/div/li[1]/span",
                #"frameworkStructuralMaterial": "//*[@id='property-details-scroll']/div/div[2]/div/div/div[2]/div[2]/div[2]/ul/div/li[2]/span",
                #"constructionQuality":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[2]/div[2]/div[2]/ul/li[1]/span",
                #"buildingShape":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[2]/div[2]/div[2]/ul/li[2]/span",
                #"lastLandAppraisal":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[2]/div[2]/div[3]/ul/div/li/span",
                #"lotSize":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[3]/div[2]/div[1]/ul/div/li/span",
                #"buildingSqFt":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[3]/div[2]/div[2]/ul/div/li[1]/span",
                #"totalStories":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[3]/div[2]/div[2]/ul/div/li[2]/span",
                #"totalStructuralSqFt":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[3]/div[2]/div[2]/ul/div/li[2]/span",
                #"totalStructureDesc":"//*[@id='property-details-scroll']/div/div[2]/div/div/div[3]/div[2]/div[2]/ul/li[2]/span",
                #"allBuildingsOnPropertySqFt": "//*[@id='property-details-scroll']/div/div[2]/div/div/div[3]/div[2]/div[2]/ul/li[3]/span",
                #"totalAssessorSqFt": "//*[@id='property-details-scroll']/div/div[2]/div/div/div[3]/div[2]/div[2]/ul/li[4]/span",
                #"permittedRemodelYear": "//*[@id='property-details-scroll']/div/div[2]/div/div/div[3]/div[2]/div[2]/ul/li[5]/span",
               # "numOfStructures": "//*[@id='property-details-scroll']/div/div[2]/div/div/div[3]/div[2]/div[2]/ul/li[6]/span"
            }

zillowXPaths = {
    "estimate": "//*[@id='home-value-wrapper']/div[1]/div[2]/span[2]",
    "beds": "//*[@id='hdp-content']/div[2]/div[1]/div[1]/header/h3/div/span[2]",
    "baths": "//*[@id='hdp-content']/div[2]/div[1]/div[1]/header/h3/div/span[4]",
    "sqft": "//*[@id='hdp-content']/div[2]/div[1]/div[1]/header/h3/div/span[6]",
    "yearBuilt": "//*[@id='hdp-content']/div[2]/div[1]/section[1]/div[2]/div/div[1]/div[2]/div/div[2]/div",
    "lotSize": "//*[@id='hdp-content']/div[2]/div[1]/section[1]/div[2]/div/div[1]/div[6]/div/div[2]/div",
    "roomCount": "//*[@id='yui_3_18_1_2_1498856895577_951']/div[2]/div[1]/div[3]/ul/li/span[2]"
}

def getExactAddress(searchString):
    gmapresult = requests.get("http://maps.googleapis.com/maps/api/geocode/json?address="+searchString).text
    jdata = json.loads(gmapresult)
    status = jdata.get('status')
    if (status == "OK"):
        results = jdata.get('results')
        result = results[0]
        geography = result['geometry']
        location = geography["location"]
        lat = repr(location["lat"])
        lng = repr(location["lng"])
        requrl = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+lng+"&key=AIzaSyBNphpzmEaN30wVqQnOKYf0ATlXcnyDzX0"
        addresult = requests.get(requrl).text
        jdata = json.loads(addresult)
        results = jdata.get('results')
        for item in results:
            types = item.get('types')
            if "premise" in types:
                return item.get('formatted_address')
                
    elif (status == "ZERO_RESULTS"):
        return "Address non-existent in Google Maps"
    else:
        return "Google Maps " + status


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
            
def search_redfin(search_string, array):
    try: 
         driver = webdriver.PhantomJS('./mac/phantomjs', desired_capabilities=caps)
    except:
        driver = webdriver.PhantomJS('./linux/phantomjs', desired_capabilities=caps)  # Optional argument, if not specified will search path.
    def tryPath(xpath):
            try:
                item = driver.find_element(By.XPATH, xpath)
                return item.text
            except (NoSuchElementException):
                return 'not found'
           
    addressInfo = {}
    driver.get(search_string)
    source = driver.page_source
    bsObj = BeautifulSoup(source, "lxml")
    sibling = bsObj.findAll("h3", { "class" : "r" })
    if len(sibling) >= 1:
        link = sibling[0].a['href']
        link
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
        bsObj = BeautifulSoup(source, "lxml")
        try:
            print("waiting for redfin")
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='content']/div[5]/div[2]/div/div/div/div[2]/div[1]/h1/span/span[1]/span[1]")))

            print("Found")
            addressInfo['type'] = 'redfin'
            for var, xpath in varAndXPath.iteritems():
                item = tryPath(xpath)
                addressInfo[var] = item 


            sibling5 = bsObj.find("div", {"class": "walk-score"})
            addressInfo["walk_score"] = 0
            addressInfo["transit_score"] = 0
            if sibling5:
                percentages = sibling5.div.findAll("div", {"class":"percentage"})
                if len(percentages) > 0:
                    addressInfo["walk_score"] = percentages[0].get_text()
                if len(percentages) > 1:
                    addressInfo["transit_score"] = percentages[1].get_text()
            history = [] 
            try:
                sibling6 = bsObj.find("section", {"class" : "PropertyHistory"}).find("div", {"class" : "main-content"}).div.table.tbody
                rows = sibling6.findAll("tr", {"class": "PropertyHistoryEventRow"})
                for row in rows:
                    section = row.findAll("td")
                    date = section[0].get_text()
                    status = section[1].get_text()
                    price = section[2].get_text()
                    history.append({
                        "date" : date,
                        "status" : status,
                        "price" : price
                    })
            except (AttributeError):
                pass
            addressInfo["history"] = history

            schools = []
            try:
                sibling7 = bsObj.find("section", {"class" : "SchoolsSection"}).find("div", {"class" : "main-content"}).find("div", {"class": "schools-content"}).div.table.tbody.findAll("tr")
                for item in sibling7:
                    infos = item.findAll("td", {"class" : "name-col"})
                    for info in infos:
                        #print info
                        rating = info.find("div", {"class": "rating"}).div.get_text()
                        name = info.find("div", {"class": "name-and-info"}).a.get_text()
                        schoolInfo = info.find("div", {"class": "name-and-info"}).div


                        infoArray = schoolInfo.get_text().split(" — ")
                        infoText = infoArray[0] + " " + infoArray[1]
                        schools.append({
                            "name" : name,
                            "info": infoText,
                            "rating": rating
                        })
            except (AttributeError):
                pass

            addressInfo["schools"] = schools


            return addressInfo
        except:
            return False
        finally:
            driver.service.process.send_signal(signal.SIGTERM)
            driver.quit()



    else: 
        #bad link
        driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()
        return False
        
    




    
def search_zillow(search_string, array):
    try: 
         driver = webdriver.PhantomJS('./mac/phantomjs', desired_capabilities=caps)
    except:
        driver = webdriver.PhantomJS('./linux/phantomjs', desired_capabilities=caps)  # Optional argument, if not specified will search path.
            
    addressInfo = {}
    
    addressArray = getExactAddress(search_string).split(",")
    citystatezip = addressArray[1] + addressArray[2]
    r = requests.post("http://www.zillow.com/webservice/GetSearchResults.htm", data={'zws-id': "X1-ZWz1fuv8v7kdmz_5m9vn", 'address':addressArray[0] , "citystatezip":citystatezip })

    print(r.status_code, r.reason)
    if (r.status_code == 200):
        content = ElementTree.fromstring(r.content)
        response = content.find("response")
        results = response.find("results")
        result = results.find("result")
        links = result.find("links")
        homedetails = links.find("homedetails")
        link = homedetails.text
    else:
        zillowString="https://www.google.com/#q="+search_string +"zillow"
        driver.get(zillowString)

        source = driver.page_source
        bsObj = BeautifulSoup(source, "lxml")

        sibling = bsObj.findAll("h3", { "class" : "r" })

        if len(sibling) >= 1:
            link = sibling[0].a['href']
            link
        else:
            return False

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
        print(link)
        driver.get(link)
        source = driver.page_source
        bsObj = BeautifulSoup(source, "lxml")


        print("here")
        try:
            print("waiting for zillow")
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "hdp-content")))
            print("Found")
            estimate = "Price Unknown"
            rentEstimate = "Price Unknown"
            #zillow
            sibling = bsObj.findAll("div", { "class" : "home-summary-row" })
            for item in sibling:
                if '  Zestimate' in item.get_text():
                    if len(item.get_text().split('$')) >= 2:
                        estimate = item.get_text().split('$')[1]
                if 'Rent Zestimate' in item.get_text():
                    if len(item.get_text().split('$')) >= 2:
                        rentEstimate = item.get_text().split('$')[1]

            sibling1 = bsObj.findAll("span", { "class" : "addr_bbs" })
            sibling2 = bsObj.findAll("div", { "class" : "hdp-fact-ataglance-value" })

            history = []
            try:
                sibling3 = bsObj.findAll("section", {"class" : "zsg-content-section"})
                for item in sibling3:
                    item2 = item.find("div", {"id" : "hdp-price-history"})
                    if (item2):
                        rows = item2.div.table.tbody.findAll("tr")
                        for row in rows:
                            info = row.findAll("td")
                            if len(info) >= 3:
                                history.append ({
                                    "date" : info[0].get_text(),
                                    "status" : info[1].get_text(),
                                    "price" : info[2].get_text()
                                })
            except:
                pass

            schools = []
            try:
                sibling4 = bsObj.findAll("section", {"id" : "nearbySchools"})
                for item in sibling4:
                    item2 = item.div.findAll("div", {"class" : "zsg-content-item"})
                    for content in item2:
                        ul = content.findAll("ul", {"class" : "nearby-schools-list"})
                        for lists in ul:
                            listItems = lists.findAll("li", {"class":"nearby-school"})
                            for listItem in listItems:
                                rating = listItem.find("div", {"class":"nearby-schools-rating"}).span.get_text()
                                name = listItem.find("div", {"class":"nearby-schools-name"}).a.get_text()
                                grades = listItem.find("div", {"class":"nearby-schools-grades"}).get_text()
                                distance = listItem.find("div", {"class":"nearby-schools-distance"}).get_text()
                                schools.append({
                                    "name": name,
                                    "info": distance + " " + grades,
                                    "rating": rating
                                })
            except: 
                 pass

        except:
            driver.service.process.send_signal(signal.SIGTERM)
            driver.quit()
            print("Fail")
            return False

        addressInfo = {
            'type': 'zillow',
            'estimate':estimate if estimate else None,
            'rentEstimate':rentEstimate if rentEstimate else None,
            'beds': sibling1[0].get_text() if sibling1 else None,
            'baths':sibling1[1].get_text() if sibling1 else None,
            'sqft': sibling1[2].get_text() if sibling1 else None,
            "yearBuilt": sibling2[1].get_text() if sibling2 else None,
            "type": sibling2[0].get_text() if sibling2 else None,
            "yearBuilt": sibling2[1].get_text() if sibling2 else None,
            "Heating": sibling2[2].get_text() if sibling2 else None,
            "Cooling": sibling2[3].get_text() if sibling2 else None,
            "Parking": sibling2[4].get_text() if sibling2 else None,
            "Lot": sibling2[5].get_text() if sibling2 else None,
            "history" : history if len(history) > 1 else [],
            "schools" : schools if len(schools) > 1 else []
        }
        driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()
        return addressInfo

    else: 
        #bad link
        driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()
        return False

    
@app.route('/getredfin', methods=['POST'])
def getRedfin():
    try:
        address = request.json.get('address').lower()
    except:
        return jsonify({
            "error" : "Request Error"
        })
        
    array = address.split()
    searchString = ""
    for word in array:
        searchString+=word 
        searchString+="+"

    redfinString="https://www.google.com/#q="+searchString +"redfin"
    zillowString="https://www.google.com/#q="+searchString +"zillow"
    redfinInfo = search_redfin(redfinString, array)
    if redfinInfo != False:
        return jsonify(redfinInfo)
    else:
        return jsonify({
            "Error" : "Address Not Found"
        })

@app.route('/getzillow', methods=['POST'])
def getZillow():
    try:
        address = request.json.get('address').lower()
    except:
        return jsonify({
            "error" : "Request Error"
        })
    array = address.split()
    searchString = ""
    for word in array:
        searchString+=word 
        searchString+="+"
        
    zillowInfo = search_zillow(searchString, array) 
    if zillowInfo != False:
        return jsonify(zillowInfo)
    else:
        return jsonify({
            "Error" : "Address Not Found"
        })
            
            
           
    
    
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
    
    
