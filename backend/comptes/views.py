from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    InscriptionSerializer,
    UtilisateurSerializer,
    CustomTokenObtainPairSerializer,
)

Utilisateur = get_user_model()


# ───────────── POST /auth/register/ ─────────────
class InscriptionView(generics.CreateAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = InscriptionSerializer
    permission_classes = [AllowAny]


# ───────────── POST /auth/login/ ─────────────
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


# ───────────── GET /auth/me/ ─────────────
class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UtilisateurSerializer(request.user)
        return Response(serializer.data)


# Alias « MoiView » si tu l’utilisais ailleurs
MoiView = UserMeView
