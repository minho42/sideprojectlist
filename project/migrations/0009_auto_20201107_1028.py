# Generated by Django 3.1.2 on 2020-11-07 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_auto_20201107_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='github_handle',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='producthunt_handle',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
