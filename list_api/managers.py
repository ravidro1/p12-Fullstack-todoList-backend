from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email')
        if not password:
            raise ValueError('Users must have an password')
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email')
        if not password:
            raise ValueError('Users must have an password')
        user = self.create_user(email,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
