from django.apps import AppConfig
import pandas as pd


class PredictorConfig(AppConfig):
    name = 'predictor'

    def ready(self):

        global feat_sold

        feat_sold = []

        feat_sold = pd.read_csv('./survival_api_data/feat_sold_1.csv')
