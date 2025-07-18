# Generated by Django 5.2.3 on 2025-06-24 21:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chambre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('taille', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('simple', 'Chambre simple'), ('appartement', 'Appartement'), ('maison', 'Maison complète')], max_length=50)),
                ('meublee', models.BooleanField(default=False)),
                ('salle_de_bain', models.BooleanField(default=False)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disponible', models.BooleanField(default=True)),
                ('cree_le', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('montant_caution', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mois_caution', models.PositiveSmallIntegerField()),
                ('description', models.TextField(blank=True)),
                ('mode_paiement', models.CharField(choices=[('virement', 'Virement'), ('cash', 'Cash'), ('mobile_money', 'Mobile money')], max_length=50)),
                ('periodicite', models.CharField(choices=[('journalier', 'Journalier'), ('hebdomadaire', 'Hebdomadaire'), ('mensuel', 'Mensuel')], default='mensuel', max_length=20)),
                ('statut', models.CharField(choices=[('actif', 'Actif'), ('resilie', 'Résilié')], default='actif', max_length=20)),
                ('cree_le', models.DateTimeField(auto_now_add=True)),
                ('chambre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrats', to='location_api.chambre')),
                ('locataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Maison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('description', models.TextField(blank=True)),
                ('cree_le', models.DateTimeField(auto_now_add=True)),
                ('proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maisons', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chambre',
            name='maison',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chambres', to='location_api.maison'),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to='medias/')),
                ('type', models.CharField(choices=[('photo', 'Photo'), ('video', 'Vidéo')], max_length=10)),
                ('description', models.TextField(blank=True)),
                ('cree_le', models.DateTimeField(auto_now_add=True)),
                ('chambre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='location_api.chambre')),
            ],
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('statut', models.CharField(choices=[('paye', 'Payé'), ('impaye', 'Impayé')], max_length=20)),
                ('date_echeance', models.DateField()),
                ('date_paiement', models.DateTimeField(blank=True, null=True)),
                ('cree_le', models.DateTimeField(auto_now_add=True)),
                ('contrat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paiements', to='location_api.contrat')),
            ],
        ),
        migrations.CreateModel(
            name='Probleme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('plomberie', 'Plomberie'), ('electricite', 'Électricité'), ('autre', 'Autre')], max_length=20)),
                ('responsable', models.CharField(choices=[('locataire', 'Locataire'), ('proprietaire', 'Propriétaire')], max_length=20)),
                ('resolu', models.BooleanField(default=False)),
                ('cree_le', models.DateTimeField(auto_now_add=True)),
                ('contrat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problemes', to='location_api.contrat')),
                ('signale_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RendezVous',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_heure', models.DateTimeField()),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('confirme', 'Confirmé'), ('annule', 'Annulé')], default='en_attente', max_length=20)),
                ('cree_le', models.DateTimeField(auto_now_add=True)),
                ('chambre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rendezvous', to='location_api.chambre')),
                ('locataire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rendezvous', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
