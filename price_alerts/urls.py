from django.urls import path
from .views import AlertCreateView, AlertDeleteView, AlertListView

urlpatterns = [
    path('create/', AlertCreateView.as_view(), name='alert_create'),
    path('delete/<int:pk>/', AlertDeleteView.as_view(), name='alert_delete'),
    path('list/', AlertListView.as_view(), name='alert_list'),
]