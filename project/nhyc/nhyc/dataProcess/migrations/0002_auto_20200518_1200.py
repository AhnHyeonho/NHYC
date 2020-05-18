# Generated by Django 3.0.5 on 2020-05-18 03:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataProcess', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='memberInfo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dataProcess.MemberInfo'),
        ),
        migrations.AlterField(
            model_name='memberinfo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]