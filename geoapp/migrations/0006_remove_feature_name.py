# Generated by Django 5.1 on 2024-09-02 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0005_feature_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='name',
        ),
    ]
