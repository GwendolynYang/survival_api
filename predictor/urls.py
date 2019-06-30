from django.urls import path

from . import views
from django.conf.urls import url
from predictor.views import predictor

urlpatterns = [
    url(' ', predictor, name='weblink'),
]