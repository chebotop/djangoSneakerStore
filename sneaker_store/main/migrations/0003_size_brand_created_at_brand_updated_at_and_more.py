# Generated by Django 4.2.4 on 2023-11-19 13:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_shoemodel_size_delete_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_value', models.CharField(max_length=20)),
                ('size_gender', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='brand',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brand',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name='shoemodel',
            name='size',
        ),
        migrations.AddField(
            model_name='shoemodel',
            name='size',
            field=models.ManyToManyField(to='main.size'),
        ),
    ]
