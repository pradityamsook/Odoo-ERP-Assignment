# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
#from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # name = fields.Char(string='Name')

    @api.multi
    def action_kpi_report(self):
        return {
                'name': _('เช็คของแถม'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'view_id': False,
                'res_id' : False,
                'context' : False,
                'type': 'ir.actions.act_window',
        }


