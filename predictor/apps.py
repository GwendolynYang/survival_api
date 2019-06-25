from django.apps import AppConfig
import pandas as pd

class PredictorConfig(AppConfig):
    name = 'predictor'

    def ready(self):

        global feat_all

        feat_all = pd.read_csv('../../survival_api_data/feat_all.csv')