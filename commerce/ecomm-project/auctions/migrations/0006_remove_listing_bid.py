# Generated by Django 4.0.4 on 2022-04-26 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
    ]
