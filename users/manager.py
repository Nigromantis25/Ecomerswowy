from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        if not extra_fields.get("username"):
            base_username = slugify(email.partition("@")[0])[:150] or "user"
            username = base_username
            suffix = 1
            while self.filter(username__iexact=username).exists():
                suffix_text = str(suffix)
                username = f"{base_username[:150 - len(suffix_text)]}{suffix_text}"
                suffix += 1
            extra_fields["username"] = username
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
