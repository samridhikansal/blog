from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm , CategoryForm, CommentsForm, ReplyCommentForm
from .models import PostCategory, Post, Comments
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
# view for the home page 

# posts on the index page with pagination. Only three posts will be displayed on each page 
def index(request, page):
    posts = Post.objects.all().order_by("name")
    paginator = Paginator(posts, per_page=3)
    page_object =paginator.get_page(page)
    users = User.objects.all().values()
    return render( request, "index.html", { "users": users, "page_obj":page_object})

#display posts sorted by categories

def category(request, name):
    try:
        category = PostCategory.objects.get(category = name)
        if category:
          posts = Post.objects.filter(category= category)
          return render(request, "category.html", {"posts": posts, "category": category.category})
    except ObjectDoesNotExist:
        messages.error(request, "there is some error")
        return redirect('index')

#post detail page. The comments form is also on this page. All the prvious comments are also rendered on this page 
def post(request, id):
    post = Post.objects.get(id = id)
    form = CommentsForm()
    reply_form = ReplyCommentForm()
    post_comments = Comments.objects.filter(post_id=id).values() 
    return render(request, "post.html", {"post": post, "form": form, "comments": post_comments, "reply_form": reply_form})

#edit post 
def edit_post(request, id):
    post = Post.objects.get(id=id)
    author = post.author
    form = PostForm(instance=post)
    # categories = PostCategory.objects.all()
    if request.method == "POST":

        form=PostForm(request.POST or None, request.FILES or None)
        if form.is_valid:
              form.save(commit=False)
              cat = request.POST.get('category')
              post.desc = request.POST.get('desc')
              post.name = request.POST.get('name')
              post.image = request.FILES.get("image")
              post.category = PostCategory.objects.get(pk = cat)
              post.author = User.objects.get(username = author)
              post.save()
              messages.success(request, "The post has been edited sucessfully")
              return render(request, "post.html", {"post":post})
        # else:
             # messages.success(request, "you can not edit this post as you are not the author.")
            # return redirect('/posts/1')
    return render(request, "edit_post.html", {"form": form, "id": post.id})

#new comment logic. If the user is authenticated the author will be the authenticated user otherwise it will be automatically taken as guest.
def comments(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = CommentsForm()
    reply_form = ReplyCommentForm()
    post_comments = Comments.objects.filter(post_id=post_id).values() 
    if request.method =="POST":
        comment = CommentsForm(request.POST or None)
        
        if comment.is_valid():
            new_comment = Comments()
            new_comment.comment = comment.cleaned_data['comment']
            if request.user.is_authenticated:
                new_comment.author = request.user.username
            else:
                new_comment.author = "Guest"
            new_comment.post = Post.objects.get(pk=post_id)
            new_comment.save()
            post_comments = Comments.objects.filter(post_id=post_id).values()
            messages.success(request, "Your comment was successfully added!!")
            return render(request, "post.html", { "post":post, "form": form, "comments":post_comments})
    return render(request, "post.html", {"post": post, "form": form, "comments":post_comments, "reply_form": reply_form })

def edit_comments(request, comment_id):
    comment = Comments.objects.get(id=comment_id)
    form = CommentsForm(instance=comment)
    if request.method =="POST":
        edited_comment_form= CommentsForm(request.POST)
        if edited_comment_form.is_valid():
            edited_comment= edited_comment_form.cleaned_data['comment']
            comment.comment= edited_comment
            comment.save()
            user= request.user.username
            url = "/" + user + "/profile"
            messages.success(request, "The comment has been successfully edited")
            return redirect(url)
    
    return render(request, "edit_comments.html",{"form": form, "comment": comment})

def  comments_reply(request, id, post_id):
    post = Post.objects.get(id = post_id)
    comment = Comments.objects.get(pk=id)
    if request.method == "POST":
       comment_reply = ReplyCommentForm(request.POST)
       try:
        if comment_reply.is_valid():
            comment_reply.save(commit=False)
            if request.user.is_authenticated:
                comment_reply.author = User.objects.get(username = request.user.username)
            else:
                comment_reply.author = "Guest"
            comment_reply.comment= comment
            comment_reply.save()
            messages.success(request, "Reply added sucessfully!")
            return render(request ,'post.html',{"post": post } )
       except Exception as e:
         messages.error(request, e)
         return render(request ,'post.html',{"post": post } )

    else:
       return render(request ,'post.html',{"post": post } )
           
           
       

    

# view to help user see his profile that includes all activities that he has done on the website 
def user_profile(request, username):
    if username == "guest":
      messages.success(request, "You are not logged in. Loggin to view your profile")
      return render(request, "login.html")
    else:
      user = User.objects.get(username = username)
      posts = Post.objects.filter(author=user.id)
      comments = Comments.objects.filter(author=user.username)
      return render(request, 'profile.html', {"username": username, "posts": posts, "comments": comments})
     
      

#login user
def login_user(request):
    if request.method =="POST": 
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username= username, password= password)
        if user is not None:
            login( request, user)
            messages.success(request, "You are logged in now")
            return render( request, "index.html", {"user": user})
        else:
            return render( request, "login.html", {"error": "there is an error"})
    return render( request, "login.html")

#logout user
def logout_user(request):
    logout(request)
    messages.success(request,"You have successfully loged out")
    return render( request, "index.html")

#register a user. 
# If there is any form validation error the template will show an error message. 
# This includes an already existing user trying to register again
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid:
            try:
                user = form.save()
                login(request,user)
                messages.success(request, "You have sucessfully register. You are logged in now. You can press logout if you dont wish to cont.")
                return render( request, "index.html", {"user":user})
            except Exception as e :
                messages.error(request, e)
                errors = form.errors
                return render(request, "register.html",{"errors":errors} )
        else:
            error = form.errors()
            return render(request, "register.html", {"error": error})
    return render(request, "register.html")

#add a post. Login is required to add a post 
@login_required
def add_post(request):
    current_user = request.user.username
    user = User.objects.get(username = current_user)

    form = PostForm()
    categories = PostCategory.objects.all().values()
    if request.method == "POST":
      form = PostForm(request.POST or None, request.FILES or None) 
      if form.is_valid():
        mypost = form.save(commit=False)
        mypost.author = User.objects.get(username = request.user)
        cat = request.POST.get("category")
        mypost.category = PostCategory.objects.get(pk = cat)
        mypost.save() 
        posts = Post.objects.filter(author=user.id)
        comments = Comments.objects.filter(author=user.username)
        messages.success(request, "Your post has been successfully added!!")    
        return render(request, "profile.html", {"user": user, "posts":posts, "comments":comments})
   
    

    return render(request, "add.html", {"form": form, "categories": categories})
