from django.http import HttpResponse
import json
import math
import pandas as pd
import pickle

import numpy as np
from lifelines import CoxPHFitter
from lifelines.utils import qth_survival_times

from scraper.views import houseScraper
#from predictor.apps import feat_sold


def get_time_model(censor, feat_train):
    """
    :param censor: int, choose which model to use, based on DOM.
    :return: model
    """
    data = feat_train.copy()

    if censor > 18:
        ndays = 540
    else:
        ndays = censor * 30

    #data.loc[(data.days > 540), 'sold'] = 0

    cph = pickle.load(open("./survival_api_data/cph1.pickle", "rb"))
    cph.fit(data, duration_col='days', event_col='sold')

    return cph


def get_off_model(censor, feat_train):
    """
    :param censor: int, choose which model to use, based on DOM.
    :return: model
    """
    data = feat_train.copy()
    data.loc[(data.discount > 50), 'sold'] = 0

    cph = pickle.load(open("./survival_api_data/cph2.pickle", "rb"))
    cph.fit(data, duration_col='discount', event_col='sold')

    return cph


def predictor(request):

    house_link = request.GET['weblink']

    print(request.GET['weblink'])


    # get training data
    feat = pd.read_csv('./survival_api_data/feat.csv')

    house_all = houseScraper(house_link)

    house_feat = [0]
    house_feat.append(house_all['days'])
    house_feat.append(house_all['discount'])
    house_feat.append(house_all['price'])
    house_feat.append(house_all['r2M'])
    house_feat.append(house_all['MonthList'])
    house_feat.append(house_all['MonthSold'])
    house_feat.append(house_all['NumList'])
    house_feat.append(house_all['NumPC'])
    house_feat.append(house_all['NumSold'])

    col_name = ['sold', 'days', 'discount', 'price', 'r2M', 'MonthList', 'MonthSold', 'NumList', 'NumPC', 'NumSold']

    feat_df = pd.DataFrame([house_feat], columns=col_name)

    feat_all = pd.concat([feat, feat_df], ignore_index=True)

    censor = house_all['days']//30 + 3
    cph_time = get_time_model(censor, feat_all)
    pred_time_0 = cph_time.predict_survival_function(feat_df)
    pred_time = pred_time_0.apply(lambda c: (c / c.loc[feat_all.loc[c.name, 'days']]).clip_upper(1))
    pred_time_75 = qth_survival_times(0.25, pred_time)
    pred_time_50 = qth_survival_times(0.5, pred_time)

    pred_week = int((pred_time_50 - house_all['days'])//7)

    cph_off = get_off_model(5, feat_all)
    pred_off_0 = cph_off.predict_survival_function(feat_df)
    pred_off = pred_off_0.apply(lambda c: (c / c.loc[feat_all.loc[c.name, 'discount']]).clip_upper(1))
    pred_off_75 = qth_survival_times(0.25, pred_off)
    pred_off_50 = qth_survival_times(0.5, pred_off)

    if pred_off_75 != float("inf"):
        off = pred_off_75
    elif pred_off_50 != float("inf"):
        off = pred_off_50

    else:
        off = 0

    off_str = "{:.1f}%".format(off)
    off = round(off / 100, 1)
    off_usd = int(round((1-off) * house_all['price']))
    off_usd_str = '$' + format(off_usd, ',')

    dom_w = int(math.ceil(house_all['days']/7))
    dom_w_str = str(dom_w) + ' weeks'
    pred_week_str = str(pred_week) + ' weeks'

    response_dict = {
        "log": True,
        # "pred_time_75": pred_time_75,
        # "pred_off_75": pred_off_75,
        # "pred_off_50": pred_off_50,

        "prediction":
            {
                "address": house_all['address'],

                "listing_price": house_all['listingPrice'],

                "dom": dom_w_str,

                "pred_weeks": pred_week_str,

                "off_usd": off_usd_str,

                "off_pct": off_str
            }
    }

    response = json.dumps(response_dict)

    return HttpResponse(response)
