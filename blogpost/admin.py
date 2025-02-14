from django.contrib import admin
from .models import Post, PostCategory, Comments, Comments_reply, Post_like_dislike, Author, Follow, About

# Register your models here.

admin.site.register( Post)
admin.site.register(PostCategory)
admin.site.register(Comments)
admin.site.register(Comments_reply)
admin.site.register(Post_like_dislike)
admin.site.register(Author)
admin.site.register(Follow)
admin.site.register(About)


