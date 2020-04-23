from odoo import api, models, fields, _

class ReportPurchase(models.Model):
    _name = "report.purchase"

    date_from = fields.Date(string='Date from', require=True)
    date_to = fields.Date(string='Date to', require=True)

    selection = fields.Selection(
        [
            ('rfq', 'RFQ'),
            ('purchase order', 'Purchase Order')
        ],
    )

    @api.multi
    def print_report(self):
        report = self.env['ir.actions.report'].search(
            [('report_name', '=', 'report_purchase.wizard_report_purchase'),
             ('report_type', '=', 'xlsx')], limit=1)
        return report.report_action(self)