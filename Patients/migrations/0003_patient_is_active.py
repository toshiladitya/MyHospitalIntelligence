# Generated by Django 4.2.4 on 2023-09-15 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patients', '0002_remove_patient_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
