from django.urls import path, include
from .views import HelloAPI, RegistrationAPI, KakaoLoginAPI, LoginAPI, UserAPI

urlpatterns = [
    path("hello/", HelloAPI),
    path("auth/register/", RegistrationAPI.as_view()),
    path("auth/login/", LoginAPI.as_view()),
    path("auth/kakaoLogin/", KakaoLoginAPI.as_view()),
    path("auth/user/", UserAPI.as_view()),
]
