# price_alert/urls.py

from django.contrib import admin
from django.urls import path
from price_alerts.views import home, AlertCreateView, AlertListView, TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from price_alerts.views import AlertDeleteView

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('alerts/create/', AlertCreateView.as_view(), name='alert_create'),
    path('alerts/delete/', AlertDeleteView.as_view(), name='alert_delete'),  # Add this line
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]