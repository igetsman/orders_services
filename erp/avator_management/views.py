from erp.photo_management.models import Photo
from erp.user_management.models import CustomUser
from erp.avator_management.models import Avator
from erp.avator_management.forms import AvatorForm
from django.shortcuts import get_object_or_404, render_to_response
from django.shortcuts import redirect

def change(request):
    if request.method == 'POST':
        custom_user = CustomUser.objects.get(pk=request.user.id)
        form = AvatorForm(request.POST,request.FILES)
        # PhotoFormSet = inlineformset_factory(Employee, Photo)
        # formset = PhotoFormSet(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            Avator.objects.filter(custom_user=request.user.id).delete()
            form = form.save(commit=False)
            form.custom_user = custom_user
            form.save()
    return redirect('/accounts/profile/', {})

