from django.shortcuts import render

# Create your views here.

def featPrep(houseraw):

    # TODO: now just basic raw to features, may need more features

    price = houseraw[2]
    price = int(price.replace(',', '').replace('$', ''))

    days = houseraw[3]


