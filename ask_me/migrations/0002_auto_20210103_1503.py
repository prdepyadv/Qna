# Generated by Django 3.0.5 on 2021-01-03 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask_me', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='Question',
            new_name='question_text',
        ),
    ]
