# Generated by Django 5.0.6 on 2024-10-12 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0042_remove_axypkepikservicereport_officer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='axypkepikservicereport',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='axyp_anafora/'),
        ),
    ]
