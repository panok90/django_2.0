from django.urls import path

from .views import UserLoginView, UserRegistrationView, UserLogoutView, profile
#from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<str:activation_key>/', UserRegistrationView.verify, name='verify'),
]
