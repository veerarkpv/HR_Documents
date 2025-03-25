from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit
from .models import Certificate
import json
from io import BytesIO
from django.utils.timezone import now

def home(request):
    return render(request, 'home.html')

def details(request):
    if request.method == 'POST':
        doc_type = request.POST.get('doc_type')
        return render(request, 'details.html', {'doc_type': doc_type})
    return render(request, 'home.html')

def preview(request):
    if request.method == 'POST':
        doc_type = request.POST.get('doc_type')
        recipient_name = request.POST.get('recipient_name')
        verification_code = request.POST.get('verification_code')
        #print(doc_type, recipient_name, verification_code)
        if not doc_type or not recipient_name or not verification_code:
            return render(request, 'home.html', {'error': 'Missing required fields'})

        # Retrieve the stored certificate details
        try:
            certificate = Certificate.objects.get(
                doc_type=doc_type,
                recipient_name=recipient_name,
                verification_code=verification_code
            )

            form_data = json.loads(certificate.edited_data) if certificate.edited_data else json.loads(certificate.original_data)

        except Certificate.DoesNotExist:
            form_data = {key: request.POST.get(key) for key in request.POST.keys()}

        template_name = f"certificates/{doc_type}_preview.html"
        return render(request, template_name, form_data)

    return render(request, 'home.html')

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

def generate_pdf(request):
    if request.method == 'POST':
        try:
            doc_type = request.POST.get('doc_type')
            if not doc_type:
                return HttpResponse("Document type missing", status=400)

            recipient_name = request.POST.get('recipient_name', 'Unknown')
            # print(recipient_name)
            verification_code = request.POST.get('verification_code', '')

            # Dynamically collect all form fields from request.POST
            form_data = {key: request.POST.get(key, '') for key in request.POST.keys()}
            form_data['doc_type'] = doc_type
            form_data['for_pdf'] = True  # Flag for PDF-specific rendering

            # Load the appropriate preview template dynamically
            template_name = f"certificates/{doc_type}_preview.html"
            template = get_template(template_name)
            html = template.render(form_data)

            # PDF configuration options
            options = {
                'enable-local-file-access': '',
                'quiet': '',
                'viewport-size': '1000x600',
                'margin-top': '0',
                'margin-right': '0',
                'margin-bottom': '0',
                'margin-left': '0',
                'encoding': 'UTF-8',
                'no-stop-slow-scripts': '',  # Allow scripts to fully load images
                'load-error-handling': 'ignore',  # Prevent errors if images take time to load
                'zoom': '1.3',  # Scale the content properly
                'no-images': '',
            }

            pdf_bytes = pdfkit.from_string(html, False, configuration=config, options=options)

            # Store in DB
            certificate, created = Certificate.objects.get_or_create(
                verification_code=verification_code,
                defaults={
                    'recipient_name': recipient_name,
                    'doc_type': doc_type,
                    'original_data': form_data,  # Store initial data
                    'pdf_file': pdf_bytes,  # Store PDF as binary data
                    'download_count': 1,
                }
            )
            #print(certificate,"hii",created)
            # If the certificate already exists, update its details
            if not created:
                certificate.edited_data = json.dumps(form_data)
                certificate.download_count += 1
                certificate.pdf_file = pdf_bytes  # Update stored PDF
                certificate.updated_at = now()
                certificate.save()

            # Return PDF response
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            filename = f"{recipient_name}_{doc_type}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # Set download completion cookie
            response.set_cookie(
                'download_complete',
                'true',
                max_age=10,
                path='/',
                samesite='Lax',
                secure=False  # Set to True in production
            )

            return response

        except Exception as e:
            print(f"PDF Generation Error: {str(e)}")
            return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

    return redirect('home')

def success(request):
    return render(request, 'success.html')