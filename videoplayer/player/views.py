from django.shortcuts import render
from .forms import PostForm
from django.contrib import messages
from markdown_deux import markdown
from django.utils import timezone
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

# Create your views here.
def posts_create(request): 
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, "Successfully created")
    
    context = {
            "form": form,
        }
    return render(request, 'post_form.html', context)

def posts_list(request):
    today = timezone.now().date()
    
    queryset_list = Post.objects.all().order_by("publish")
    
    query  = request.GET.get("query")
    if query:
        queryset_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)       
            ).distinct()
    
    paginator = Paginator(queryset_list, 3) 
    
    page_request_var = 'page'
    
    page = request.GET.get(page_request_var)
    
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
        
    context = {
            "object_list": queryset,
            "title": "List",
            "page_request_var": page_request_var,
            "today": today,
        }
    return render(request, 'post_list.html', context)