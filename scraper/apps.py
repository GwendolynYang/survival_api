from django.apps import AppConfig
import pandas as pd

class ScraperConfig(AppConfig):
    name = 'scraper'

    def ready(self):

        global median

        mhv = pd.read_csv('../../survival_api_data/MedianHomeValue.csv')

        median = dict(zip(mhv.zipcode.astype(str), mhv.MedianHomeValue))