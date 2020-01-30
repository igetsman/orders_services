from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from erp.employee_management.models import Employee


def robots(request):
    user = request.user
    return render_to_response('robots.txt', {'request': request})

    
    
    
