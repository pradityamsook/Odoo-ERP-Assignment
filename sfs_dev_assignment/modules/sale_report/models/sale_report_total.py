from odoo import api, models, fields

class SaleReportTotal(models.Model):
    _name = "sale.report.total"

    date_from = fields.Date(string='Date from', require=True)
    date_to = fields.Date(string='Date to', require=True)
    # test = fields.Selection([
    #     ('', 'RFQ'),
    #     ('test01', 'Purchase Order')
    # ], require=True)

    @api.multi
    def print_report_total(self):
        report = self.env['ir.actions.report'].search(
            [('report_name', '=', 'sale_report.wizard_sale_report_total'),
             ('report_type', '=', 'xlsx')], limit=1)
        return report.report_action(self)