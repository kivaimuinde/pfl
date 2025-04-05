from django import forms
from ..models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department','manager', 'description']
        widgets = {
            'department': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter department name',
                'required': 'required'  # HTML5 validation
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Enter department description (optional)'
            }),
            
            'manager': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean_department(self):
        department = self.cleaned_data.get('department')
        if not department or department.strip() == "":
            raise forms.ValidationError("Department name cannot be empty.")
        return department
    
    def clean_manager(self):
        manager = self.cleaned_data.get('manager')
        if manager and Department.objects.filter(manager=manager).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(f"{manager} is already assigned as a manager to another department.")
        return manager
