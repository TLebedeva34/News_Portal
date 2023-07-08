from django import forms
from django.core.exceptions import ValidationError

from .models import Article


class ArticleForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Article
        fields = [
            'author',
            'category',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Текст статьи не должен совпадать с заголовком."
            )
        return cleaned_data

