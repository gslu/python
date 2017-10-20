# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.views.generic import ListView
from django.db.models import Count
from taggit.models import Tag
from .models import Post,Comment
from .forms import EmailPostForm,CommentForm,LoginForm

# Create your views here.


def login_user(request):

    login_status = None
    if request.method == 'POST':

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                login_status = 200
                return HttpResponseRedirect(request.META.get('REFERER', '/'))
            else:
                login_status = 400
                login_form = LoginForm(initial={"username": cd["username"],
                                                "password": cd["password"]})

    else:
        login_form = LoginForm()


    return render(request,"blog/login.html",{"login_form":login_form,
                                             "login_status":login_status})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'blog/post/list.html'

def post_list(request,tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 6)  # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts': posts,
                                                 'page':page,
                                                 'tag':tag,
                                                 'user':request.user})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year
                                    #publish__month=month, #不识别month,day
                                    #publish__day=day
                                )
    if post:
        post.accesstimes += 1
        post.save()

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        #A comment was post
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    return render(request,'blog/post/detail.html',{'post': post,
                                                   'comments':comments,
                                                   'comment_form':comment_form,
                                                   'new_comment':new_comment,
                                                   'similar_posts':similar_posts})

def post_share(request,post_id):
    # Retrieve post by id
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    cd = None
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        # Form fields passed validation
        if form.is_valid():
            cd = form.cleaned_data
            #....send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],
                                                                   cd['email'],
                                                                   post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,
                                                                     post_url,
                                                                     cd['name'],
                                                                     cd['comments'])
            send_mail(subject=subject,
                      message=message,
                      from_email='352240513@qq.com',
                      recipient_list=[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'form':form,'post':post,'sent':sent,'cd':cd})


def music(request,blogger=None):
    return render(request,'blog/music/music.html',{})

