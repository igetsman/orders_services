#!/usr/bin/env python
# -*- coding: utf-8 -*-
import locale
import datetime

enc = locale.getpreferredencoding()
from erp.news_management.forms import NewsForm
from erp.news_management.models import News
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
import operator
from django.shortcuts import redirect
from django.db.models import Count
from django import forms
from erp.comment_management.forms import CommentForm
from erp.comment_management.models import Comment
from erp.employee_management.views import count_of_employees

def index(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        form.instance.date = datetime.datetime.now()
        if form.is_valid():
            form.save()
        else:
            error_message = form.errors
            form.fields['user_id'].widget = forms.HiddenInput(attrs={'value' : request.user.id})
            form.fields['rating'].widget = forms.HiddenInput(attrs={'value' : 0})
            return render_to_response('news_management/create.html',
                                      {'form':form,'user': request.user, 'error_message': error_message})
    form_filtered = NewsForm(request.GET)
    news = News.objects.order_by('-date');
    for e in news:
        e.comments_count = Comment.objects.filter(type=e.get_cname(),object_id=e.id).count()
    news = sorted(news, key=operator.attrgetter('rating'), reverse=True)
    if form_filtered:
        if form_filtered.data and len(form_filtered.errors)<len(form_filtered.fields):
            active_fields = {}
            for f in form_filtered.data:
                if form_filtered.data[f]!=u'':
                    active_fields[f] = form_filtered.data[f]
            for f in active_fields:
                try:
                    news = filter(lambda x: active_fields[f] in x.__dict__[f],news)
                except:
                    news = filter(lambda x: str(active_fields[f]) in str(x.__dict__[f]),news)
    paginator = Paginator(news, 5)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)
    return render_to_response('news_management/index.html', {'news': news,'form_filtered':form_filtered, 'user': request.user, 'request':request})

def details(request, news_id):
    news = get_object_or_404(News, id=news_id)
    form = NewsForm(instance=news)
    referer = request.META.get('HTTP_REFERER')
    for field in form:
        field.field.widget.attrs['readonly'] = True
    form.fields['description'].widget = forms.HiddenInput()
    form.fields['date'].widget = forms.HiddenInput()
    form.fields['user_id'].widget = forms.HiddenInput()
    form.fields['rating'].widget = forms.HiddenInput()
    formComment = CommentForm()
    comments = Comment.objects.filter(type=news.get_cname(),object_id=news_id)
    comments_count = Comment.objects.filter(type=news.get_cname(),object_id=news_id).count()
    return render_to_response('news_management/details.html', {'form': form,'formComment':formComment,'comments':comments,'comments_count':comments_count, 'user': request.user, 'referer':referer})

def dashboard(request):
    return render_to_response('dashboard/dashboard.html', {'user': request.user, 'request':request})


@login_required
def edit(request, news_id):
    if 'edit' in request.META.get('HTTP_REFERER'):
        referer = '/news/'
    else:
        referer = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        news = News.objects.get(id=news_id)
        form = NewsForm(request.POST, instance=news)
        form.fields['user_id'].widget = forms.HiddenInput()
        form.fields['rating'].widget = forms.HiddenInput()
        form.fields['date'].widget = forms.HiddenInput()
        if news.user_id_id == request.user.id and form.is_valid():
            form.save()
        else:
            error_message = form.errors
            return render_to_response('news_management/edit.html',
                                      {'form':form, 'user': request.user, 'error_message': error_message, 'referer':referer})
        news = get_object_or_404(News, id=news_id)
        form = NewsForm(instance=news)
        for field in form:
            field.field.widget.attrs['readonly'] = True
        form.fields['user_id'].widget = forms.HiddenInput()
        form.fields['rating'].widget = forms.HiddenInput()
        form.fields['description'].widget = forms.HiddenInput()
        form.fields['date'].widget = forms.HiddenInput()
        return render_to_response('news_management/details.html',
                                  {'form': form, 'saved': True, 'user': request.user, 'referer':referer})
    else:
        news = get_object_or_404(News, id=news_id)
        form = NewsForm(instance=news)
        form.fields['user_id'].widget = forms.HiddenInput()
        form.fields['rating'].widget = forms.HiddenInput()
        form.fields['date'].widget = forms.HiddenInput()
        return render_to_response('news_management/edit.html', {'form': form, 'user': request.user, 'referer':referer})


@login_required
def create(request):
    referer = request.META.get('HTTP_REFERER')
    form = NewsForm()
    form.fields['user_id'].widget = forms.HiddenInput(attrs={'value' : request.user.id})
    form.fields['rating'].widget = forms.HiddenInput(attrs={'value' : 0})
    form.fields['date'].widget = forms.HiddenInput(attrs={'value' : datetime.datetime.now() })
    return render_to_response('news_management/create.html', {'form':form,'user': request.user,'referer':referer})


@login_required
def delete(request, news_id):
    referer = request.META.get('HTTP_REFERER')
    new = News.objects.get(id=news_id)
    return render_to_response('news_management/delete.html', {'new': new, 'user': request.user,'referer': referer})


@login_required
def deleteconfirmed(request, news_id):
    referer = request.GET.get('ref', '')
    if News.objects.get(id=news_id).user_id_id == request.user.id:
        News.objects.filter(id=news_id).delete()
    return redirect(referer, {})