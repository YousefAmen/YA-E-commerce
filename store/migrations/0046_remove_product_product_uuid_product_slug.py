# Generated by Django 5.0.7 on 2024-10-04 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0045_alter_product_product_uuid'),
    ]

    operations = [
      
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default=''),
        ),
    ]
