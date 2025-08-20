from django import forms

from .models import Comment


class EmailArticleForm(forms.Form):
    name = forms.CharField(max_length=50)
    from_email = forms.EmailField()
    to_email = forms.EmailField()
    message = forms.CharField(required=False, widget=forms.Textarea)
    published = forms.DateTimeField(required=False)


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "content"]
