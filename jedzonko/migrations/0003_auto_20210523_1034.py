# Generated by Django 3.2 on 2021-05-23 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0002_auto_20210521_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayname',
            name='name',
            field=models.TextField(choices=[('Monday', 'MONDAY'), ('Tuesday', 'TUESDAY'), ('Wednesday', 'WEDNESDAY'), ('Thursday', 'THURSDAY'), ('Friday', 'FRIDAY'), ('Saturday', 'SATURDAY'), ('Sunday', 'SUNDAY')], max_length=16),
        ),
        migrations.AlterField(
            model_name='plan',
            name='description',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='dish_description',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='recipeplan',
            name='meal_name',
            field=models.TextField(max_length=255),
        ),
    ]
