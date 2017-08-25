from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.


class Tag(models.Model):
    tag_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=50, unique=True,help_text='a label for url')

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return reverse('tag_detail',kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('tag_delete',kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('tag_update',kwargs={'slug':self.slug})
