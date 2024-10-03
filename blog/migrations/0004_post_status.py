# Generated by Django 5.1.1 on 2024-10-03 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('PU', 'Published'), ('DR', 'Draft')], default='DR', max_length=2),
        ),
    ]
