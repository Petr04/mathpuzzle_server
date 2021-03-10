from django.urls import path, re_path, include

from .views import RegistrationAPIView, LoginAPIView, \
    UserDataAPIView, IsRegistered

urlpatterns = [
    re_path(r'^registration/?$', RegistrationAPIView.as_view(),
        name='user_registration'),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
    path('data/<str:username>/', UserDataAPIView.as_view(), name='user_data'),
    path('is_registered/', IsRegistered.as_view(), name="is_registered"),
]
