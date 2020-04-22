from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("signin", views.signIn, name="signin"),
    path("postsign", views.postsign, name="Logged"),
    path("logout", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("create", views.createClip, name="clip"),   

]