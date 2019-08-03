from django.shortcuts import render
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

from cleaner.views import featPrep

# Create your views here.


def houseScraper(weblink):

    headers = {'User-Agent': 'Chrome/75.0.3770.100'}#'Chrome/56.0.2661.102'
    page = requests.session().get(weblink, headers=headers)
    # print(page.cookies)


    if not page:
        print(page.content)

    # maxcount = 10
    # while (not page) and maxcount:
    #
    #     page = requests.session().get(weblink, headers=headers)
    #     maxcount -= 1
    #     print("connection issue")

    soup = BeautifulSoup(page.content, 'html.parser')

    feat = featPrep(soup)

    print(feat)

    return feat

