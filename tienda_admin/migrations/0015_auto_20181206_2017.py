# Generated by Django 2.0.8 on 2018-12-06 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda_admin', '0014_product_colour_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeOutcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(max_length=100)),
                ('update_date', models.DateTimeField(auto_now=True, max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('is_income', models.BooleanField(default=False)),
                ('is_outcome', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='colour',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]