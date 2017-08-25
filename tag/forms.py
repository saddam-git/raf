from django import  forms
from .models import Tag
from django.core.exceptions import ValidationError

class SlugCleanMixin:
    def clean_slug(self):
        new_slug = (self.cleaned_data['slug'].lower())
        if new_slug=='create':
            raise ValidationError('Slug may not be create ')
        return new_slug



class TagForm(forms.ModelForm):
    class Meta:
        model  = Tag
        fields = '__all__'

    def clean_tag_name(self):
        return (self.cleaned_data['tag_name'].lower())

    def clean_slug(self):
        return self.cleaned_data['slug'].lower()

