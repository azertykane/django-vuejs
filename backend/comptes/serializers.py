from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

Utilisateur = get_user_model()


# ────────────────── Profil utilisateur ──────────────────
class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ("id", "email", "telephone", "cni", "role", "date_joined")


# ────────────────── Inscription (register) ──────────────────
class InscriptionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Utilisateur.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password], style={"input_type": "password"}
    )

    class Meta:
        model = Utilisateur
        fields = ("email", "password", "telephone", "cni", "role")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Utilisateur.objects.create_user(password=password, **validated_data)
        return user


# ────────────────── Login JWT custom ──────────────────
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Ajoute le rôle & l'email dans le token et renvoie aussi le rôle au login.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["role"] = self.user.role
        return data
