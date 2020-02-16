from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:campaign_id>/', views.campaign, name='campaign'),
    path('new/', views.new_campaign, name='new_campaign'),
]


