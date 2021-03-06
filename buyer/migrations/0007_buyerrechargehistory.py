# Generated by Django 3.2.2 on 2022-04-04 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0006_alter_buyerinfo_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerRechargeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=40)),
                ('country', models.CharField(max_length=400, null=True)),
                ('operator', models.CharField(max_length=400, null=True)),
                ('amount', models.CharField(max_length=400, null=True)),
            ],
        ),
    ]
