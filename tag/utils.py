from .models import Tag
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import render


class PageMixin:
    def get(self,request):
        tags = Tag.objects.all()
        paginator = Paginator(tags,2)

        page = request.GET.get('page')

        try:
            tag_list = paginator.page(page)
        except PageNotAnInteger:
            tag_list = paginator.page(1)
        except EmptyPage:
            tag_list = paginator.page(paginator.num_pages)

        return render(request,'tag/tag_list.html',{'tag_list':tag_list})

