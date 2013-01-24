# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from ponyFiction.stories.models import Author, Comment, Vote
from django.core.paginator import Paginator
from ponyFiction.stories.forms.author import AuthorEditEmailForm, AuthorEditPasswordForm, AuthorEditProfileForm 
@login_required
@csrf_protect
def author_info(request, **kwargs):
    user_id = kwargs.pop('user_id', None)
    page_title = kwargs.pop('page_title', None)
    if user_id is None:
        author = Author.objects.get(pk=request.user.id)
        comments_list = Comment.objects.filter(in_story__authors=request.user.id)
        template = 'author_dashboard.html'
    else:
        author = Author.objects.get(pk=user_id)
        comments_list = author.comment_set.all()
        template = 'author_overview.html'
    comments_count = comments_list.count()
    series = author.series_set.all()
    stories = author.story_set.all()
    votes = [Vote.objects.filter(direction=True).filter(story__authors__id=author.id).count(),
             Vote.objects.filter(direction=False).filter(story__authors__id=author.id).count()]
    paged = Paginator(comments_list, settings.COMMENTS_COUNT['page'], orphans=settings.COMMENTS_ORPHANS)
    comments = paged.page(1).object_list
    num_pages = paged.num_pages
    data = {
            'author' : author,
            'series' : series,
            'stories' : stories,
            'comments' : comments,
            'num_pages': num_pages,
            'comments_count': comments_count,
            'page_title': page_title,
            'votes': votes
            }
    return render(request, template, data)


@login_required
@csrf_protect
def author_edit(request, **kwargs):
    page_title = kwargs.pop('page_title', None)
    author = request.user
    data={}
    if request.POST:
        if 'save_profile' in request.POST:
            profile_form = AuthorEditProfileForm(request.POST, instance=author, prefix='profile_form')
            if profile_form.is_valid():
                profile_form.save()
                data['profile_ok'] = True
        else:
            profile_form = AuthorEditProfileForm(instance=author, prefix='profile_form')
        if 'save_email' in request.POST:
            email_form = AuthorEditEmailForm(request.POST, author=author, prefix='email_form')
            if email_form.is_valid():
                email_form.save()
                data['email_ok'] = True
        else:
            email_form = AuthorEditEmailForm(author=author, prefix='email_form')
        if 'save_password' in request.POST:
            password_form = AuthorEditPasswordForm(request.POST, author=author, prefix='password_form')
            if password_form.is_valid():
                password_form.save()
                data['password_ok'] = True
        else:
            password_form = AuthorEditPasswordForm(author=author, prefix='password_form')
    else:
        profile_form = AuthorEditProfileForm(instance=author, prefix='profile_form')
        email_form = AuthorEditEmailForm(author=author, prefix='email_form')
        password_form = AuthorEditPasswordForm(author=author, prefix='password_form')
    data.update({'profile_form': profile_form,
          'email_form': email_form,
          'password_form': password_form,
          'page_title': page_title
          })
    return render(request, 'author_profile_edit.html', data)