#!/usr/bin/env python
# -*- coding: utf-8 -*-
from erp.customer_management.forms import CustomerForm
from erp.customer_management.models import Customer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
import operator
from django.shortcuts import redirect
from django import forms
from erp.comment_management.forms import CommentForm
from erp.comment_management.models import Comment
from erp.common.fields import HiddenInputWithText
from erp.common.common import get_city_by_ip
from django.http import HttpResponseRedirect

def count_of_customers():
    """
    Count of customers
    """
    return Customer.objects.all().count()

def index(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error_message = form.errors
            form.fields['user_id'].widget = forms.HiddenInput(attrs={'value' : request.user.id})
            form.fields['rating'].widget = forms.HiddenInput(attrs={'value' : 0})
            return render_to_response('customer_management/create.html',
                                      {'form':form,'user': request.user, 'error_message': error_message})
    city = get_city_by_ip(request)
    form_filtered = CustomerForm(request.GET)
    if not form_filtered.data:
        return HttpResponseRedirect("/customers/?location="+str(city))
    customers = Customer.objects.order_by('-rating')
    for c in customers:
        c.comments_count = Comment.objects.filter(type=c.get_cname(),object_id=c.id).count()
    customers = sorted(customers, key=operator.attrgetter('rating'), reverse=True)
    if form_filtered:
        if form_filtered.data and len(form_filtered.errors)<len(form_filtered.fields):
            active_fields = {}
            for f in form_filtered.data:
                if form_filtered.data[f]!=u'':
                    active_fields[f] = form_filtered.data[f]
            for f in active_fields:
                try:
                    customers = filter(lambda x: active_fields[f] in x.__dict__[f],customers)
                except:
                    customers = filter(lambda x: str(active_fields[f]) in str(x.__dict__[f]),customers)
    paginator = Paginator(customers, 20) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        customers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        customers = paginator.page(paginator.num_pages)
    return render_to_response('customer_management/index.html', {'customers':customers, 'form_filtered':form_filtered,'user': request.user, 'request':request})

def details(request, customer_id):
    referer = request.META.get('HTTP_REFERER')
    customer = get_object_or_404(Customer, id=customer_id)
    form = CustomerForm(instance=customer)
    for field in form:
        field.field.widget.attrs['readonly'] = True
    form.fields['description'].widget = forms.HiddenInput()
    form.fields['user_id'].widget = forms.HiddenInput()
    form.fields['rating'].widget = forms.HiddenInput()
    form.fields['currency'].widget.attrs['disabled'] = 'disabled'
    form.fields['typeofwork'].widget.attrs['disabled'] = 'disabled'
    form.fields['creation_time'] = forms.CharField(widget=HiddenInputWithText(attrs={'value':form.instance.creation_time}),label="Время создания")
    form.fields['modification_time'] = forms.CharField(widget=HiddenInputWithText(attrs={'value':form.instance.modification_time}),label="Время редактирования")
    formComment = CommentForm()
    comments = Comment.objects.filter(type=customer.get_cname(),object_id=customer_id)
    comments_count = Comment.objects.filter(type=customer.get_cname(),object_id=customer_id).count()
    return render_to_response('customer_management/details.html', {'form':form,'formComment':formComment, 'user': request.user,'referer':referer,'comments':comments,'comments_count':comments_count})

@login_required
def edit(request, customer_id):
    if 'edit' in request.META.get('HTTP_REFERER'):
        referer = '/customers/'
    else:
        referer = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerForm(request.POST,instance=customer)
        form.fields['user_id'].widget = forms.HiddenInput()
        form.fields['rating'].widget = forms.HiddenInput()
        if customer.user_id_id == request.user.id and form.is_valid():
            form.save()
        else:
            error_message = form.errors
            return render_to_response('customer_management/edit.html', {'form':form, 'user': request.user,'error_message' : error_message,'referer':referer})
        form.fields['description'].widget = forms.HiddenInput()
        for field in form:
            field.field.widget.attrs['readonly'] = True
        form.fields['creation_time'] = forms.CharField(widget=HiddenInputWithText(attrs={'value':form.instance.creation_time}),label="Время создания")
        form.fields['modification_time'] = forms.CharField(widget=HiddenInputWithText(attrs={'value':form.instance.modification_time}),label="Время редактирования")
        form.fields['currency'].widget.attrs['disabled'] = 'disabled'
        form.fields['typeofwork'].widget.attrs['disabled'] = 'disabled'
        return render_to_response('customer_management/details.html', {'form':form, 'saved':True, 'user': request.user,'referer':referer})
    else:
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerForm(instance=customer)
        form.fields['user_id'].widget = forms.HiddenInput()
        form.fields['rating'].widget = forms.HiddenInput()
        return render_to_response('customer_management/edit.html', {'form':form, 'user': request.user,'referer':referer})

@login_required
def create(request):
    referer = request.META.get('HTTP_REFERER')
    form = CustomerForm()
    form.fields['user_id'].widget = forms.HiddenInput(attrs={'value' : request.user.id})
    form.fields['rating'].widget = forms.HiddenInput(attrs={'value' : 0})
    return render_to_response('customer_management/create.html', {'form':form, 'user': request.user,'referer':referer})

@login_required
def delete(request,customer_id):
    referer = request.META.get('HTTP_REFERER')
    cust = Customer.objects.get(id=customer_id)
    return render_to_response('customer_management/delete.html', {'customer':cust, 'user': request.user,'referer':referer})

@login_required
def deleteconfirmed(request,customer_id):
    referer = request.GET.get('ref', '')
    if Customer.objects.get(id=customer_id).user_id_id==request.user.id:
        Customer.objects.filter(id=customer_id).delete()
    return redirect(referer,{})