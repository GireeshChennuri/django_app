from django.urls import path
from . import views
app_name='hacker_news'
urlpatterns=[
   path('',views.home,name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('newest/',views.new_posts,name='newest'),
     path('past/', views.past_posts, name='past'),
     path('submit_view/',views.submit_view,name='submit_view'),
     path('handle_vote/<int:post_id>/<str:vote_type>/',views.handle_vote,name='handle_vote'),
     path('comment/<int:post_id>/',views.comment_view,name='comment')

]

