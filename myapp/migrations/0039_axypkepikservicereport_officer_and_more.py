# Generated by Django 5.0.6 on 2024-10-12 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0038_delete_postareport'),
    ]

    operations = [
        migrations.AddField(
            model_name='axypkepikservicereport',
            name='officer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.officerservicereport'),
        ),
        migrations.AlterField(
            model_name='axypkepikservicereport',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='axyp_anafora/'),
        ),
    ]
