# -*- coding: utf-8 -*-
import datetime
from odoo import api, models, _, fields


class ReportRender(models.AbstractModel):
    _name = 'report.ma_service.report_ma'

    @api.model
    def _get_report_values(self, docids, data):
        if data['form']['partner'] and data['form']['status'] and data['form']['sale_ref'] and data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('status', '=', data['form']['status'][0]), ('partner','=', data['form']['partner'][0]),
                                                   ('sale_ref', '>=', data['form']['sale_ref'][0]),
                                                   ('site', '<=', data['form']['site'][0])])
        elif data['form']['partner'] and not data['form']['status'] and data['form']['sale_ref'] and data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('partner','=', data['form']['partner'][0]),
                                                   ('sale_ref', '>=', data['form']['sale_ref'][0]),
                                                   ('site', '<=', data['form']['site'][0])])
        elif data['form']['partner'] and data['form']['status'] and not  data['form']['sale_ref'] and data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('partner','=', data['form']['partner'][0]),
                                                   ('status', '>=', data['form']['status'][0]),
                                                   ('site', '<=', data['form']['site'][0])])
        elif data['form']['partner'] and data['form']['status'] and data['form']['sale_ref'] and not data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('partner','=', data['form']['partner'][0]),
                                                   ('status', '>=', data['form']['status'][0]),
                                                   ('sale_ref', '<=', data['form']['sale_ref'][0])])
        elif not data['form']['partner'] and  data['form']['status'] and data['form']['sale_ref'] and  data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('site','=', data['form']['site'][0]),
                                                   ('status', '>=', data['form']['status'][0]),
                                                   ('sale_ref', '<=', data['form']['sale_ref'][0])])
        elif data['form']['partner'] and  data['form']['status'] and not data['form']['sale_ref'] and  not data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('partner','=', data['form']['partner'][0]),
                                                   ('status', '>=', data['form']['status'][0])])
        elif data['form']['partner'] and not  data['form']['status'] and  data['form']['sale_ref'] and  not data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('partner','=', data['form']['partner'][0]),
                                                   ('sale_ref', '>=', data['form']['sale_ref'][0])])
        elif data['form']['partner'] and not  data['form']['status'] and  not data['form']['sale_ref'] and  data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('partner','=', data['form']['partner'][0]),
                                                   ('site', '>=', data['form']['site'][0])])
        elif not data['form']['partner'] and data['form']['status'] and  not data['form']['sale_ref'] and  data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('status','=', data['form']['status'][0]),
                                                   ('site', '>=', data['form']['site'][0])])
        elif not data['form']['partner'] and data['form']['status'] and   data['form']['sale_ref'] and  not data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('status','=', data['form']['status'][0]),
                                                   ('sale_ref', '>=', data['form']['sale_ref'][0])])
        elif not data['form']['partner'] and  not data['form']['status'] and  data['form']['sale_ref'] and  data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('sale_ref','=', data['form']['sale_ref'][0]),
                                                   ('site', '>=', data['form']['site'][0])])
        elif data['form']['partner'] and  not data['form']['status'] and not  data['form']['sale_ref'] and not  data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('partner','=', data['form']['partner'][0])])
        elif not data['form']['partner'] and   data['form']['status'] and not  data['form']['sale_ref'] and not  data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('status','=', data['form']['status'][0])])
        elif not data['form']['partner'] and   not data['form']['status'] and not  data['form']['sale_ref'] and  data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('site','=', data['form']['site'][0])])
        elif not data['form']['partner'] and   not data['form']['status'] and data['form']['sale_ref'] and not  data['form']['site']:
            report_data = self.env['sale.ma_service'].search([('sale_ref','=', data['form']['sale_ref'][0])])
        elif not data['form']['partner'] and   not data['form']['status'] and not data['form']['sale_ref'] and not  data['form']['site']:
            report_data = self.env['sale.ma_service'].search([])

        return {
            'doc_ids': docids,
            'doc_model': 'sale.ma_service',
            'docs': report_data,
            'data': data
            }

