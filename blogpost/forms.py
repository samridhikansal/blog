from .models import Post, PostCategory, Comments, Comments_reply, Author
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("name", "desc","image")
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = PostCategory
        fields = ( "category",)   

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ("comment",) 

class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comments_reply
        fields = ("reply",)

class AuthorForm(forms.ModelForm):
    class Meta:
        model=Author
        fields =("category", "image")