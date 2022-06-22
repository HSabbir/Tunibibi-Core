# Generated by Django 3.2.2 on 2022-05-16 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('buyer', '0009_bankrecipt'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerSgippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile_number', models.CharField(max_length=20)),
                ('street_address', models.TextField(blank=True, null=True)),
                ('apt_suite_unit', models.TextField(blank=True, null=True)),
                ('city', models.TextField(null=True)),
                ('zip_code', models.TextField(null=True)),
                ('default', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]