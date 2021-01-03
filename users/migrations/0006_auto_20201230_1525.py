# Generated by Django 3.1.4 on 2020-12-30 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201230_1520'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='clcfee',
            name='CLC Fee already exist',
        ),
        migrations.AddField(
            model_name='clcfee',
            name='fee_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Normal Fee'), (2, 'Tatkal Fee')], default=1),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='clcfee',
            constraint=models.UniqueConstraint(fields=('course', 'fee_type'), name='CLC Fee already exist'),
        ),
    ]
