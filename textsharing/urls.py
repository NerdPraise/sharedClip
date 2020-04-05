from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.signIn, name="login"),
    path("postsign", views.postsign, name="Logged"),
    path("logout", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("create", views.createClip, name="clip"),   

]