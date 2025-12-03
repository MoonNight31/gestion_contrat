# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

# ========== CONTRAT (Alternance / Stage) ==========
class ContratContrat(models.Model):
    _name = 'contrat.contrat'
    _description = 'Contrat (Alternance / Stage)'
    _rec_name = 'display_name'

    date_started = fields.Date(string="Date de début", required=True)
    date_ended = fields.Date(string="Date de fin", required=True)
    
    type_contrat = fields.Selection([
        ('alternance', 'Alternance'),
        ('stage', 'Stage'),
    ], string="Type de contrat", required=True, default='alternance')
    
    # Relations : Étudiant, Entreprise, Tuteur
    personne_etudiant_id = fields.Many2one('school.personne', string="Étudiant", 
                                           domain=[('type_profil', '=', 'etudiant')], 
                                           required=True)
    entreprise_id = fields.Many2one('entreprise.entreprise', string="Entreprise d'accueil", required=True)
    personne_tuteur_id = fields.Many2one('school.personne', string="Tuteur en entreprise", 
                                         domain=[('type_profil', '=', 'salarie')],
                                         required=True)
    
    # Champs calculés et affichage
    display_name = fields.Char(string="Référence", compute='_compute_display_name', store=True)
    duree_jours = fields.Integer(string="Durée (jours)", compute='_compute_duree', store=True)
    formation_id = fields.Many2one('school.formation', string="Formation", 
                                   related='personne_etudiant_id.formation_id', 
                                   store=True, readonly=True)

    @api.depends('personne_etudiant_id', 'entreprise_id', 'type_contrat')
    def _compute_display_name(self):
        for record in self:
            if record.personne_etudiant_id and record.entreprise_id:
                record.display_name = f"{record.type_contrat.upper()} - {record.personne_etudiant_id.display_name} @ {record.entreprise_id.nom}"
            else:
                record.display_name = "Nouveau contrat"

    @api.depends('date_started', 'date_ended')
    def _compute_duree(self):
        for record in self:
            if record.date_started and record.date_ended:
                delta = record.date_ended - record.date_started
                record.duree_jours = delta.days
            else:
                record.duree_jours = 0

    @api.constrains('date_started', 'date_ended')
    def _check_dates(self):
        for record in self:
            if record.date_started and record.date_ended:
                if record.date_ended <= record.date_started:
                    raise ValidationError("La date de fin doit être postérieure à la date de début.")

    @api.constrains('personne_tuteur_id', 'entreprise_id')
    def _check_tuteur_entreprise(self):
        for record in self:
            if record.personne_tuteur_id and record.entreprise_id:
                if record.personne_tuteur_id.entreprise_id != record.entreprise_id:
                    raise ValidationError("Le tuteur doit être un salarié de l'entreprise d'accueil.")
