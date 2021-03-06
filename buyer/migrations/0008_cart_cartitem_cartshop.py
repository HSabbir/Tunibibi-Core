# Generated by Django 3.2.2 on 2022-05-11 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0018_alter_review_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('buyer', '0007_buyerrechargehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyer.cart')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_shop', to='seller.shopinfo')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('cart_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='buyer.cartshop')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='seller.shopproduct')),
            ],
        ),
    ]
