from .models import PostCategory, Post
from .forms  import CommentsForm, ReplyCommentForm
from .page import Page
def categories(request):
    categories = PostCategory.objects.all().values()
    posts = Post.objects.all().order_by("name")
    return {"categories": categories, "posts": posts}

def all_forms(request):
    comments_form=CommentsForm()
    reply_form = ReplyCommentForm()
    return {"comments_form": comments_form, "reply_form": reply_form}

def page_obj(request):
    return {page_obj:Page(request)}