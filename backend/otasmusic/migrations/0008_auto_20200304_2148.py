# Generated by Django 2.2.9 on 2020-03-04 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otasmusic', '0007_auto_20200114_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='slug',
            field=models.SlugField(choices=[('accoustic-guitar', 'accoustic guitar'), ('bass', 'bass'), ('backing-vocal', 'backing vocal'), ('camera', 'camera'), ('drums-track', 'drums track'), ('drums', 'drums'), ('electric-guitar', 'electric guitar'), ('keyboard', 'keyboard'), ('keyboard-track', 'keyboard track'), ('lead-vocal', 'lead vocal'), ('mastering', 'mastering'), ('metallophone', 'metallophone'), ('mix', 'mix'), ('mouth-organ', 'mouth organ'), ('recording', 'recording'), ('saxophone', 'saxophone'), ('trombone', 'trombone'), ('trumpet', 'trumpet'), ('video', 'video')], unique=True),
        ),
    ]
