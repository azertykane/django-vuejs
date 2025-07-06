from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email requis')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(unique=True)
    nom         = models.CharField(max_length=100, blank=True)
    telephone   = models.CharField(max_length=20, blank=True, null=True)  # ✅ Ajouté
    cni         = models.CharField(max_length=20, blank=True, null=True)  # ✅ Ajouté
    role        = models.CharField(
        max_length=30,
        choices=[
            ('locataire', 'Locataire'),
            ('proprietaire', 'Propriétaire'),
        ],
        default='locataire'
    )
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)  # ✅ Ajouté

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UtilisateurManager()

    def __str__(self):
        return self.email
