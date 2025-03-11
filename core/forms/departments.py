from django import forms
from ..models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department', 'description']
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
        }

    def clean_department(self):
        department = self.cleaned_data.get('department')
        if not department or department.strip() == "":
            raise forms.ValidationError("Department name cannot be empty.")
        return department
