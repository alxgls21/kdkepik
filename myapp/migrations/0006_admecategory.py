# Generated by Django 5.0.7 on 2024-08-04 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_harpcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Όνομα')),
                ('ip_address', models.URLField(blank=True, null=True, verbose_name='Διεύθυνση IP')),
                ('supervisory_tool', models.CharField(blank=True, max_length=100, verbose_name='Εποπτικό Μέσο')),
            ],
            options={
                'verbose_name': 'ΑΔΜΕ',
                'verbose_name_plural': 'ΑΔΜΕ',
            },
        ),
    ]