# Generated by Django 5.0.6 on 2024-08-04 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('size', models.CharField(choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large')], max_length=50)),
                ('image', models.ImageField(upload_to='food_images/')),
            ],
        ),
    ]
