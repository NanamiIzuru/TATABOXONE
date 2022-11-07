# Generated by Django 4.0.4 on 2022-05-12 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_prettynum_alter_userinfo_age_alter_userinfo_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.CharField(max_length=32, verbose_name='av号')),
                ('title', models.TextField(verbose_name='视频标题')),
            ],
        ),
        migrations.AlterField(
            model_name='prettynum',
            name='mobile',
            field=models.CharField(max_length=11, verbose_name='手机号码'),
        ),
    ]
