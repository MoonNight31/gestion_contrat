# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

# ========== EXTENSION DE RES.PARTNER ==========
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Relations inverses pour les contrats (ajoutées par le module gestion_contrat)
    contrat_etudiant_ids = fields.One2many('contrat.contrat', 'personne_etudiant_id', 
                                           string="Contrats (en tant qu'étudiant)")
    contrat_tuteur_ids = fields.One2many('contrat.contrat', 'personne_tuteur_id', 
                                         string="Contrats (en tant que tuteur)")
    contrat_entreprise_ids = fields.One2many('contrat.contrat', 'entreprise_id', 
                                            string="Contrats")
    contrat_count = fields.Integer(string="Nombre de contrats", compute='_compute_contrat_count', store=True)

    @api.depends('contrat_entreprise_ids')
    def _compute_contrat_count(self):
        for record in self:
            if record.is_company:
                record.contrat_count = len(record.contrat_entreprise_ids)
            else:
                record.contrat_count = 0


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
    personne_etudiant_id = fields.Many2one('res.partner', string="Étudiant", 
                                           domain=[('type_profil', '=', 'etudiant'), ('is_company', '=', False)], 
                                           required=True)
    entreprise_id = fields.Many2one('res.partner', string="Entreprise d'accueil", 
                                    domain=[('is_company', '=', True)],
                                    required=True)
    personne_tuteur_id = fields.Many2one('res.partner', string="Tuteur en entreprise", 
                                         domain=[('type_profil', '=', 'salarie'), ('is_company', '=', False)],
                                         required=True)
    
    # Champs calculés et affichage
    display_name = fields.Char(string="Référence", compute='_compute_display_name', store=True)
    duree_jours = fields.Integer(string="Durée (jours)", compute='_compute_duree', store=True)
    formation_id = fields.Many2one('school.formation', string="Formation", 
                                   compute='_compute_formation_id', 
                                   store=True, readonly=True)

    @api.depends('personne_etudiant_id')
    def _compute_formation_id(self):
        for record in self:
            if record.personne_etudiant_id and record.personne_etudiant_id.formation_id:
                record.formation_id = record.personne_etudiant_id.formation_id.id
            else:
                record.formation_id = False

    @api.depends('personne_etudiant_id', 'entreprise_id', 'type_contrat')
    def _compute_display_name(self):
        for record in self:
            if record.personne_etudiant_id and record.entreprise_id and record.type_contrat:
                type_label = dict(record._fields['type_contrat'].selection).get(record.type_contrat, '')
                record.display_name = f"{type_label.upper()} - {record.personne_etudiant_id.name} @ {record.entreprise_id.name}"
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
                if record.personne_tuteur_id.employer_partner_id != record.entreprise_id:
                    raise ValidationError("Le tuteur doit être un salarié de l'entreprise d'accueil.")
