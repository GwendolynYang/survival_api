from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import time
# Create your views here.

def houseScraper(weblink):

    url = weblink

    headers = {'User-Agent': 'Chrome/56.0.2661.102'}
    page = requests.session().get(url, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')

    address = get_addr(soup)
    city = get_city(soup)
    curr_price = get_currprice(soup)
    days_listing = get_dayslisting(soup)

    raw = [address, city, curr_price, days_listing]
    #TODO:
    # Price history is required. Month and date required
    # Listing event counting required
    return raw


def get_addr(soup):
    obj = soup.find("span", class_="Text__TextBase-sc-1cait9d-0 dhOdUy")
    if obj is None:
        addr = np.nan
    else:
        addr = obj.get_text()

    return addr


def get_city(soup):
    obj = soup.find("span",
                     class_="HomeSummaryShared__CityStateAddress-vqaylf-0 fyHNRA Text__TextBase-sc-1cait9d-0 hUlhgk")

    if obj is None:
        city = np.nan
    else:
        city = obj.get_text()

    return city

def get_currprice(soup):
    obj = soup.find("h3", id="on-market-price-details")
    if obj is None:
        curr_price = np.nan
    else:
        curr_price = obj.get_text()
        return curr_price

# output strings. deal with number types later in 'cleansor'
        # curr_price.replace(',', '').replace('$', '')
        # return int(curr_price)


def get_dayslisting(soup):

    block = soup.find('ul', id='home-features')

    for obj in block.find_all("li"):
        items = obj.get_text.strip().split(' ')
        if items[1:] == ['Days', 'on', 'Trulia']:
            return int(items[0])  # here returns a integer