from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.contrib.auth.models import User
from .models import Post

class Page():
    def __init__(self, request):
        self.session = request.session
        page =self.session.get("page")
        test_posts = self.session.get("test_posts")
        if "page" not in request.session:
         page= self.session['page'] =1 
        self.page =page
        if "test_posts" not in request.session:
           test_posts = self.session["test_post"]=[]
        self.test_posts = test_posts
        
    def my_pagination(request,page):
       posts = Post.objects.all().order_by("name")
       paginator = Paginator(posts, per_page=3)
       page_object =paginator.get_page(page)
       return  {"page_obj":page_object}

       
    # def __len__(self):
        # return(len(self.cart))