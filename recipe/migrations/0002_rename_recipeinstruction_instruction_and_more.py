# Generated by Django 4.1.2 on 2022-11-01 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipeInstruction',
            new_name='Instruction',
        ),
        migrations.RenameField(
            model_name='cuisinetype',
            old_name='diet',
            new_name='cuisine_type',
        ),
        migrations.RenameField(
            model_name='diettype',
            old_name='diet',
            new_name='diet_type',
        ),
    ]