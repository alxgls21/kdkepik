# Generated by Django 5.0.7 on 2024-09-10 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0035_remove_soldier_iban_soldier_posto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldier',
            name='posto',
            field=models.CharField(blank=True, choices=[('HARP', 'HARP'), ('Helpdesk', 'Helpdesk'), ('Διαχείριση Δικτύων / Κυκλωμάτων', 'Διαχείριση Δικτύων / Κυκλωμάτων'), ('Τηλέτυπα', 'Τηλέτυπα'), ('Τηλεφωνικό', 'Τηλεφωνικό'), ('Τμήμα ΟΤΕ', 'Τμήμα ΟΤΕ'), ('ΥΕΣΑ', 'ΥΕΣΑ')], max_length=100, null=True, verbose_name='ΠΟΣΤΟ'),
        ),
    ]