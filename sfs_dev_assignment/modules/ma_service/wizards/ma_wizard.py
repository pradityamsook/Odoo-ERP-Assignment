# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MAReportWizard(models.Model):
    _name = 'wizard.ma.report'


    company = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)
    partner = fields.Many2one('res.partner', string="Customer")
    sale_ref = fields.Many2one('sale.order', string="Project Name")
    site = fields.Many2one('ma.site', string="Site")
    status = fields.Many2one('ma.status', string="Status")

    def check_report(self):
        context = self._context
        data = {}
        data['form'] = {}
        data['form'].update(self.read(['company', 'partner', 'sale_ref','site', 'status'])[0])
        return self.env.ref('ma_service.action_ma_report_pdf').with_context(landscape=True).report_action(self,data=data)


