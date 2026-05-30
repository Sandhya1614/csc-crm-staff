
from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document

        fields = [
            'name',
            'department',
            'document',
            'verified'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'glass-input'}),
            'certificate_id': forms.TextInput(attrs={'class': 'glass-input'}),
            'department': forms.TextInput(attrs={'class': 'glass-input'}),
            'document': forms.FileInput(attrs={'class': 'glass-input' }),
        }