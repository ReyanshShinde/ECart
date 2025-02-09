# Generated by Django 5.0.6 on 2024-07-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pimage',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Mobile'), (2, 'Shoes'), (3, 'cloth')], verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='product name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pdetails',
            field=models.CharField(max_length=100, verbose_name='product details'),
        ),
    ]
