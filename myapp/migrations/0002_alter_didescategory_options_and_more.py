# Generated by Django 5.0.7 on 2024-08-04 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='didescategory',
            options={'verbose_name': 'Κατηγορία Dides', 'verbose_name_plural': 'Κατηγορίες Dides'},
        ),
        migrations.AlterField(
            model_name='didescategory',
            name='application',
            field=models.CharField(choices=[('monitoring', 'Monitoring'), ('kepik_apps', 'Εφαρμογές ΚΕΠΙΚ'), ('useful_links', 'Χρήσιμοι Σύνδεσμοι'), ('pyrseia', 'ΠΥΡΣΕΙΑ'), ('vosip', 'VOSIP')], max_length=20, verbose_name='Εφαρμογή'),
        ),
        migrations.AlterField(
            model_name='didescategory',
            name='category',
            field=models.CharField(choices=[('unclassified', 'Αδιαβάθμητο Δίκτυο'), ('classified', 'Διαβαθμισμένο Δίκτυο')], max_length=20, verbose_name='Κατηγορία'),
        ),
        migrations.AlterField(
            model_name='didescategory',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='Διεύθυνση IP'),
        ),
        migrations.AlterField(
            model_name='didescategory',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Όνομα'),
        ),
        migrations.AlterField(
            model_name='didescategory',
            name='supervisory_tool',
            field=models.CharField(blank=True, max_length=100, verbose_name='Εποπτικό Μέσο'),
        ),
    ]