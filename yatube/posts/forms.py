from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text", "group"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "group": forms.Select(attrs={"class": "form-control"})
        }
