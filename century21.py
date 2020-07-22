#!/usr/bin/env python
# coding: utf-8

# In[87]:


import requests
from bs4 import BeautifulSoup

req = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
con = req.content

bsoup = BeautifulSoup(con,"html.parser")

all = bsoup.find_all("div", {"class": "propertyRow"})
all[0].find("h4", {"class": "propPrice"}).text.replace("\n", "").replace(" ","")

page_num = bsoup.find_all("a", {"class": "Page"})[-1].text


dectionaryList = []

base_url = "http://pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
for page in range(0,int(page_num)*10,10):
    print(base_url + str(page) + ".html")
    req = requests.get(base_url + str(page) + ".html", headers = headers)
    con = req.content
    bsoup = BeautifulSoup(con, "html.parser")
    all = bsoup.find_all("div", {"class": "propertyRow"})


    for item in all:
        dectionary = {}
        dectionary["Price"] = item.find("h4",{"class": "propPrice"}).text.replace("\n", "").replace(" ","")
        dectionary["Address"] = item.find_all("span", {"class": "propAddressCollapse"})[0].text
        try:
            dectionary["Locality"] = item.find_all("span", {"class": "propAddressCollapse"})[1].text
        except:
            dectionary["Locality"] = None
        try:
            dectionary["Beds"] = item.find("span", {"class": "infoBed"}).find("b").text
        except:
            dectionary["Beds"] = None

        try:
            dectionary["Area"] = item.find("span", {"class": "infoSqFt"}).find("b").text
        except:
            dectionary["Area"] = None

        try:
            dectionary["Full Baths"] = item.find("span", {"class": "infoValueFullBath"}).find("b").text
        except:
            dectionary["Full Baths"] = None

        try:
            dectionary["Half Baths"] = item.find("span", {"class": "infoValueHalfBath"}).find("b").text
        except:
            dectionary["Half Baths"] = None

        for column_group in item.find_all("div", {"class": "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}), column_group.find_all("span", {"class": "featureName"})):
                if "Lot Size" in feature_group.text:
                    dectionary["Lot Size"] = feature_name.text

        dectionaryList.append(dectionary)


import pandas
dtFrame = pandas.DataFrame(dectionaryList)

dtFrame.to_csv("Century21Property.csv")

