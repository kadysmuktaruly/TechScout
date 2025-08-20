from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'salary', 'is_remote']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'salary': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary

    