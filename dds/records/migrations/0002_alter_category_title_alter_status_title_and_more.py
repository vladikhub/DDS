# Generated by Django 5.2.1 on 2025-05-15 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(unique=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='title',
            field=models.CharField(unique=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='title',
            field=models.CharField(unique=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='title',
            field=models.CharField(unique=True),
        ),
    ]
