# Generated by Django 3.2.2 on 2022-05-16 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0012_alter_buyersgippingaddress_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='color',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.CharField(default=1, max_length=5),
            preserve_default=False,
        ),
    ]