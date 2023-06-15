from django.urls import path
from .views import EventDetailView

app_name = "events"
urlpatterns = [
    path(
        route='event/<str:slug>/',
        view=EventDetailView.as_view(),
        name='event_details'
    ),

]
