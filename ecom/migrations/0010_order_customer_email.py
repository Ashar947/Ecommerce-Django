# Generated by Django 4.1.5 on 2023-02-24 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0009_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_email',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
