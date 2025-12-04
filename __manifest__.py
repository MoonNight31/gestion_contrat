# -*- coding: utf-8 -*-
{
    'name': "Gestion Contrat",
    'icon': '/gestion_contrat/static/description/icon.png',
    'web_icon': 'gestion_contrat/static/description/icon.png',
    'summary': "Gestion des contrats d'alternance et de stage",
    'description': """
        Module de gestion des contrats
        ================================
        * Contrats d'alternance
        * Contrats de stage
        * Lien entre étudiants, entreprises et tuteurs
    """,
    'author': "MoonDev",
    'version': '1.0',
    'category': 'Human Resources',
    'depends': ['base', 'gestion_ecole', 'gestion_entreprise'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
