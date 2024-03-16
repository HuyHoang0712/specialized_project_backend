from django.db import migrations, models
from django.contrib.postgres.operations import UnaccentExtension
class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_issue_status_alter_order_status_and_more'),
    ]

    operations = [
        UnaccentExtension()
    ]