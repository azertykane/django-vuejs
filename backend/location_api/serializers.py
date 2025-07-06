from rest_framework import serializers
from .models import (
    Maison, Chambre, Contrat, Paiement, RendezVous, Media, Probleme
)

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"

class MaisonSerializer(serializers.ModelSerializer):
    chambres = serializers.SerializerMethodField()
    medias   = MediaSerializer(many=True, read_only=True)

    class Meta:
        model  = Maison
        fields = "__all__"

    def get_chambres(self, obj):
       return ChambreSerializer(obj.chambres.all(), many=True).data

class ChambreSerializer(serializers.ModelSerializer):
    maison_id = serializers.PrimaryKeyRelatedField(
        source='maison', queryset=Maison.objects.all(), write_only=True
    )
    medias = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Chambre
        fields = [
            'id', 'titre', 'description', 'taille', 'type', 'meublee',
            'salle_de_bain', 'prix', 'disponible', 'cree_le',
            'maison_id',  
            'medias'     
        ]






class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Paiement
        fields = "__all__"

class ContratSerializer(serializers.ModelSerializer):
    paiements = PaiementSerializer(many=True, read_only=True)

    class Meta:
        model  = Contrat
        fields = "__all__"

class RendezVousSerializer(serializers.ModelSerializer):
    locataire = serializers.SerializerMethodField()
    chambre = serializers.SerializerMethodField()

    class Meta:
        model = RendezVous
        fields = '__all__'
        read_only_fields = ['locataire', 'statut', 'cree_le']

    def get_locataire(self, obj):
        return {
            "id": obj.locataire.id,
            "nom": obj.locataire.nom,
            "email": obj.locataire.email,
        }

    def get_chambre(self, obj):
        return {
            "id": obj.chambre.id,
            "titre": obj.chambre.titre,
        }

    def validate(self, attrs):
        if self.context['request'].method == 'POST' and not attrs.get('date_heure'):
            from django.utils import timezone
            attrs['date_heure'] = timezone.now()
        return attrs



class ProblemeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Probleme
        fields = "__all__"
