# Generated by Django 3.0.6 on 2020-06-28 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_contact_orders_orderupdate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
    ]
