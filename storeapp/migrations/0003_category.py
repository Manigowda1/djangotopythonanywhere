# Generated by Django 4.0.3 on 2022-04-02 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0002_product_image_alter_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]