# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from odoo.addons import decimal_precision as dp


class ExternalServices(models.Model):
    '''TODO DOCUMENT
    '''
    _name = 'external.services'
    _rec_name = 'service_name'
    _description = 'Catálogo de Servicios'

    service_name = fields.Char(required=True)
    users_ids = fields.Many2many('res.users', required=True)


class ResUsers(models.Model):
    ''' TODO DOCUMENT
    '''
    _inherit = 'res.users'

    related_partner_id = fields.Many2one('res.partner', copy=False,
                                         required=True)


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

    external_services_ids = fields.Many2many('external.services',
                                             required=True)
    requisition_code = fields.Char()
    total_amount = fields.Float(compute='_get_total_amount', store=True)

    @api.depends('line_ids')
    def _get_total_amount(self):
        '''Find the partner related with the login user.

        '''
        for record in self:
            total = sum(line.product_qty * line.price_unit
                        for line in record.line_ids)
            record.total_amount = total

    # @api.model
    # def create(self, vals):
    #     ''' TODO: DOCUMENT
    #     '''
    #     if self.total_amount == 0:
    #         raise except_orm("VALUE ERROR",
    #                          _("The Total Amount could not be 0.\
    #                          Please check your products lines values."))
    #     return super(PurchaseRequisition,self).create(vals)


class PurchaseOrderLine(models.Model):
    ''' TODO DOCUMENT
    '''
    _inherit = 'purchase.order.line'

    user_prod_qty = fields.Float(related='product_qty',
                                 groups="mark_place.group_lititator_user,\
                                 mark_place.group_lititator_admin",
                                 readonly=True, store=True)

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
    initial_amount = fields.Float(related='requisition_id.total_amount',
                                  store=True)

    @api.onchange('order_line')
    def _compute_partner(self):
        '''Find the partner related with the login user.

        '''
        for pur in self:
            if pur.env.user.related_partner_id:
                pur.computed_partner_id = pur.env.user.related_partner_id.id
                pur.partner_id = pur.env.user.related_partner_id.id
                pur.currency_id = pur.env.user.related_partner_id.currency_id

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
        return self.env.user.id in [u.id for u in purchase_manager.users]

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
                _("Usted no tiene PERMISO para confirmar una Orden de\
                Compra. Contacte con su Administrador."))
