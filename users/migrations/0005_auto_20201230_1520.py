# Generated by Django 3.1.4 on 2020-12-30 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201229_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feemaster',
            name='feehead',
            field=models.PositiveIntegerField(choices=[(1, 'Admission'), (2, 'First Year'), (3, 'Second Year'), (4, 'Third Year'), (5, 'clc')]),
        ),
        migrations.AlterField(
            model_name='studentfee',
            name='feehead',
            field=models.PositiveIntegerField(choices=[(1, 'Admission'), (2, 'First Year'), (3, 'Second Year'), (4, 'Third Year'), (5, 'clc')]),
        ),
        migrations.CreateModel(
            name='CLCFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.PositiveIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.courses')),
            ],
        ),
        migrations.AddConstraint(
            model_name='clcfee',
            constraint=models.UniqueConstraint(fields=('course', 'fee'), name='CLC Fee already exist'),
        ),
    ]