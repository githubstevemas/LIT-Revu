# Generated by Django 5.0.6 on 2024-06-05 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_review_ticket_remove_review_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]