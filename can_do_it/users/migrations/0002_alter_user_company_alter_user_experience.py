# Generated by Django 4.1.7 on 2023-06-23 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='experience',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]