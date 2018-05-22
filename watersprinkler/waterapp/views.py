from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.views.generic import ListView
from .models import Post, Comment, Post1, Comment1, Post2, Comment2
from .forms import PostForm, CommentForm, CreateUserForm, Post1Form, Comment1Form, Post2Form, Comment2Form


def index(request):
	return render(request, 'waterapp/index.html')


def about(request):
	return render(request, 'waterapp/about.html')


def contact(request):
	return render(request, 'waterapp/contact.html')


def portfolio(request):
	return render(request, 'waterapp/portfolio.html')


def services(request):
	return render(request, 'waterapp/services.html')


def introduce(request):
	return render(request, 'waterapp/introduce.html')


def post(request):
	return render(request, 'waterapp/post.html')


def loginpage(request):
	return render(request, 'waterapp/loginpage.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'waterapp/index.html')
    else:
        form = UserCreationForm()
    return render(request, 'waterapp/signup.html', {'form': form})


def blacklist(request):
	return render(request, 'waterapp/blacklist.html')

class postLV(ListView):
	model = Post
	template_name = 'waterapp/post_list.html'
	paginate_by = 7

	def get_queryset(self):
		qs = Post.objects.all()
		q = self.request.GET.get('q', '') # GET request의 get 인자중에 q 가 있으면 가져오고, 없으면 빈 문자열

		if q:
			qs = qs.filter(title__icontains=q)

		return qs


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        if request.user.id == None:
            return redirect('login')
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('waterapp:post_detail', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'waterapp/post_detail.html', {'post':post, 'form':form})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect(post)
	else:
		form = PostForm()
	return render(request, 'waterapp/post_new.html', {'form': form})


@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save()
			return redirect(post)

	else:
		if post.author == request.user:
			form = PostForm(instance=post)
			return render(request, 'waterapp/post_edit.html', {'form':form})
		else:
			return render(request, 'waterapp/warning.html')


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('waterapp:post_list')
    else:
        return render(request, 'waterapp/warning.html')



@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        post_pk = comment.post.pk
        comment.delete()
        return redirect('waterapp:post_detail', pk=post_pk)
    else:
        return render(request, 'waterapp/warning.html')


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(Post, pk=comment.post.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_date = timezone.now()
            comment.save()
        return redirect('waterapp:post_detail', pk=post.pk)

    else:
        form_edit = CommentForm(instance=comment)
        return render(request, 'waterapp/post_detail.html', {'post':post, 'form_edit':form_edit, 'pk':comment.pk})




class post1LV(ListView):
    model = Post1
    template_name = 'waterapp/post1_list.html'
    paginate_by = 7

    def get_queryset(self):
        qs = Post1.objects.all()
        q = self.request.GET.get('q', '') # GET request의 get 인자중에 q 가 있으면 가져오고, 없으면 빈 문자열

        if q:
            qs = qs.filter(title__icontains=q)

        return qs


def post1_detail(request, pk):
    post = get_object_or_404(Post1, pk=pk)
    if request.method == "POST":
        if request.user.id == None:
            return redirect('login')
        form = Comment1Form(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('waterapp:post1_detail', pk=post.pk)
    else:
        form = Comment1Form()
        return render(request, 'waterapp/post1_detail.html', {'post':post, 'form':form})

@login_required
def post1_new(request):
    if request.method == "POST":
        form = Post1Form(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post)
    else:
        form = Post1Form()
    return render(request, 'waterapp/post1_new.html', {'form': form})


@login_required
def post1_edit(request, pk):
    post = get_object_or_404(Post1, pk=pk)
    if request.method == 'POST':
        form = Post1Form(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post)

    else:
        if post.author == request.user:
            form = Post1Form(instance=post)
            return render(request, 'waterapp/post1_edit.html', {'form':form})
        else:
            return render(request, 'waterapp/warning.html')


@login_required
def post1_remove(request, pk):
    post = get_object_or_404(Post1, pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('waterapp:post1_list')
    else:
        return render(request, 'waterapp/warning.html')



@login_required
def comment1_remove(request, pk):
    comment = get_object_or_404(Comment1, pk=pk)
    if comment.author == request.user:
        post_pk = comment.post.pk
        comment.delete()
        return redirect('waterapp:post1_detail', pk=post_pk)
    else:
        return render(request, 'waterapp/warning.html')


@login_required
def comment1_edit(request, pk):
    comment = get_object_or_404(Comment1, pk=pk)
    post = get_object_or_404(Post1, pk=comment.post.id)

    if request.method == "POST":
        form = Comment1Form(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_date = timezone.now()
            comment.save()
        return redirect('waterapp:post1_detail', pk=post.pk)

    else:
        form_edit = Comment1Form(instance=comment)
        return render(request, 'waterapp/post1_detail.html', {'post':post, 'form_edit':form_edit, 'pk':comment.pk})










class post2LV(ListView):
    model = Post2
    template_name = 'waterapp/post2_list.html'
    paginate_by = 7

    def get_queryset(self):
        qs = Post2.objects.all()
        q = self.request.GET.get('q', '') # GET request의 get 인자중에 q 가 있으면 가져오고, 없으면 빈 문자열

        if q:
            qs = qs.filter(title__icontains=q)

        return qs


def post2_detail(request, pk):
    post = get_object_or_404(Post2, pk=pk)
    if request.method == "POST":
        if request.user.id == None:
            return redirect('login')
        form = Comment2Form(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('waterapp:post2_detail', pk=post.pk)
    else:
        form = Comment2Form()
        return render(request, 'waterapp/post2_detail.html', {'post':post, 'form':form})

@login_required
def post2_new(request):
    if request.method == "POST":
        form = Post2Form(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post)
    else:
        form = Post2Form()
    return render(request, 'waterapp/post2_new.html', {'form': form})


@login_required
def post2_edit(request, pk):
    post = get_object_or_404(Post2, pk=pk)
    if request.method == 'POST':
        form = Post2Form(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post)

    else:
        if post.author == request.user:
            form = Post2Form(instance=post)
            return render(request, 'waterapp/post2_edit.html', {'form':form})
        else:
            return render(request, 'waterapp/warning.html')


@login_required
def post2_remove(request, pk):
    post = get_object_or_404(Post2, pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('waterapp:post2_list')
    else:
        return render(request, 'waterapp/warning.html')



@login_required
def comment2_remove(request, pk):
    comment = get_object_or_404(Comment2, pk=pk)
    if comment.author == request.user:
        post_pk = comment.post.pk
        comment.delete()
        return redirect('waterapp:post2_detail', pk=post_pk)
    else:
        return render(request, 'waterapp/warning.html')


@login_required
def comment2_edit(request, pk):
    comment = get_object_or_404(Comment2, pk=pk)
    post = get_object_or_404(Post2, pk=comment.post.id)

    if request.method == "POST":
        form = Comment2Form(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_date = timezone.now()
            comment.save()
        return redirect('waterapp:post2_detail', pk=post.pk)

    else:
        form_edit = Comment2Form(instance=comment)
        return render(request, 'waterapp/post2_detail.html', {'post':post, 'form_edit':form_edit, 'pk':comment.pk})
