# Generated by Django 3.1.1 on 2021-07-05 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TextChoiceAttemptAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
                ('attempt', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_choice_answer', to='tasks.attempt')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('check_on_submit', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('text', models.TextField()),
                ('attempts_max', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('textQuestion', 'textQuestion'), ('choiceQuestion', 'choiceQuestion'), ('orderQuestion', 'orderQuestion')], max_length=16)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='OrderAttemptAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=64)),
                ('attempt', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_answer', to='tasks.attempt')),
            ],
        ),
        migrations.AddField(
            model_name='attempt',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='tasks.question'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_num', models.IntegerField()),
                ('text', models.CharField(max_length=64)),
                ('is_true', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tasks.question')),
            ],
        ),
    ]
