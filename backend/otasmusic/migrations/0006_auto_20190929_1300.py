# Generated by Django 2.2.1 on 2019-09-29 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otasmusic', '0005_remove_record_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='slug',
            field=models.SlugField(choices=[('accoustic-guitar', 'accoustic guitar'), ('bass', 'bass'), ('backing-vocal', 'backing vocal'), ('drums-track', 'drums track'), ('drums', 'drums'), ('electric-guitar', 'electric guitar'), ('keyboard', 'keyboard'), ('keyboard-track', 'keyboard track'), ('lead-vocal', 'lead vocal'), ('mastering', 'mastering'), ('metallophone', 'metallophone'), ('mix', 'mix'), ('mouth-organ', 'mouth organ'), ('recording', 'recording'), ('saxophone', 'saxophone'), ('trombone', 'trombone'), ('video', 'video')], unique=True),
        ),
    ]
