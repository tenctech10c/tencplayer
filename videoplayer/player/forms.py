from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post
from pagedown.settings import SHOW_PREVIEW

class PostForm(forms.ModelForm):
    content =  forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(
            widget=forms.TextInput(
                attrs={'type': 'date'}
            ), required=False
        )
    class Meta:
        model = Post
        fields = [
                "title",
                "content",
                "video_url",
                "image_url",
                "publish"
            ]
    