# Generated by Django 4.1.5 on 2023-03-11 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0018_alter_wishlist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='user',
        ),
    ]
