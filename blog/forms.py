from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Join the discussion and leave a comment!',
                'rows': 3,
                }),
        }