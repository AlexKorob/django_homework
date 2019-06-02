# Generated by Django 2.1.5 on 2019-02-07 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20190205_1835'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestrunAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=120)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='testrun_answer', to='questions.Question')),
            ],
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='question',
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='answer',
        ),
        migrations.AddField(
            model_name='testrunanswer',
            name='testrun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Testrun'),
        ),
        migrations.AddField(
            model_name='testrun',
            name='answer',
            field=models.ManyToManyField(related_name='testruns', through='questions.TestrunAnswer', to='questions.Question'),
        ),
    ]
