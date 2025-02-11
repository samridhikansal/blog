from django.urls import path
from . import views

urlpatterns = [
    path('posts/<int:page>', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('add', views.add_post , name= 'add'),
    path('<str:username>/profile', views.user_profile, name = 'profile'),
    path('post/<int:id>', views.post, name = 'post'),
    path('post/comments/<int:post_id>', views.comments, name = 'comments'),
    path('post/<int:post_id>/comments/reply/<int:id>', views.comments_reply, name = 'comments_reply'),
    path('post/comments/edit/<int:comment_id>', views.edit_comments, name = 'edit_comments'),
    path('post/edit/<int:id>', views.edit_post, name = 'edit_post'),
    path('category/<str:name>', views.category, name = "category"),




    
    

    # path('<int:post_id>/', views.detail, name='detail'),
]