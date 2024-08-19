# Generated by Django 4.2.14 on 2024-07-28 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses', models.ManyToManyField(related_name='university', to='timetable.course')),
                ('instructors', models.ManyToManyField(related_name='university', to='timetable.instructor')),
                ('time_slots', models.ManyToManyField(related_name='university', to='timetable.timeslot')),
            ],
        ),
    ]
