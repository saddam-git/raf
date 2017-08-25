from django.shortcuts import render
from django.core.urlresolvers import reverse,reverse_lazy
from django.views.generic import ListView, View, CreateView,DeleteView,UpdateView,DetailView
from tag.models import Tag
from tag.forms import TagForm
from django.contrib.messages.views import SuccessMessageMixin
from .utils import PageMixin
################################### Permission #######################
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from .decorators import (require_authenticated_permission, class_login_required,)


# Create your views here.


class TagList(ListView):
    paginate_by = 2
    model = Tag

@require_authenticated_permission('tag.add_tag')
class TagCreate(SuccessMessageMixin, CreateView):
    form_class = TagForm
    model = Tag

    success_url = reverse_lazy('tag_list_view')
    success_message = 'Another tag is created!!!!'





#@require_authenticated_permission('tag.view_tag')
class TagDetail(DetailView):
    model = Tag

@require_authenticated_permission('tag.delete_tag')
class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('tag_list_view')

@require_authenticated_permission('tag.change_tag')
class TagUpdate(SuccessMessageMixin,UpdateView):
    model = Tag
    fields = '__all__'
    template_name_suffix = '_form_update'
    success_url = reverse_lazy('tag_list_view')
    success_message = 'Successfully Updated!!!!'






