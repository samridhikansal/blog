from .models import Post, PostCategory, Comments
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