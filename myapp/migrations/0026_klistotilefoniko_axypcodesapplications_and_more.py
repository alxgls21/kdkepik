# Generated by Django 5.0.7 on 2024-09-10 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_delete_imerisiodinamologio'),
    ]

    operations = [
        migrations.CreateModel(
            name='KlistoTilefoniko',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('YPETHA', 'ΥΠΕΘΑ'), ('GEETHA', 'ΓΕΕΘΑ'), ('GES', 'ΓΕΣ'), ('GEN', 'ΓΕΝ'), ('GEA', 'ΓΕΑ'), ('CYPRUS', 'ΚΥΠΡΟΣ')], max_length=10, verbose_name='Κατηγορία')),
                ('stoixeia', models.CharField(max_length=255, verbose_name='Στοιχεία')),
                ('number', models.CharField(max_length=4, verbose_name='Νούμερο')),
            ],
        ),
        migrations.CreateModel(
            name='AxypCodesApplications',
            fields=[
            ],
            options={
                'verbose_name': 'Λοιπές Εφαρμογές',
                'verbose_name_plural': 'Λοιπές Εφαρμογές',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('myapp.axypcodescategory',),
        ),
        migrations.CreateModel(
            name='AxypCodesComputers',
            fields=[
            ],
            options={
                'verbose_name': 'Υπολογιστές',
                'verbose_name_plural': 'Υπολογιστές',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('myapp.axypcodescategory',),
        ),
        migrations.CreateModel(
            name='AxypCodesPhoneCodes',
            fields=[
            ],
            options={
                'verbose_name': 'Κωδικοί Λειτουργίας Τηλεφώνου',
                'verbose_name_plural': 'Κωδικοί Λειτουργίας Τηλεφώνου',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('myapp.axypcodescategory',),
        ),
        migrations.CreateModel(
            name='AxypCodesPyrseia',
            fields=[
            ],
            options={
                'verbose_name': 'Πυρσεία',
                'verbose_name_plural': 'Πυρσεία',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('myapp.axypcodescategory',),
        ),
        migrations.CreateModel(
            name='AxypCodesStaff',
            fields=[
            ],
            options={
                'verbose_name': 'Στελέχη',
                'verbose_name_plural': 'Στελέχη',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('myapp.axypcodescategory',),
        ),
        migrations.CreateModel(
            name='AxypCodesUsefulPhones',
            fields=[
            ],
            options={
                'verbose_name': 'Χρήσιμα Τηλέφωνα',
                'verbose_name_plural': 'Χρήσιμα Τηλέφωνα',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('myapp.axypcodescategory',),
        ),
    ]