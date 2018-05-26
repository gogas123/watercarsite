# study/forms.py
from django import forms
from .models import Post, Comment, Post1, Comment1, Post2, Comment2
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_summernote import fields as summer_fields

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)

class PostForm(forms.ModelForm):

   class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '댓글을 입력해주세요.'}),
        }

class Post1Form(forms.ModelForm):

   class Meta:
        model = Post1
        fields = ['title', 'content']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
        }


class Comment1Form(forms.ModelForm):

    class Meta:
        model = Comment1
        fields = ('text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '댓글을 입력해주세요.'}),
        }


class Post2Form(forms.ModelForm):

   class Meta:
        model = Post2
        fields = ['title', 'content']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
        }


class Comment2Form(forms.ModelForm):

    class Meta:
        model = Comment2
        fields = ('text',)
        widgets = {
            'text' : forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '댓글을 입력해주세요.'}),
        }


class CreateUserForm(UserCreationForm):
    use = forms.BooleanField(
        required=False,
        initial=True,
        label = '',
        widget = forms.HiddenInput()
        )
    infor = forms.BooleanField(
        required=False,
        initial=True,
        label = '',
        widget = forms.HiddenInput()
        )
    name = forms.CharField(
        required=True,
        label = "이름",
        widget = forms.TextInput(attrs={ 'class': 'form-control1', 'placeholder': '이름을 입력해주세요'})
        )
    email = forms.EmailField(
        required=True,
        label="이메일",
        widget = forms.TextInput(attrs={'class': 'form-control1', 'placeholder': '이메일 주소를 입력해주세요' ,'id':'email'}),
        )
    username = forms.CharField(
        required=True,
        label="ID",
        widget = forms.TextInput(attrs={'class': 'form-control1', 'placeholder': 'ID를 입력해주세요','id':'idid'}),
        )

    password1 = forms.CharField(
        required=True,
        label="비밀번호",
        widget = forms.PasswordInput(attrs={'class': 'form-control1', 'placeholder': '숫자와 문자를 포함해 8자리 이상을 입력해주세요','id':'password1'}),
        )

    password2 = forms.CharField(
        required=True,
        label="비밀번호 확인",
        widget = forms.PasswordInput(attrs={'class': 'form-control1', 'placeholder': '같은 비밀번호를 다시 입력해주세요.' ,'id':'password2'}),
        )

    class Meta:
        model = User
        fields = ( 'use', 'infor','name' ,'username', 'email', 'password1', 'password2')
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control', 'help_text': ''}),
            'use' : forms.HiddenInput(),
            'infor' : forms.HiddenInput(),
        }