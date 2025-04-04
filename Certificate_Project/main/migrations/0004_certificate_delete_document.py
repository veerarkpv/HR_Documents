# Generated by Django 5.1.6 on 2025-03-03 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_date_issued_document_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(max_length=100)),
                ('recipient_name', models.CharField(max_length=255)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('verification_code', models.CharField(max_length=50, unique=True)),
                ('edited_data', models.JSONField(blank=True, null=True)),
                ('original_data', models.JSONField()),
                ('generated_pdf', models.BinaryField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('download_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
