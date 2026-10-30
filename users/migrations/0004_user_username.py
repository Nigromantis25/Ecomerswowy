from django.db import migrations, models
from django.utils.text import slugify
import django.contrib.auth.validators


def populate_usernames(apps, schema_editor):
    User = apps.get_model("users", "User")
    used_usernames = set()

    for user in User.objects.order_by("pk").iterator():
        base_username = slugify(user.email.partition("@")[0])[:150]
        if not base_username:
            base_username = f"user{user.pk}"

        username = base_username
        suffix = 1
        while username.casefold() in used_usernames:
            suffix_text = str(suffix)
            username = f"{base_username[:150 - len(suffix_text)]}{suffix_text}"
            suffix += 1

        user.username = username
        user.save(update_fields=["username"])
        used_usernames.add(username.casefold())


def clear_usernames(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.update(username=None)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.RunPython(populate_usernames, clear_usernames),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=150,
                unique=True,
                validators=[
                    django.contrib.auth.validators.UnicodeUsernameValidator()
                ],
            ),
        ),
    ]
