# Generated by Django 5.0 on 2024-01-19 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('brand_name', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('main_image_url', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('regular_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('default_seller_id', models.CharField(max_length=12)),
                ('store_id', models.IntegerField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category')),
                ('tags', models.ManyToManyField(blank=True, related_name='products', to='product.tag')),
            ],
        ),
    ]
