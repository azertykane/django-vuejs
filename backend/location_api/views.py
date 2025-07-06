from django.conf import settings
from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializers import RendezVousSerializer

from .models import (
    Maison, Chambre, Contrat, Paiement,
    RendezVous, Media, Probleme
)
from .serializers import (
    MaisonSerializer, ChambreSerializer, ContratSerializer,
    PaiementSerializer, RendezVousSerializer,
    MediaSerializer, ProblemeSerializer
)

class IsProprietaireOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Méthodes SAFE (GET, HEAD, OPTIONS) : OK pour tous
        if request.method in permissions.SAFE_METHODS:
            return True

        # Maison → obj.proprietaire
        # Chambre → obj.maison.proprietaire
        proprietaire = getattr(obj, "proprietaire", None) or getattr(obj, "maison", None).proprietaire
        return proprietaire == request.user


class MaisonViewSet(viewsets.ModelViewSet):
    queryset = Maison.objects.none()
    serializer_class = MaisonSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Maison.objects.filter(proprietaire=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        latitude = data.get("latitude")
        longitude = data.get("longitude")
        adresse = data.get("adresse")

        # Si adresse absente mais coords présentes, on tente de la récupérer automatiquement
        if not adresse and latitude and longitude:
            geo = GeolocationService()
            adresse = geo.reverse_geocode(latitude, longitude)
            if adresse:
                data["adresse"] = adresse
            else:
                return Response(
                    {"detail": "Impossible de géolocaliser l'adresse."},
                    status=400
                )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        maison = serializer.save(proprietaire=request.user)

        # Gestion des fichiers image
        files = request.FILES.getlist("images")
        if len(files) > 3:
            return Response({"detail": "Maximum 3 images autorisées."}, status=400)

        for f in files:
            Media.objects.create(maison=maison, fichier=f, type="photo")

        return Response(
            MaisonSerializer(maison).data,
            status=201,
            headers=self.get_success_headers(serializer.data)
        )



class ChambreViewSet(viewsets.ModelViewSet):
   
    queryset = Chambre.objects.select_related("maison", "maison__proprietaire").all()
    serializer_class = ChambreSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["titre", "description", "type"]
    ordering_fields = ["prix", "taille"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        maison_id = self.request.query_params.get("maison_id")

        if maison_id:
            qs = qs.filter(maison_id=maison_id)

        if user.role == "proprietaire" and not user.is_superuser:
            qs = qs.filter(maison__proprietaire=user)
        elif user.role == "locataire":
            qs = qs.filter(disponible=True)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chambre = serializer.save()

        # Gérer les images transmises
        files = request.FILES.getlist("images")
        if len(files) > 3:
            return Response(
                {"detail": "Vous pouvez envoyer un maximum de 3 images."},
                status=status.HTTP_400_BAD_REQUEST
            )

        for f in files:
            Media.objects.create(chambre=chambre, fichier=f, type="photo")

        return Response(
            self.get_serializer(chambre).data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )


class ContratViewSet(viewsets.ModelViewSet):
    """
    • Propriétaire : contrats de ses chambres
    • Locataire    : ses propres contrats
    """
    queryset = Contrat.objects.select_related(
        "locataire", "chambre", "chambre__maison", "chambre__maison__proprietaire"
    ).all()
    serializer_class = ContratSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == "proprietaire" and not user.is_superuser:
            qs = qs.filter(chambre__maison__proprietaire=user)
        elif user.role == "locataire":
            qs = qs.filter(locataire=user)
        return qs
    @action(detail=True, methods=["post"])
    def accepter(self, request, pk=None):
        contrat = self.get_object()
        if contrat.locataire != request.user:
            return Response({"detail": "Non autorisé"}, status=403)
        contrat.statut = "accepte"
        contrat.save()
        return Response({"status": "accepté"}, status=200)

    @action(detail=True, methods=["post"])
    def refuser(self, request, pk=None):
        contrat = self.get_object()
        if contrat.locataire != request.user:
            return Response({"detail": "Non autorisé"}, status=403)
        contrat.statut = "refuse"
        contrat.save()
        return Response({"status": "refusé"}, status=200)


class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.select_related(
        "contrat", "contrat__chambre", "contrat__locataire"
    ).all()
    serializer_class = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == "proprietaire" and not user.is_superuser:
            qs = qs.filter(contrat__chambre__maison__proprietaire=user)
        elif user.role == "locataire":
            qs = qs.filter(contrat__locataire=user)
        return qs


class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.select_related("chambre", "locataire", "chambre__maison", "chambre__maison__proprietaire")
    serializer_class = RendezVousSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'locataire':
            return qs.filter(locataire=user)
        elif user.role == 'proprietaire':
            return qs.filter(chambre__maison__proprietaire=user)
        return qs.none()

    def perform_create(self, serializer):
        serializer.save(locataire=self.request.user)

    @action(detail=True, methods=['post'])
    def confirmer(self, request, pk=None):
        rdv = self.get_object()
        if rdv.chambre.maison.proprietaire != request.user:
            return Response({"detail": "Non autorisé"}, status=403)
        rdv.statut = "confirme"
        rdv.save()
        return Response({"status": "confirmé"})

    @action(detail=True, methods=['post'])
    def envoyer_contrat(self, request, pk=None):
        rdv = self.get_object()
        user = request.user

        if rdv.chambre.maison.proprietaire != user:
            return Response({"detail": "Non autorisé"}, status=403)

    # Vérifie si un contrat existe déjà
        if Contrat.objects.filter(
            locataire=rdv.locataire,
            chambre=rdv.chambre,
            statut__in=["actif"]
        ).exists():
            return Response({"detail": "Contrat déjà existant pour ce locataire et cette chambre."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Récupère les données du POST
        data = request.data

        try:
            mois_caution = int(data.get('mois_caution', 1))
            montant_caution = float(data.get('montant_caution')) if data.get('montant_caution') else rdv.chambre.prix * mois_caution
        except ValueError:
            return Response({"detail": "Valeur invalide pour mois_caution ou montant_caution"},
                        status=status.HTTP_400_BAD_REQUEST)

        # Création du contrat
        contrat = Contrat.objects.create(
            locataire=rdv.locataire,
            chambre=rdv.chambre,
            date_debut=data.get('date_debut'),
            date_fin=data.get('date_fin'),
            mois_caution=mois_caution,
            montant_caution=montant_caution,
            mode_paiement=data.get('mode_paiement', 'mobile_money'),
            periodicite=data.get('periodicite', 'mensuel'),
            statut='propose',
            description=data.get('description', '')
        )

        serializer = ContratSerializer(contrat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.select_related("chambre", "chambre__maison").all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes    = [MultiPartParser, FormParser]  # Permet upload de fichiers

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == "proprietaire" and not user.is_superuser:
            qs = qs.filter(chambre__maison__proprietaire=user)
        elif user.role == "locataire":
            qs = qs.filter(chambre__disponible=True)
        return qs


class ProblemeViewSet(viewsets.ModelViewSet):
    queryset = Probleme.objects.select_related(
        "contrat", "contrat__locataire", "contrat__chambre"
    ).all()
    serializer_class = ProblemeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Le champ signale_par est rempli automatiquement
        serializer.save(signale_par=self.request.user)
