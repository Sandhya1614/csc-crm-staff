import os
from django.db import models
 


def document_upload_path( instance,filename):
    return os.path.join("documents",filename)


class Document(models.Model):
    STATUS_CHOICES = [
        ('verified', 'Verified'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]

    DOC_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_upload_path)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.CharField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f"{self.name} ({self.status})"

    def get_file_extension(self):
        _, ext = os.path.splitext(self.file.name)
        return ext.lower().strip('.')

    def get_doc_type(self):
        ext = self.get_file_extension()
        if ext == 'pdf':
            return 'pdf'
        elif ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            return 'image'
        return 'other'

    def save(self, *args, **kwargs):
        if self.file:
           self.doc_type = self.get_doc_type()
        super().save(*args, **kwargs)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
