# Generated by Django 4.0.4 on 2022-05-19 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_transfer_leagues'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchresult',
            name='league_link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='result_league', to='home.league'),
        ),
    ]