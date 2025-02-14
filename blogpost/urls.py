from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("about",views.about, name="about"),
    path('posts/<int:page>', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('add', views.add_post , name= 'add'),
    path('<str:username>/profile', views.user_profile, name = 'profile'),
    path('follow/<int:id>/<str:username>', views.follow, name = 'follow'),
    path('post/<int:id>', views.post, name = 'post'),
    path("post/like/<int:id>", views.total_likes, name = "total_likes"),
    path("post/dislike/<int:id>", views.total_dislikes, name = "total_dislikes"),
    path('post/comments/<int:post_id>', views.comments, name = 'comments'),
    path('post/<int:post_id>/comments/reply/<int:id>', views.comments_reply, name = 'comments_reply'),
    path('post/comments/<int:post_id>/edit/<int:comment_id>', views.edit_comments, name = 'edit_comments'),
    path('post/edit/<int:id>', views.edit_post, name = 'edit_post'),
    path('category/<str:name>', views.category, name = "category"),




    
    

    # path('<int:post_id>/', views.detail, name='detail'),
]