
from django.urls import path
from . import views

app_name='login'
urlpatterns = [
    path('',views.home,name='home'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('signup/store_details/',views.store_details,name='store_details'),
    path('signin/check_signin/',views.check_signin,name='check_signin'),
    path('signin/check_signin/',views.logout,name='logout'),
]
