from odoo import models, fields, api, _
from . import promotions as pro

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # sale_giveaway_lines = pro.GiveAwayLine.giveaway_lines
    # sale_product_id = pro.GiveAwayLine.product_id
    # sale_product_uom_id = pro.GiveAwayLine.product_uom_id
    # sale_product_uom_qty = pro.GiveAwayLine.product_uom_qty
    # sale_notes= pro.GiveAwayLine.notes

    @api.multi
    def action_show(self):
        #action_tree = self.env.ref('promotions.promotions_action_tree_id').id
        return {
            'name': _('เช็คของแถม'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'give.away.line',
            'view_id': False,
            'res_id' : False,
            'context' : False,
            'type': 'ir.actions.act_window',
        }

    def action_giveaway(self):
        return {
            'name': _('เช็คของแถม'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'give.away.line',
            'view_id': False,
            'res_id': False,
            'context': False,
            'type': 'ir.actions.act_window',
        }

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_promotion_id = fields.Many2one('product.product', string='ของแถม')