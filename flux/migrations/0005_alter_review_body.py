# Generated by Django 5.0.6 on 2024-06-12 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux', '0004_delete_photo_rename_book_ticket_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, max_length=8192),
        ),
    ]
