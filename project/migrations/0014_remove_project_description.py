# Generated by Django 3.1.2 on 2020-11-09 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_auto_20201109_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='description',
        ),
    ]