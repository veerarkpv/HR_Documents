from django.contrib import admin
from django.http import HttpResponse
from .models import Certificate

def download_pdf(modeladmin, request, queryset):
    for certificate in queryset:
        if certificate.pdf_file:
            response = HttpResponse(certificate.pdf_file, content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename="{certificate.recipient_name}_{certificate.doc_type}.pdf"'
            return response
    return HttpResponse("No PDF available", status=404)

download_pdf.short_description = "Download Selected PDFs"

class CertificateAdmin(admin.ModelAdmin):
    list_display = ('recipient_name', 'doc_type', 'download_count', 'created_at')
    actions = [download_pdf]

admin.site.register(Certificate, CertificateAdmin)
