# Generated by Django 5.0.7 on 2024-08-09 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_axypkepikservicereport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='axypkepikservicereport',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='axypkepikservicereport',
            name='pdf_file',
        ),
        migrations.AddField(
            model_name='axypkepikservicereport',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/'),
        ),
    ]
