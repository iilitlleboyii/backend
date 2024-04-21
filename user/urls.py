from django.urls import path
from user.views import LoginView, RegisterView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth'),
    path('register/', RegisterView.as_view(), name='auth'),
    path('refresh/', TokenRefreshView.as_view(), name='auth'),
    path('verify/', TokenVerifyView.as_view(), name='auth'),
    path('current/', UserProfileView.as_view(), name='auth')
]