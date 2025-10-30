from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts"""

    class Meta:
        model = Post
        fields = ["title", "category", "content", "excerpt", "featured_image", "status"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter post title"}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Write your post content here...",
                }
            ),
            "excerpt": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Brief description of your post (optional)",
                }
            ),
            "featured_image": forms.FileInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments to posts"""

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your comment here...",
                }
            ),
        }
        labels = {"content": "Your Comment"}
