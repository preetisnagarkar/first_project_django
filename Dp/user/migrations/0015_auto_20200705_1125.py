# Generated by Django 3.0.6 on 2020-07-05 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20200704_1339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category_wt',
            new_name='weight',
        ),
    ]
