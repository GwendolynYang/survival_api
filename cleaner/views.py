from django.shortcuts import render
import numpy as np
import pandas as pd
#from cleaner.apps import mhv_dict
# Create your views here.


def get_street(soup):
    # get Address
    obj = soup.find("span", class_="Text__TextBase-sc-1cait9d-0 dhOdUy")
    #obj = soup.find("span", attrs={"data-testid": "home-details-summary-headline"})
    #print(obj)
    street = obj.text

    return street


def get_city(soup):
    # get city, State, zipcode
    obj = soup.find("span",
                    class_="HomeSummaryShared__CityStateAddress-vqaylf-0 fyHNRA Text__TextBase-sc-1cait9d-0 hUlhgk")
    city = obj.text
    #print(city)
    return city


def get_dom(soup):
    """
    return int

    """
    # get city, State, zipcode
    objlist = soup.find("ul", attrs={"data-testid": "home-features"})

    for obj in objlist.find_all('li'):
        items = obj.text.strip().split(' ')
        if items[1:4] == ['Days', 'on', 'Trulia']:
            # print(items)
            dom = int(items[0])

    return dom


def get_price_from_h3(soup):
    """
    return int

    Get price from header-3 (h3) in the begining of the page
    Current price. may not be original listing price
    """

    obj = soup.find('h3')

    price_str = obj.text

    price = int(price_str.strip('$').replace(',', ''))

    return price #price_str


def get_price_from_history(priceHistory):
    """
    return int(price), str(date)
    # Get latest listing price
    # If the latest history record is 'sold',
    # then listing price is not in the price history table.
    # Then 'return 0'
    """

    if not priceHistory:
        return 0, 0

    for row in priceHistory:
        if row[2] == 'Sold':
            return 0, 0
        elif row[2] == 'Listed For Sale':
            date = row[0]
            price_str = row[1]
            price = int(price_str.strip('$').replace(',', ''))

            return price_str, price, date


def get_price_history_2(soup):
    """
    return list of lists, i.e, [[date, price, event]], string

    get the price history table from webpage,
    no address, just 3-column table
    """

    objtable = soup.find('div', attrs={"data-testid": "price-history-container"})

    priceHistory = []
    if objtable.find_all('tr') is None:
        priceHistory.append([np.nan, np.nan, np.nan])
    else:
        for tr in objtable.find_all('tr'):
            tempHist = [td.text for td in tr.find_all('td')]
            if len(tempHist) == 3:
                priceHistory.append(tempHist)

    return priceHistory


def get_zipcode(soup):
    obj = soup.find('h1').get_text()
    zipcode = obj.split()[-1]

    return zipcode


def get_lotsize(soup):
    """
    return int
    """

    objlist = soup.find("ul", attrs={"data-testid": "home-features"})

    for obj in objlist.find_all('li'):
        items = obj.text.strip().split(' ')
        if items[:2] == ['Lot', 'Size:']:
            #print(items)
            if items[-1] == 'sqft':
                lotsize = int(items[2].replace(',', ''))
            if items[-1] == 'acres':
                lotsize = int(float(items[2]) * 43560)

    return lotsize


def get_sqft(soup):
    """
    return int
    """

    #     objbox = soup.find('div', attrs={'data-testid':"home-details-summary-medium"})
    #     obj = objbox.find('div', class_="MediaBlock__MediaContent-skmvlj-1 dCsAgE")

    objbox = soup.find(class_="StyledSectionContainer__Container-hjriq0-0 jtfHO")
    objlist = objbox.find_all('div', class_="MediaBlock__MediaContent-skmvlj-1 dCsAgE")

    for obj in objlist:
        text = obj.get_text()
        items = text.strip().split(' ')
        if items[1] == 'sqft':
            sqft = int(items[0].replace(',', ''))

            return sqft


def get_eventMonth(priceHistory):
    mList, mSold = 0, 0
    for row in priceHistory:
        if row[2] == 'Listed For Sale':
            mList = int(row[0][:2])
            break
        elif row[2] == 'Sold':
            mSold = int(row[0][:2])
    return mList, mSold


def get_eventCount(priceHistory):
    # do not count records before 1989

    nList, nPC, nSold = 0, 0, 0
    for row in priceHistory:
        if row[2] == 'Listed For Sale':
            if int(row[0][-4:]) > 1989:
                nList += 1
        elif row[2] == 'Price Change':
            if int(row[0][-4:]) > 1989:
                nPC += 1
        elif row[2] == 'Sold':
            if int(row[0][-4:]) > 1989:
                nSold += 1
    return nList, nPC, nSold


def get_r2m(price, zipcode):
    """
        return %2f, float.
        median is a global variable, a dictionary

    """
    # zipcode bug. a four digit zipcode is missing a '0' as the first digit
    if zipcode[0] == '0':
        zipcode = zipcode[1:]

    mhv = pd.read_csv('./survival_api_data/MedianHomeValue.csv')

    mhv_dict = dict(zip(mhv.zipcode.astype(str), mhv.MedianHomeValue))

    if zipcode in mhv_dict:
        # this should read from a dictionary
        medianHV = mhv_dict[zipcode]  # median house value of this area
    else:
        medianHV = 950000.0

    r2m = round(price / medianHV, 2)

    return r2m

def featPrep(soup):
    """
    return a dictionary. keys are named as dataframe's column name
    """

    street = get_street(soup)

    city = get_city(soup)

    dom = get_dom(soup)

    pH = get_price_history_2(soup)

    price_str, listPrice, date = get_price_from_history(pH)

    cPrice = get_price_from_h3(soup)

    mList, mSold = get_eventMonth(pH)

    nList, nPC, nSold = get_eventCount(pH)

    lotsize = get_lotsize(soup)

    zipcode = get_zipcode(soup)

    sqft = get_sqft(soup)

    address = street + ', ' + city

    if listPrice == 0:
        price = cPrice
        discount = 0
    else:
        price = listPrice
        discount = round((listPrice-cPrice)/listPrice, 2)

    ratio = get_r2m(price, zipcode)

    feat_dict = {
        "address": address,
        "days": dom,        # int
        "discount": discount,  # float %2f
        "listingPrice": price_str,
        "price": price,  # int
        "r2M": ratio,
        "MonthList": mList,
        "MonthSold": mSold,
        "NumList": nList,
        "NumPC": nPC,
        "NumSold": nSold,
        "zipcode": zipcode,
        "sqft": sqft,
        "lotsize": lotsize
    }

    return feat_dict
