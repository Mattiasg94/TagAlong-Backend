
from website import views
from django.urls import path, include
from website import api


urlpatterns = [
    path(r'', views.events, name='events'),
    path(r'new-event', views.new_event, name='new_event'),

    path(r'api/event/<str:pk>/', api.EventsById.as_view()),
    path(r'api/event/<str:pk>/<str:action>/', api.EventsById.as_view()),
    path(r'api/event/<str:pk>/<str:action>/<str:target>/',
         api.EventsById.as_view()),

    path(r'api/events/', api.EventsList.as_view()),
    path(r'api/events/<str:pk>/', api.EventsList.as_view()),
    path(r'api/templates/<str:pk>/', api.TemplateEventsList.as_view()),
    path(r'api/template/<str:pk>/', api.TemplateById.as_view()),

]
