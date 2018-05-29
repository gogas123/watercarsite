from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic import ListView
from .models import Post, Comment, Post1, Comment1, Post2, Comment2, Constructionpost, TOS
from .forms import PostForm, CommentForm, CreateUserForm, Post1Form, Comment1Form, Post2Form, Comment2Form
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, QueryDict
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import mail_managers, send_mail,EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

UserModel = get_user_model()



def index(request):
	return render(request, 'waterapp/index.html')


def about(request):
	return render(request, 'waterapp/about.html')

class services(ListView):
    model = Constructionpost
    template_name = 'waterapp/services.html'
    paginate_by = 9

    def get_queryset(self):
        qs = Constructionpost.objects.all()
        q = self.request.GET.get('q', '') # GET request의 get 인자중에 q 가 있으면 가져오고, 없으면 빈 문자열

        if q:
            qs = qs.filter(title__icontains=q)

        return qs

def introduce(request):
	return render(request, 'waterapp/introduce.html')


def post(request):
	return render(request, 'waterapp/post.html')


def agree(request):
    toss = TOS.objects.all()

    return render(request, 'waterapp/agree.html', {'toss':toss})

def password_reset_done(request):
    return render(request, 'waterapp/password_reset_done.html')

def password_reset_complete(request):
    return render(request, 'waterapp/password_reset_complete.html')

class signup(View):


    def get(self, request):
        if request.user.is_authenticated:
            return redirect("waterapp:index")
        form = CreateUserForm()
        return render(request, 'waterapp/signup.html', {'form':form})

    def post(self, request):

        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('waterapp/acc_active_email.html',{
                'user':user, 'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
                })
            mail_subject = '계정을 활성화 시켜 주세요.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to= [to_email])
            email.send()
            return render(request, 'waterapp/confirm_email_sent.html')

        print(form.errors)


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



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64).decode())
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("waterapp:index")
    else:
        return HttpResponse('작성하신 이메일의 메일함을 확인해주세요')


def agree(request):
    toss = TOS.objects.all()

    return render(request, 'waterapp/agree.html', {'toss':toss})

class DuplicationCheck(View):
    def post(self, request):
        # user = get_object_or_404(User, username=username)
        username = request.POST.get('username', None)
        data = {
            'is_taken': User.objects.filter(username__iexact=username).exists()
            }
        return JsonResponse(data)


def password_reset(request):
    return render(request, 'registration/password_reset_form.html')



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, ('비밀번호가 성공적으로 변경되었습니다.'))
            return redirect('waterapp:index')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = '/reset/done/'
    template_name = 'waterapp/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context

def password_reset_done(request):
    return render(request, "waterapp/password_reset_done.html")

class PasswordResetView(PasswordContextMixin, FormView):

    email_template_name = 'waterapp/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'waterapp/password_reset_subject.txt'
    success_url = '/password_reset/done/'
    template_name = 'waterapp/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)
