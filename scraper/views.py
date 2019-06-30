from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd

from cleansor.views import featPrep

# Create your views here.

def houseScraper(weblink):

    url = "https://www.trulia.com/p/nj/short-hills/26-campbell-rd-short-hills-nj-07078--2006164351"

    headers = {'User-Agent': 'Chrome/56.0.2661.102'}
    page = requests.session().get(weblink, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')

    feat = featPrep(soup)

    return feat



