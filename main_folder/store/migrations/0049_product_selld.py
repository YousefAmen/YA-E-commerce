# Generated by Django 5.0.7 on 2024-10-15 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0048_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='selld',
            field=models.IntegerField(default=0),
        ),
    ]
