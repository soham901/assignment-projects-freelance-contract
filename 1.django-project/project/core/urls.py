from .views import home, get_datapoints_test, get_datapoints, test_data, real_data

from django.urls import path



urlpatterns = [
    path('', home, name='home'),
    path('real-data/', real_data, name='real-data'),
    path('test-data/', test_data, name='test-data'),
    path('get_datapoints/', get_datapoints, name='get_datapoints'),
    path('get_datapoints_test/', get_datapoints_test, name='get_datapoints_test'),
]