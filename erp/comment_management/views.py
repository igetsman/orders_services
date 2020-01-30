from erp.user_management.models import CustomUser
from erp.comment_management.forms import CommentForm
from erp.customer_management.models import Customer
from erp.employee_management.models import Employee
import erp.customer_management.views
import erp.employee_management.views
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
import datetime

def add(request,type,obj_id):
    referer = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        custom_user = CustomUser.objects.get(pk=request.user.id)
        form = CommentForm(request.POST)
        form.instance.type = type
        form.instance.object_id = obj_id
        form.instance.date = datetime.datetime.now()
        form.instance.author = custom_user
        if form.is_valid():
            form.save()
    return redirect(referer,{})

def open_details(request,type,id):
    return {
        'employee': erp.employee_management.views.details(request,id),
        'customer': erp.customer_management.views.details(request,id),
        }[type]
