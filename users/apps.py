from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_admin(sender, **kwargs):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user, _ = User.objects.get_or_create(
        email="ithancito05@gmail.com",
        defaults={
            "name": "Admin Usuario",
            "phone": "0000000000",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    user.name = user.name or "Admin Usuario"
    user.phone = user.phone or "0000000000"
    user.is_staff = True
    user.is_superuser = True
    user.set_password("12345678")
    user.save(update_fields=["name", "phone", "is_staff", "is_superuser", "password"])


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        post_migrate.connect(create_default_admin, sender=self)
