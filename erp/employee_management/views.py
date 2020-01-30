#!/usr/bin/env python
# -*- coding: utf-8 -*-
import locale
enc = locale.getpreferredencoding()
from erp.employee_management.forms import EmployeeForm
from erp.employee_management.models import Employee
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
import operator
from django.shortcuts import redirect
from django.db.models import Count
from django import forms
from erp.comment_management.forms import CommentForm
from erp.comment_management.models import Comment
from erp.common.common import get_city_by_ip
from django.http import HttpResponseRedirect

def count_of_employees():
    """
    Count of employees
    """
    return Employee.objects.all().count()

def index(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            error_message = form.errors
            form.fields['user_id'].widget = forms.HiddenInput(attrs={'value' : request.user.id})
            form.fields['rating'].widget = forms.HiddenInput(attrs={'value' : 0})
            return render_to_response('employee_management/create.html',
                                      {'form':form,'user': request.user, 'error_message': error_message})
    city = get_city_by_ip(request)
    form_filtered = EmployeeForm(request.GET)
    if not form_filtered.data:
        return HttpResponseRedirect("/employees/?location="+str(city))
    employees = Employee.objects.annotate(photoes_count=Count('photo')).order_by('-rating');
    for e in employees:
        e.comments_count = Comment.objects.filter(type=e.get_cname(),object_id=e.id).count()
    employees = sorted(employees, key=operator.attrgetter('rating'), reverse=True)
    if form_filtered:
        if form_filtered.data and len(form_filtered.errors)<len(form_filtered.fields):
            active_fields = {}
            for f in form_filtered.data:
                if form_filtered.data[f]!=u'':
                    active_fields[f] = form_filtered.data[f]
            for f in active_fields:
                try:
                    employees = filter(lambda x: active_fields[f] in x.__dict__[f],employees)
                except:
                    employees = filter(lambda x: str(active_fields[f]) in str(x.__dict__[f]),employees)
    paginator = Paginator(employees, 20) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        employees = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        employees = paginator.page(paginator.num_pages)
    return render_to_response('employee_management/index.html', {'employees': employees,'form_filtered':form_filtered, 'user': request.user, 'request':request})

def details(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    form = EmployeeForm(instance=employee)
    referer = request.META.get('HTTP_REFERER')
    for field in form:
        field.field.widget.attrs['readonly'] = True
    form.fields['description'].widget = forms.HiddenInput()
    form.fields['user_id'].widget = forms.HiddenInput()
    form.fields['rating'].widget = forms.HiddenInput()
    form.fields['currency'].widget.attrs['disabled'] = 'disabled'
    form.fields['specialisation'].widget.attrs['disabled'] = 'disabled'
    formComment = CommentForm()
    comments = Comment.objects.filter(type=employee.get_cname(),object_id=employee_id)
    comments_count = Comment.objects.filter(type=employee.get_cname(),object_id=employee_id).count()
    return render_to_response('employee_management/details.html', {'form': form,'formComment':formComment,'comments':comments,'comments_count':comments_count, 'user': request.user, 'referer':referer})

def dashboard(request):
    return render_to_response('dashboard/dashboard.html', {'user': request.user, 'request':request})


@login_required
def edit(request, employee_id):
    if 'edit' in request.META.get('HTTP_REFERER'):
        referer = '/employees/'
    else:
        referer = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        employee = Employee.objects.get(id=employee_id)
        form = EmployeeForm(request.POST, instance=employee)
        form.fields['user_id'].widget = forms.HiddenInput()
        form.fields['rating'].widget = forms.HiddenInput()
        if employee.user_id_id == request.user.id and form.is_valid():
            form.save()
        else:
            error_message = form.errors
            return render_to_response('employee_management/edit.html',
                                      {'form':form, 'user': request.user, 'error_message': error_message, 'referer':referer})
        employee = get_object_or_404(Employee, id=employee_id)
        form = EmployeeForm(instance=employee)
        for field in form:
            field.field.widget.attrs['readonly'] = True
        form.fields['user_id'].widget = forms.HiddenInput()
        form.fields['rating'].widget = forms.HiddenInput()
        form.fields['description'].widget = forms.HiddenInput()
        form.fields['currency'].widget.attrs['disabled'] = 'disabled'
        form.fields['specialisation'].widget.attrs['disabled'] = 'disabled'
        return render_to_response('employee_management/details.html',
                                  {'form': form, 'saved': True, 'user': request.user, 'referer':referer})
    else:
        employee = get_object_or_404(Employee, id=employee_id)
        form = EmployeeForm(instance=employee)
        form.fields['user_id'].widget = forms.HiddenInput()
        form.fields['rating'].widget = forms.HiddenInput()
        return render_to_response('employee_management/edit.html', {'form': form, 'user': request.user, 'referer':referer})


@login_required
def create(request):
    referer = request.META.get('HTTP_REFERER')
    form = EmployeeForm()
    form.fields['user_id'].widget = forms.HiddenInput(attrs={'value' : request.user.id})
    form.fields['rating'].widget = forms.HiddenInput(attrs={'value' : 0})
    return render_to_response('employee_management/create.html', {'form':form,'user': request.user,'referer':referer})


@login_required
def delete(request, employee_id):
    referer = request.META.get('HTTP_REFERER')
    emp = Employee.objects.get(id=employee_id)
    return render_to_response('employee_management/delete.html', {'employee': emp, 'user': request.user,'referer': referer})


@login_required
def deleteconfirmed(request, employee_id):
    referer = request.GET.get('ref', '')
    if Employee.objects.get(id=employee_id).user_id_id == request.user.id:
        Employee.objects.filter(id=employee_id).delete()
    return redirect(referer, {})