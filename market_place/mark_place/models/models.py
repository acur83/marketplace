# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from odoo.addons import decimal_precision as dp


class MarketServicesCatalog(models.Model):
    '''TODO DOCUMENT
    '''
    _name = 'market.services.catalog'
    _rec_name = 'custom_name'
    _description = 'Services Catalog'

    custom_name = fields.Char(required=True)
    users_ids = fields.One2many('res.users', 'services_catalog_id',
                                required=True)


class ResUsers(models.Model):
    ''' TODO DOCUMENT
    '''
    _inherit = 'res.users'

    services_catalog_id = fields.Many2one('services.catalog')
    related_partner_id = fields.Many2one('res.partner', copy=False)


class PurchaseRequisitionLine(models.Model):
    ''' TODO DOCUMENT
    '''
    _inherit = 'purchase.requisition.line'

    product_qty = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'))


class PurchaseRequisition(models.Model):
    ''' TODO DOCUMENT
    '''
    _inherit = 'purchase.requisition'

    services_catalogs_ids = fields.Many2many('market.services.catalog',
                                             required=True)
    requisition_code = fields.Char()


class PurchaseOrder(models.Model):
    ''' TODO DOCUMENT
    '''
    _inherit = 'purchase.order'

    note = fields.Char()
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

    def _ckeck_right_access(self):
        '''check if the logged user belong to purchase manager group
        purchase.
        '''
        purchase_manager = self.env.ref('purchase.group_purchase_manager')
        return self.env.user.id in [purchase_manager.users.id]

    @api.multi
    def button_confirm(self):
        '''Redefined for check if the user have the right to confirm a
        purchase.
        '''
        if self._ckeck_right_access():
            return super(PurchaseOrder, self).button_confirm()
        else:
            raise except_orm(
                "ACCESS ERROR",
                _("You have NOT ACCESS to confirm a Purchase Order."))
