# Create your views here.
from django.http import request
from erp.user_management.models import CustomUser
from erp.avator_management.models import Avator
from erp.user_management.forms import CustomUserForm
from erp.user_management.forms import UserForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms.models import modelformset_factory
from erp.employee_management.models import Employee
from erp.customer_management.models import Customer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, Http404, HttpResponseRedirect, HttpResponse, render_to_response
import operator
from django.db.models import Count

def profile(request,u_id=None):
    if u_id is None:
        u_id = request.user.id
    is_owner = str(request.user.id) == str(u_id)
    try:
        avatorka = get_object_or_404(Avator, custom_user=u_id)
    except:
        avatorka = None
    my_emp = Employee.objects.annotate(photoes_count=Count('photo')).filter(user_id_id=u_id)
    my_emp = my_emp.order_by('-rating');
    employees = sorted(my_emp, key=operator.attrgetter('rating'), reverse=True)
    paginator = Paginator(employees, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        my_emp = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        my_emp = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        my_emp = paginator.page(paginator.num_pages)
    my_customers = Customer.objects.filter(user_id_id=u_id).order_by('-rating');
    my_customers = sorted(my_customers, key=operator.attrgetter('rating'), reverse=True)
    paginator = Paginator(my_customers, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        my_customers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        my_customers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        my_customers = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        custom_user = CustomUser.objects.get(user_id=u_id)
        usr = User.objects.get(id=u_id)
        form = CustomUserForm(request.POST, instance=custom_user)
        formU = UserForm(request.POST, instance=usr)
        if form.is_valid() and formU.is_valid():
            form.save()
            formU.save()
        else:
            return render_to_response('user_management/profile.html', {'error_message' : form.errors, 'avatorka':avatorka, 'error_message2' : formU.errors, 'user': request.user,'form':form, 'is_owner' : is_owner, 'formU': formU, 'employees':my_emp, 'customers':my_customers,'request':request})
    custom_user = get_object_or_404(CustomUser, user_id=u_id)
    usr = get_object_or_404(User, id=u_id)
    form = CustomUserForm()
    formU = UserForm(request.POST, instance=usr)
    if (not is_owner):
        for field in form:
            field.field.widget.attrs['readonly'] = True
        for field in formU:
            field.field.widget.attrs['readonly'] = True
    form.fields['custom_description'].widget.attrs['value'] = custom_user.custom_description
    form.fields['custom_email'].widget.attrs['value'] = custom_user.custom_email
    form.fields['custom_phone'].widget.attrs['value'] = custom_user.custom_phone
    formU.fields['first_name'].widget.attrs['value'] = usr.first_name
    formU.fields['last_name'].widget.attrs['value'] = usr.last_name
    return render_to_response('user_management/profile.html', {'form':form, 'avatorka':avatorka, 'user' : request.user, 'is_owner' : is_owner, 'formU': formU, 'employees':my_emp, 'customers':my_customers, 'request':request})


