# -*- coding: utf-8 -*-
from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    password = forms.CharField(widget=forms.PasswordInput,label=u"密码")


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=40,min_length=3,label=u"帐号")
    phone = forms.CharField(max_length=20, label=u"手机")
    password = forms.CharField(widget=forms.PasswordInput,label=u"密码")



