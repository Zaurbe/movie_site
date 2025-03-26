# movies/forms.py
from django import forms
from .models import FilmRating, Review, Comment

class RatingForm(forms.Form):
    rating = forms.DecimalField(max_digits=3, decimal_places=1, min_value=1.0, max_value=10.0, label="Ваша оценка")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
        }
        labels = {
            'content': 'Рецензия',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        }
        labels = {
            'content': 'Комментарий',
        }
