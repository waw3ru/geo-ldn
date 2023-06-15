# Core Django imports.
from django.urls import path
from .views import ToolDetailView

app_name = "core"
urlpatterns = [
    path(
        route='<str:slug>/',
        view=ToolDetailView.as_view(),
        name='tool_detail'
    ),
]
