# Generated by Django 4.1.6 on 2023-02-20 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_user_cartitem_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='customer',
            new_name='user',
        ),
    ]