from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
        labels = {
            'name': '',  # Do not display a label for the name field
            'text': '',  # Do not display a label for the text field
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'text': forms.Textarea(attrs={'placeholder': 'Leave a comment!'}),
        }