# Generated by Django 4.1.5 on 2023-03-11 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0014_alter_cart_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=25)),
                ('Price', models.IntegerField()),
                ('Image', models.ImageField(upload_to='ecom/images')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecom.category')),
            ],
        ),
    ]
