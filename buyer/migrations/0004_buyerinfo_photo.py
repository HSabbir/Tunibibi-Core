# Generated by Django 3.2.9 on 2022-03-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0003_buyerinvitationcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyerinfo',
            name='photo',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
