from .models import PostCategory, Post
def categories(request):
    categories = PostCategory.objects.all().values()
    posts = Post.objects.all().order_by("name")
    return {"categories": categories, "posts": posts}