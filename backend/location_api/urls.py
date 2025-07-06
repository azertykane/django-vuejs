from rest_framework import routers
from django.urls import path, include
from .views import (
    MaisonViewSet, ChambreViewSet, ContratViewSet, PaiementViewSet,
    RendezVousViewSet, MediaViewSet, ProblemeViewSet
)

router = routers.DefaultRouter()
router.register(r"maisons", MaisonViewSet)
router.register(r"chambres", ChambreViewSet)
router.register(r"contrats", ContratViewSet)
router.register(r"paiements", PaiementViewSet)
router.register(r"rendezvous", RendezVousViewSet)
router.register(r"medias", MediaViewSet)
router.register(r"problemes", ProblemeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
