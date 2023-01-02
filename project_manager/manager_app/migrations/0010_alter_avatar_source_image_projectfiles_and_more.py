# Generated by Django 4.1.3 on 2023-01-02 16:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import manager_app.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0009_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='source_image',
            field=models.ImageField(upload_to='avatars/', verbose_name='Obraz żródłowy'),
        ),
        migrations.CreateModel(
            name='ProjectFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='AttachmentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('file_name', models.CharField(blank=True, max_length=120)),
                ('file_extension', models.CharField(blank=True, max_length=12)),
                ('source_file', models.FileField(upload_to='project_files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('txt', 'docx', 'doc', 'pdf', 'png', 'jpg', 'gif', 'psd', 'ppt', 'xls')), manager_app.models.max_file_size_validator])),
                ('project_files_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager_app.projectfiles')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
