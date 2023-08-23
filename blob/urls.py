from django.urls import path
from .views import *


urlpatterns = [
    path('sectors/', get_sectors),
    path('create-session/', create_session),
    path('create/', create_form),
    path('update/<int:id>', update_form),
    path('data/', get_data),
]
