from django.db import models

class Certificate(models.Model):
    doc_type = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=50, unique=True)
    edited_data = models.JSONField(null=True, blank=True)  # Store edited fields
    original_data = models.JSONField()  # Store original fields
    generated_pdf = models.BinaryField(null=True, blank=True)  # Store PDF in binary format
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    download_count = models.IntegerField(default=0)

        # New field to store the PDF file as binary data
    pdf_file = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return f"{self.recipient_name} - {self.doc_type}"
