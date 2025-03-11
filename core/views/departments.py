from django.shortcuts import render, get_object_or_404, redirect
from ..models import Department
from .. forms.departments import DepartmentForm

# List view
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'core/departments/department_list.html', {'departments': departments})

# Detail view
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'core/departments/department_detail.html', {'department': department})

# Create view
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'core/departments/department_form.html', {'form': form})

# Update view
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('core:department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'core/departments/department_form.html', {'form': form})

# Delete view
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        department.delete()
        return redirect('core:department_list')
    return render(request, 'core/departments/department_confirm_delete.html', {'department': department})
