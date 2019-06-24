from django.http import HttpResponse

# Create your views here. example from https://docs.djangoproject.com/en/2.2/intro/tutorial01/
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


import pandas as pd
import numpy as np

from lifelines import CoxPHFitter
from lifelines.utils import median_survival_times, qth_survival_times

def predictor(request):