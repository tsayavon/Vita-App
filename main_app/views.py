from unicodedata import category
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post
from .forms import CategoryForm


# Create your views here.

def home(request):
    return render(request, 'home.html', {'page_name': 'Home'})
    
def about(request):
  return render(request, 'about.html')

def posts_index(request):
  posts = Post.objects.all()
  return render(request, 'posts/index.html', { 'posts': posts })

def posts_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  category_form = CategoryForm()
  return render(request, 'posts/detail.html', {
     'post': post, 'category_form': category_form 
     })

def add_category(request, post_id):
    form = CategoryForm(request.POST)

    if form.is_valid():
       new_category = form.save(commit=False)
       new_category.post_id = post_id
       new_category.save()
    return redirect('detail', post_id=post_id)

class PostCreate(CreateView):
  model = Post
  fields = ('title', 'location', 'description')
  success_url = '/posts/'

class PostUpdate(UpdateView):
  model = Post
  fields = ('title', 'location', 'description')

class PostDelete(DeleteView):
  model = Post
  success_url = '/posts/'
