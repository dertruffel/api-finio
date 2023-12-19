from django.urls import path, include

from api.views import CalculatorPay, Articles
from config import settings



urlpatterns = [

    path('calculator_pay/', CalculatorPay.as_view(), name='calculator_pay'),
    path('articles/', Articles.as_view(), name='articles'),




]
