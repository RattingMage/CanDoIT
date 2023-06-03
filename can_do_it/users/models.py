from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class UserRoles(models.TextChoices):
    ADMIN = 'ADMIN', _("admin")
    EXECUTOR = 'EXECUTOR', _("executor")
    EMPLOYER = 'EMPLOYER', _("employer")


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role, phone, company, experience, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role, phone=phone, company=company, experience=experience)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, role=UserRoles.ADMIN, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            password=password
        )

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=128, blank=True)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    role = models.CharField(max_length=8, choices=UserRoles.choices)
    skills = models.ManyToManyField(Skill, blank=True)
    experience = models.IntegerField(default=0, blank=True)
    company = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role', 'phone', 'company', 'experience']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        if self.role == UserRoles.EXECUTOR or self.role == UserRoles.EMPLOYER:
            return True
        else:
            return False

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
