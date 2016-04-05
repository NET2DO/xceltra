# -*- coding: utf-8 -*-

{
    'name': 'Xceltra',
    'version': '0.1',
    'author': 'Eng. Mostafa Mohammed',
    "sequence": 1,
    'category': 'Sales & Project Management ',
    'website': 'https://eg.linkedin.com/in/mostafa-mohammed-449a8786',
    'depends': ['base', 'report', 'sale', 'crm', 'project'],
    'data': ['data/opportunity_sequence.xml',
             'data/tast_reminder_cron.xml',
             'security/ir.model.access.csv',
             'views/crm_lead_view.xml',
             'views/product_view.xml',
             'views/project_task_view.xml',
             'views/sale_order_view.xml',
             ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
