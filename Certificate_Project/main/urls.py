from django.urls import path
from .views import home, details, preview, generate_pdf, success

urlpatterns = [
    path('', home, name='home'),
    path('details/', details, name='details'),
    path('preview/', preview, name='preview'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('success/', success, name='success'),
]
