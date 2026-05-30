import uuid
from django.db import models


class Document(models.Model):

    name = models.CharField(max_length=200)

    certificate_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )

    department = models.CharField(max_length=100)

    document = models.FileField(
        upload_to='documents/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    verified = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):

        if not self.certificate_id:
            self.certificate_id = str(uuid.uuid4())[:8]

        if self.document:

            allowed_extensions = [
                '.pdf',
                '.jpg',
                '.jpeg',
                '.png'
            ]

            file_name = self.document.name.lower()

            self.verified = any(
                file_name.endswith(ext)
                for ext in allowed_extensions
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name