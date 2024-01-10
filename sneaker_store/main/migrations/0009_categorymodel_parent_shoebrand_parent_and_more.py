# Generated by Django 5.0.1 on 2024-01-07 10:29

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_categorymodel_alter_shoegalleryimages_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.shoebrand'),
        ),
        migrations.AddField(
            model_name='shoebrand',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='main.shoebrand'),
        ),
        migrations.AddField(
            model_name='shoemodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.categorymodel'),
        ),
        migrations.AlterField(
            model_name='shoemodel',
            name='category',
            field=models.ForeignKey(blank=True, default='', max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='main.categorymodel'),
        ),
    ]
