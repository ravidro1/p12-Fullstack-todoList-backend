from django.urls import path
from list_api.views.user_views import SignUp,Login, GetUser,RefreshToken, Logout


urlpatterns = [
    path("signup", SignUp.as_view()),
    path("login", Login.as_view()),
    path("getuser", GetUser.as_view()),
    path("refresh-token", RefreshToken.as_view()),
    path("logout", Logout.as_view()),

]
