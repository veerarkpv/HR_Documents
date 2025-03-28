# Generated by Django 5.1.6 on 2025-02-25 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_document_content_document_download_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='date_issued',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='document',
            name='name',
        ),
        migrations.RemoveField(
            model_name='document',
            name='verification_code',
        ),
        migrations.AddField(
            model_name='document',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
