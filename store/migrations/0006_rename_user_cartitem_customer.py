# Generated by Django 4.1.6 on 2023-02-20 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_customer_cartitem_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='user',
            new_name='customer',
        ),
    ]
