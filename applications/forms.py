from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'resume': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume and not resume.name.endswith(('.pdf', '.doc', '.docx')):
            raise forms.ValidationError("Only PDF, DOC, or DOCX files are allowed.")
        return resume