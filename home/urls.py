from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/$', views.event, name='event_new'),
    path('event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]
