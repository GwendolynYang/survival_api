

# Create your views here. example from https://docs.djangoproject.com/en/2.2/intro/tutorial01/
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

from django.http import HttpResponse
import json
import math
import pandas as pd
import numpy as np
from lifelines import CoxPHFitter
from lifelines.utils import median_survival_times, qth_survival_times

from scraper.views import houseScraper
from cleansor.views import featPrep

def predictor(request):
    #url = "https://www.trulia.com/p/nj/short-hills/26-campbell-rd-short-hills-nj-07078--2006164351"
    house_link = request.GET['weblink']
    #print(house_link)

    #house_link = "https://www.trulia.com/p/nj/short-hills/26-campbell-rd-short-hills-nj-07078--2006164351"
    #
    print(house_link)
    feat = houseScraper(house_link)


    # house_feat = featPrep(house_info)
    #
    # # check if get a validate address:
    # if house_feat[0] is not None:
    #     logflag = True

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



    dom_w = math.ceil(feat['days']/7)
    response_dict = {
        #TODO: print out house basic info address, price, days on market
        "log": True,

        "prediction":
            {
                "address": feat['address'],

                "dom": dom_w,

        'time_pred_50': "no use",
        'days': "15 weeks",

        'off_pred_50': "no use 2",
        'off_pred_75': "$999,000",

         "off_usd": "$999,000",
         "off_pct" : "13%"
         }
    }

    response = json.dumps(response_dict)

    return HttpResponse(response)
