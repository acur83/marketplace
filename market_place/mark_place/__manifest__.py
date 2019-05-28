# -*- coding: utf-8 -*-
# Created by Simple IT Develop Team.
{
    'name': "mark_place",
    'version': "1.0",
    'summary': "Market Place",
    'author': "Simple IT Develop Team.",
    'description': """
    Market Place Module
    """,
    'depends': ['base', 'purchase', 'purchase_requisition'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/external_services.xml',
        'views/purchase_requisition_inherit_view.xml',
        'views/purchase_order_inh.xml',
        'views/res_users_inh_form_view.xml',
        'views/custom_menus.xml',

    ],
    'demo': [
    ],
    'auto_install': False,
}
