from unicodedata import category
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import CategoryForm


# Create your views here.

def home(request):
    return render(request, 'home.html', {'page_name': 'Home'})
    
def about(request):
  return render(request, 'about.html')

@login_required
def posts_index(request):
  posts = Post.objects.filter(user=request.user)
  return render(request, 'posts/index.html', { 'posts': posts })

@login_required
def posts_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  category_form = CategoryForm()
  return render(request, 'posts/detail.html', {
     'post': post, 'category_form': category_form 
     })

@login_required
def add_category(request, post_id):
    form = CategoryForm(request.POST)

    if form.is_valid():
       new_category = form.save(commit=False)
       new_category.post_id = post_id
       new_category.save()
    return redirect('detail', post_id=post_id)

def signup(request):
    form = UserCreationForm()
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'invalid credentials'
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class PostCreate(LoginRequiredMixin, CreateView):
  model = Post
  fields = ('title', 'location', 'description')
  
  def form_valid(self, form):
    form.instance.user = self.request.user  
    return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = ('title', 'location', 'description')

class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/posts/'
