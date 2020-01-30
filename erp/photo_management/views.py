from erp.photo_management.models import Photo
from erp.employee_management.models import Employee
from erp.photo_management.forms import PhotoForm
from django.shortcuts import get_object_or_404, render_to_response
from django.forms.models import inlineformset_factory

def create(request,employee_id):
    form = PhotoForm()
    return render_to_response('photo_management/create.html', {'employee_id':employee_id, 'user': request.user,'form':form})

def index(request,employee_id):
    referer = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        employee = Employee.objects.get(pk=employee_id)
        form = PhotoForm(request.POST,request.FILES)
        # PhotoFormSet = inlineformset_factory(Employee, Photo)
        # formset = PhotoFormSet(request.POST, request.FILES, instance=employee)
        if Employee.objects.get(id=employee_id).user_id_id==request.user.id:
            if form.is_valid():
                form = form.save(commit=False)
                form.employee = employee
                form.save()
            else:
                error_message = form.errors
                return render_to_response('photo_management/create.html', {'employee_id':employee_id, 'user': request.user,'form':form,'error_message':error_message})
    photos = Photo.objects.filter(employee=employee_id);
    employee = Employee.objects.get(pk=employee_id)
    return render_to_response('photo_management/album.html', {'photos':photos,'employee':employee, 'user': request.user, 'referer':referer})

def delete(request,employee_id):
    try:
        photos = request.POST.getlist(u'id')
        if Employee.objects.get(id=employee_id).user_id_id==request.user.id:
            for photo in photos:
                Photo.objects.filter(id=photo).delete()
    except KeyError:
        return render_to_response('photo_management/album.html', {
            'error_message': "You didn't select any photo.",
        })
    photos = Photo.objects.filter(employee=employee_id);
    employee = Employee.objects.get(pk=employee_id)
    return render_to_response('photo_management/album.html', {'photos':photos,'employee':employee, 'user': request.user})