from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chathistory_is_flagged_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chathistory',
            name='model_used',
            field=models.CharField(
                default='groq',
                help_text='The AI model used for this chat',
                max_length=50,
                verbose_name='AI Model Used'
            ),
        ),
    ]