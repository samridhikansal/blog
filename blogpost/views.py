from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm , CategoryForm, CommentsForm, ReplyCommentForm, AuthorForm
from .models import PostCategory, Post, Comments,  Post_like_dislike, Author, Follow, Comments_reply
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
    return render( request, "index.html", {"users": users, "page_obj":page_object})

#display posts sorted by categories

def category(request,name):
    try:
        category = PostCategory.objects.get(category = name)
        if category:
          posts = Post.objects.filter(category= category)
          return render(request, "category.html", {"posts": posts, "category": category.category})
    except PostCategory.DoesNotExist:
        messages.error(request, "There is no such category in the system. Contact admin to add a new category")
        return redirect('contact')

#post detail page. The comments form is also on this page. All the prvious comments are also rendered on this page 
def post(request,id):
    try:
        post = Post.objects.get(id=id)
        form = CommentsForm()
        reply_form = ReplyCommentForm()
        post_comments = Comments.objects.filter(post_id=id).values() 
        user=request.user
        try:
            post_like_dislike = Post_like_dislike.objects.get(author=user,post_id=id)
            return render(request, "post.html", {"post": post, "form": form, "comments": post_comments, "reply_form": reply_form, "post_like_dislike":post_like_dislike})
        except Post_like_dislike.DoesNotExist:
            return render(request, "post.html", {"post": post, "form": form, "comments": post_comments, "reply_form": reply_form})
        
    except Post.DoesNotExist:
        messages.error(request, "No such post exist on the website")
        return redirect('index',page=1)

#total likes and dislikes on the post. on the authentic user can like or dislike a post.
#if a user is not authentic, the view will send them to the login template 
# if the entry of the post in the like and dislike aolumn already exist then the entry will be updates. 
# else a new entry will be created in the model Total_likes_dislikes
def total_likes(request,id):
    post = Post.objects.get(id=id)
    user = request.user
    if user.is_authenticated:
        try:
            post_like_dislike = Post_like_dislike.objects.get(author=user, post_id=id)
            post_like_dislike.like = "True"
            post_like_dislike.dislike="False"
            post_like_dislike.save()
            post.total_likes = post.total_likes+1
            post.total_dislikes=post.total_dislikes-1
            post.save()
            messages.success(request, "Thanks for changing the liking the comment")
            return redirect( "post", post=post, post_like_dislike=post_like_dislike)
        except Post_like_dislike.DoesNotExist:
            post.total_likes= post.total_likes+1
            post.save()
            post_like_dislike=Post_like_dislike()
            post_like_dislike.post =post
            post_like_dislike.author=user
            post_like_dislike.like="True"
            post_like_dislike.dislike="False"
            post_like_dislike.save()
            total_likes = post.total_likes
            messages.success(request, "Thanks for liking the comment")
            return redirect("post", post=post, post_like_dislike=post_like_dislike)
    return redirect("post", post=post)
      
       
    
# else a new entry will be created in the model Total_likes_dislikes
def total_dislikes(request,id):
    post = Post.objects.get(id=id)
    user = request.user
    if user.is_authenticated:
         try:
            post_like_dislike = Post_like_dislike.objects.get(author=user, post_id=id)
            post_like_dislike.dislike = "True"
            post_like_dislike.like="False"
            post_like_dislike.save()
            post.total_dislikes = post.total_dislikes+1
            post.total_likes=post.total_likes-1
            post.save()
            messages.success(request, "Thanks for changing the dislike to like for the comment")
            return redirect( "post", post = post, post_like_dislike = post_like_dislike)
         except Post_like_dislike.DoesNotExist:
            post.total_dislikes= post.total_dislikes+1
            post.save()
            post_like_dislike=Post_like_dislike()
            post_like_dislike.post=post
            post_like_dislike.author=user
            post_like_dislike.dislike="True"
            post_like_dislike.like="False"
            post_like_dislike.save()
            total_likes = post.total_likes
            messages.success(request, "Thanks for liking the comment")
            return redirect("post", post = post, total_likes = total_likes, post_like_dislike = post_like_dislike)
    else:
        messages.error(request, "Please Login/register to like or dislike a comment")
        return render(request, "login.html")
  
      
          
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
    if request.method =="POST":
        comment = CommentsForm(request.POST or None)
        if comment.is_valid():
            comment.save(commit= False)
            if request.user.is_authenticated:
                comment.author = request.user.username
            else:
                comment.author = "Guest"
            comment.post = Post.objects.get(pk=post_id)
            comment.save()
            post_comments = Comments.objects.filter(post_id=post_id).values()
            messages.success(request, "Your comment was successfully added!!")
            return redirect("post", id=post_id)
    return redirect("post",id=post_id)

