# Generated by Django 5.0.6 on 2024-08-05 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_admecategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficerServiceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(max_length=50, verbose_name='Βαθμός')),
                ('last_name', models.CharField(max_length=100, verbose_name='Επώνυμο')),
                ('first_name', models.CharField(max_length=100, verbose_name='Όνομα')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Τηλ Επικοινωνίας')),
            ],
            options={
                'verbose_name': 'Αξιωματικός Υπηρεσίας ΚΕΠΙΚ',
                'verbose_name_plural': 'Αξιωματικοί Υπηρεσίας ΚΕΠΙΚ',
            },
        ),
    ]