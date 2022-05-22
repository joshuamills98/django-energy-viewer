from datetime import datetime

from django.urls import path, register_converter
from . import views


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z'

    def to_python(self, value):
        # try:
        return_value = value
        # except ValueError:
        #     return_value = datetime.strptime(value, "%Y-%m-%d")
        #     return_value.replace(hour=12, minute=59)

        return return_value

    def to_url(self, value):
        return value


register_converter(DateConverter, 'dateconverter')

app_name = 'generation'
urlpatterns = [
    path('', views.index, name='index'),
    path('current/', views.current, name='current'),
    path('<dateconverter:start_date>/<dateconverter:end_date>/', views.daterange, name='daterange'),
    path('test/', views.daterangefromform, name='daterangefromform')
]
