import requests
import os
from dotenv import load_dotenv

load_dotenv()

class NotificationService:
    def __init__(self):
        self.endpoint = os.getenv("NOTIFICATION_ENDPOINT", "http://localhost:8001/api/notifications/")

    def envoyer_notification(self, utilisateur_id, message, type="info"):
        payload = {
            "utilisateur_id": utilisateur_id,
            "message": message,
            "type": type,
        }

        try:
            response = requests.post(self.endpoint, json=payload)
            return response.status_code == 201
        except Exception as e:
            print(f"Erreur envoi notification: {e}")
            return False
