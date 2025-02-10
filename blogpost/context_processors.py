from .models import PostCategory
def categories(request):
    categories = PostCategory.objects.all().values()
    return {"categories": categories}