# Generated by Django 3.2.4 on 2021-07-10 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
