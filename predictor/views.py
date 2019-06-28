

# Create your views here. example from https://docs.djangoproject.com/en/2.2/intro/tutorial01/
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

from django.http import HttpResponse
import json
import pandas as pd
import numpy as np
from lifelines import CoxPHFitter
from lifelines.utils import median_survival_times, qth_survival_times

from scraper.views import houseScraper
from cleansor.views import featPrep

def predictor(request):
    #url= "https://www.trulia.com/p/nj/short-hills/26-campbell-rd-short-hills-nj-07078--2006164351"
    house_link = request.GET['for_sale']
    print(house_link)
    #house_link = "https://www.trulia.com/p/nj/short-hills/26-campbell-rd-short-hills-nj-07078--2006164351"


    house_info = houseScraper(house_link)
    house_feat = featPrep(house_info)

    # # check if get a validate address:
    # if house_feat[0] is not None:
    #     logflag = True
    #
    # # training model with feat_all
    # if 'address' in feat_all.columns:
    #     feat_all.drop(['address'], axis=1, inplace=True)
    #
    # # fitting model on time
    # cph_time = CoxPHFitter()
    # cph_time.fit(feat_all, duration_col='days', event_col='sold', show_progress=True)
    #
    # # prediction
    # uncon_time = cph_time.predict_survival_function(house_feat)
    #
    # time_pred_50 = median_survival_times(uncon_time)
    # time_pred_75 = qth_survival_times(0.25, uncon_time)
    #
    # # fitting model on discount
    # cph_off = CoxPHFitter()
    # cph_off.fit(feat_all, duration_col='discount', event_col='sold', show_progress=True)
    #
    # # prediction on time
    # uncon_off = cph_off.predict_survival_function(house_feat)
    # # off_life = uncon_off.apply(lambda c: (c / c.loc[feat_all.loc[c.name, 'sold']]).clip_upper(1))
    #
    # off_pred_50 = median_survival_times(uncon_off)
    # off_pred_75 = qth_survival_times(0.25, uncon_off)

    # response_dict = {
    #     #TODO: print out house basic info address, price, days on market
    #     "log": logflag,
    #
    #     "address": house_info[0],
    #     "city": house_info[1],
    #
    #     "curr_price": house_info[2],
    #     "days": house_info[3],
    #
    #     'time_pred_50': time_pred_50,
    #     'time_pred_75': time_pred_75,
    #
    #     'off_pred_50': off_pred_50,
    #     'off_pred_75': off_pred_75,
    # }

    response_dict = {
        #TODO: print out house basic info address, price, days on market
        "log": True,

        "address": "SomeHouseAddress",
        "city": "07029",

        "curr_price": "$1,024,000",
        "days": "10 Weeks",

        'time_pred_50': "no use",
        'time_pred_75': "15 weeks",

        'off_pred_50': "no use 2",
        'off_pred_75': "$999,000",
    }

    response = json.dumps(response_dict)

    return HttpResponse(response)
