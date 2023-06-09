# Generated by Django 4.1.5 on 2023-03-10 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecom', '0011_remove_order_category_remove_order_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=15)),
                ('city', models.CharField(max_length=15)),
                ('contact_number', models.IntegerField()),
                ('profile_image', models.ImageField(default='user/images/default.PNG', upload_to='user/images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
