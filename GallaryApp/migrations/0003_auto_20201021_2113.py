# Generated by Django 2.2.7 on 2020-10-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GallaryApp', '0002_auto_20201021_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallaryimages',
            name='file',
            field=models.ImageField(db_column='FILE', null=True, upload_to=''),
        ),
    ]