def edit_comments(request,post_id,comment_id):
    comment = Comments.objects.get(id=comment_id)
    username= comment.author
    form = CommentsForm(instance=comment)
    if request.method =="POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment.comment = form.cleaned_data['comment']
            comment.save(update_fields=["comment"])
            messages.success(request, "The comment has been successfully edited")
            return redirect('profile', username=username)
    
    return render(request, "edit_comments.html",{"form": form, "comment": comment})

def comments_reply(request, id, post_id):
    post = Post.objects.get(id = post_id)
    comment = Comments.objects.get(id=id)
    if request.method == "POST":
       form = ReplyCommentForm(request.POST)
       if request.user.is_authenticated:
           if form.is_valid():
              comments_reply= Comments_reply()
              comments_reply.reply= form.cleaned_data["reply"]
              comments_reply.author = User.objects.get(username = request.user.username)
              comments_reply.comment= Comments.objects.get(id=id)
              comments_reply.save()
              messages.success(request, "Thanks for the reply")
              return redirect("post", id=post_id)
       else:     
            messages.error(request, "Please login to reply")
            return redirect("post", id=post_id) 
    else:
        messages.success(request, f"comment id is {comment.id}")
        return render(request ,'post.html',{"post": post } )
           
           
       

    

# view to help user see his profile that includes all activities that he has done on the website 
def user_profile(request, username):
    try:
         user = request.user
         if user.is_authenticated:
            profile_owner = User.objects.get(username=username)
            posts = Post.objects.filter(author=profile_owner.id)
            followers = Follow.objects.filter(author=profile_owner.id)
            comments = Comments.objects.filter(author=profile_owner.username)
            no_of_followers = followers.count()
            follows = Follow.objects.filter(follower=profile_owner.username)
            no_follows = follows.count( )
            posts_no = posts.count()
            try:
                author_user = Author.objects.get(user=profile_owner)
                author_user.total_followers=no_of_followers
                author_user.total_follows=no_follows
                author_user.total_posts=posts_no
                if posts_no==0:
                    author_user.category="reader"
                else:
                    author_user.category="author"
                author_user.save(update_fields=["total_followers", "total_follows", "total_posts", "category"])
            except Author.DoesNotExist:
                author_user = Author()
                author_user.total_followers=no_of_followers
                author_user.total_follows=no_follows
                author_user.user= User.objects.get(username=username)
                author_user.total_posts=posts_no
                if posts_no==0:
                    author_user.category="reader"
                else:
                    author_user.category="author"
                author_user.save()           
            author_user = Author.objects.get(user=profile_owner)
            like_dislike_posts = Post_like_dislike.objects.filter(author=profile_owner.username)
           
            return render(request, 'profile.html', { "posts": posts,\
                                                     "comments": comments, \
                                                     "like_dislike_posts":like_dislike_posts, \
                                                     "followers":followers, \
                                                      "follows":follows, \
                                                      "author":author_user })
         else:
          messages.success(request, "You are not logged in. Loggin to view the profile")
          return render(request, "login.html")
    except User.DoesNotExist:
        messages.error(request, "No such user exist. Please register to create a profile")
        return redirect("register")
    
def follow(request, username,id):
        reader = request.user
        
        user = User.objects.get(username=username)
        follower=reader
        try:
            follow = Follow.objects.get(author=user.id, follower=follower)
            if follow.status==True:
                follow.status==False
                follow.save()
                messages.success(request, "You have unfollowed the author")
                return redirect('post', id=id) 
            else:
                follow.status==False
                follow.save()
                messages.success(request, "You have unfollowed the author")
                return redirect('post', id=id)
        except Follow.DoesNotExist:
            follow = Follow()
            follow.author=user
            follow.follower=follower
            follow.status= True
            follow.save()
            messages.success(request, f"You are following{user} now")
            return redirect('post', id=id)
        
#login user
def login_user(request):
    if request.method =="POST": 
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username= username, password= password)
        if user is not None:
            login( request, user)
            messages.success(request, "You are logged in now")
            return redirect("index", page=1)
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
    author_form= AuthorForm()
    form=UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        
        if form.is_valid:
            try:
                user = form.save()
                newly_created =user.username
                author = Author()
                author.category= request.POST.get("category")
                author.image=request.FILES.get("image")
                author.user = User.objects.get(username=newly_created)
                author.save()
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
    return render(request, "register.html", {"author_form":author_form,"form":form })

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
