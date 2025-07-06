import os
import requests
from dotenv import load_dotenv

load_dotenv()  # charge .env à la racine du projet

class GeolocationService:
    """
    Service d’aide à la géolocalisation :
    • geocode_address      : adresse → (lat, lon)
    • reverse_geocode      : (lat, lon) → adresse
    • get_static_map       : miniature Google Static Maps
    • calculate_distance   : distance Haversine (km)
    """

    def __init__(self) -> None:
        self.mapbox_access_token = os.getenv("MAPBOX_ACCESS_TOKEN")
        self.google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

        if not self.mapbox_access_token:
            raise RuntimeError("MAPBOX_ACCESS_TOKEN manquant dans .env")
        if not self.google_maps_api_key:
            raise RuntimeError("GOOGLE_MAPS_API_KEY manquant dans .env")

    # ---------------------------------------------------------------------
    # 1) Adresse ➜ Coordonnées
    # ---------------------------------------------------------------------
    def geocode_address(self, address: str) -> dict | None:
        """Convertir une adresse texte en latitude / longitude (Mapbox)"""
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
        params = {"access_token": self.mapbox_access_token, "limit": 1}

        try:
            resp = requests.get(url, params=params, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            if data.get("features"):
                lon, lat = data["features"][0]["center"]
                return {"latitude": lat, "longitude": lon}
        except (requests.RequestException, ValueError) as exc:
            print(f"[Geocode] Erreur : {exc}")

        return None

    # ---------------------------------------------------------------------
    # 2) Coordonnées ➜ Adresse
    # ---------------------------------------------------------------------
    def reverse_geocode(self, latitude: float, longitude: float) -> str | None:
        """Convertir des coordonnées (lat, lon) en adresse littérale (Mapbox)"""
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{longitude},{latitude}.json"
        params = {"access_token": self.mapbox_access_token, "limit": 1}

        try:
            resp = requests.get(url, params=params, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            if data.get("features"):
                return data["features"][0]["place_name"]
        except (requests.RequestException, ValueError) as exc:
            print(f"[Reverse geocode] Erreur : {exc}")

        return None

    # ---------------------------------------------------------------------
    # 3) Carte statique Google Maps
    # ---------------------------------------------------------------------
    def get_static_map(
        self,
        latitude: float,
        longitude: float,
        width: int = 600,
        height: int = 400,
        zoom: int = 15,
    ) -> bytes | None:
        """Obtenir une image PNG de la zone (Google Static Maps)"""
        url = "https://maps.googleapis.com/maps/api/staticmap"
        params = {
            "center": f"{latitude},{longitude}",
            "zoom": zoom,
            "size": f"{width}x{height}",
            "markers": f"color:red|{latitude},{longitude}",
            "key": self.google_maps_api_key,
        }

        try:
            resp = requests.get(url, params=params, timeout=8)
            resp.raise_for_status()
            return resp.content
        except requests.RequestException as exc:
            print(f"[StaticMap] Erreur : {exc}")
            return None

    # ---------------------------------------------------------------------
    # 4) Distance Haversine
    # ---------------------------------------------------------------------
    @staticmethod
    def calculate_distance(
        lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """Distance « grand‑cercle » entre deux points (en km)"""
        from math import radians, sin, cos, sqrt, atan2

        R = 6_371.0  # Rayon moyen de la Terre, km
        lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return round(R * c, 3)  # km, arrondi à 1 m

# -------------------------------------------------------------------------
# Exemple d’usage (à retirer en prod)
# -------------------------------------------------------------------------
if __name__ == "__main__":
    geo = GeolocationService()
    print(geo.geocode_address("Tour Eiffel, Paris"))
    print(geo.reverse_geocode(48.8583701, 2.2922926))
    print(geo.calculate_distance(48.85837, 2.29448, 48.8566, 2.3522), "km")
