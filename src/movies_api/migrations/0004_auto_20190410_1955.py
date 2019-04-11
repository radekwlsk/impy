# Generated by Django 2.2 on 2019-04-10 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_api', '0003_auto_20190410_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='country',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_rating',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='metascore',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='released',
            field=models.DateField(null=True),
        ),
    ]
