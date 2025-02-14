from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.contrib.auth.models import User
from .models import Post

class Page():
    def __init__(self, request):
        self.session = request.session
        page = self.session.get('session_key')
    
        if 'session_key' not in request.session:
            page = self.session['session_key'] = 1
            # to make sure the cart works on every page of the website. we need to initialize self.cart to cart
        self.page = page
        self.posts

    def paginator(self, page):
        posts = Post.objects.all().order_by("name")
        paginator = Paginator(posts, per_page=2)
        page_object =paginator.get_page(page)
        return page_object
       
    # def __len__(self):
        # return(len(self.cart))