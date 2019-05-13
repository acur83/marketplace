# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MarketServicesCatalog(models.Model):
    '''TODO DOCUMENT
    '''
    _name = 'market.services.catalog'
    _rec_name = 'custom_name'
    _description = 'Services Catalog'

    custom_name = fields.Char(required=True)
    users_ids = fields.One2many('res.users', 'services_catalog_id',
                                required=True)
    purchase_requisition_id = fields.Many2one('purchase.requisition')


class ResUsers(models.Model):
    ''' TODO DOCUMENT
    '''
    _inherit = 'res.users'

    services_catalog_id = fields.Many2one('services.catalog')
    related_partner_id = fields.Many2one('res.partner')


class PurchaseRequisition(models.Model):
    ''' TODO DOCUMENT
    '''
    _inherit = 'purchase.requisition'

    services_catalogs_ids = fields.One2many('market.services.catalog',
                                            'purchase_requisition_id',
                                            required=True)
    requisition_code = fields.Char()


class PurchaseOrder(models.Model):
    ''' TODO DOCUMENT
    '''
    _inherit = 'purchase.order'

    requisition_code_p = fields.Char()
    related_partner_id_p = fields.Many2one('res.partner')

    computed_partner_id = fields.Many2one('res.partner', readonly=True,
                                          compute='_compute_partner',
                                          store=True)
    employee_evaluation = fields.Text(related='computed_partner_id.comment',
                                      readonly=True, store=True)

    @api.onchange('order_line')
    def _compute_partner(self):
        '''Find the partner related with the login user.

        '''
        for record in self:
            if record.env.user.related_partner_id:
                record.computed_partner_id = record.env.user.related_partner_id.id
                record.partner_id = record.env.user.related_partner_id.id
                record.currency_id = record.env.user.related_partner_id.currency_id

    @api.model
    def create(self, vals):
        '''TODO:DOCUMENT
        '''
        vals['computed_partner_id'] = self.env.user.related_partner_id.id
        return super(PurchaseOrder, self).create(vals)
