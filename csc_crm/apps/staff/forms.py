from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document name (e.g. Resume, Aadhaar Card)',
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png,.gif,.webp,.doc,.docx',
            }),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(
                    "File size must be under 10MB."
                )

            allowed_extensions = [
                'pdf', 'jpg', 'jpeg', 'png',
                'gif', 'webp', 'doc', 'docx'
            ]

            ext = file.name.rsplit('.', 1)[-1].lower()

            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    f"Unsupported file type '.{ext}'."
                )

        return file


class DocumentStatusForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['status']

        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }