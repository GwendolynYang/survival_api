from django.apps import AppConfig
import pandas as pd

class CleansorConfig(AppConfig):
    name = 'cleansor'


    def ready(self):

        global mhv_dict

        mhv = pd.read_csv('../../survival_api_data/MedianHomeValue.csv')

        mhv_dict = dict(zip(mhv.zipcode.astype(str), mhv.MedianHomeValue))