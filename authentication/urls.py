from django.urls import path
from . import views 

urlpatterns = [
    path("signup/",views.signup, name="signup"),
    path("signin/",views.handleSignIn, name="handleSignIn"),
    path("signout/",views.handleSignOut, name="handleSignOut"),
    path("activate/<uidb64>/<token>",views.ActivateAccountView.as_view(), name="activate")
]