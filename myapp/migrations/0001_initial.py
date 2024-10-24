# Generated by Django 5.0.7 on 2024-08-04 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DidesCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('unclassified', 'Αδιαβάθμητο Δίκτυο'), ('classified', 'Διαβαθμισμένο Δίκτυο')], max_length=20)),
                ('application', models.CharField(choices=[('monitoring', 'Monitoring'), ('kepik_apps', 'Εφαρμογές ΚΕΠΙΚ'), ('useful_links', 'Χρήσιμοι Σύνδεσμοι'), ('pyrseia', 'ΠΥΡΣΕΙΑ'), ('vosip', 'VOSIP')], max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('ip_address', models.GenericIPAddressField()),
                ('supervisory_tool', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
