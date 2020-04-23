# -*- coding: utf-8 -*-

from datetime import datetime
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _
#
# class SaleInherit(models.Model):
#     _inherit = 'sale.order'
#
#     state = fields.Selection([
#         ('draft', 'Quotation'),
#         ('sent', 'Quotation Sent'),
#         ('sale', 'Sales Order'),
#         ('installation', 'Installation'),
#         ('handover', 'Handover'),
#         ('done', 'Locked'),
#         ('cancel', 'Cancelled'),
#     ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
#         default='draft')
#
#     def action_installation(self):
#         for data in self:
#             data.write({'state': 'installation'})
#
#     def action_hand_over(self):
#         for data in self:
#             data.write({'state': 'handover'})

class MA(models.Model):
    _name = 'ma.service'

    ma_service = fields.One2many('sale.ma_service', 'ma_ref', string="Service")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)
    name = fields.Char(readonly=True, select=True, copy=False, default='New')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('installation', 'Installation'),
            ('handover', 'Handover'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        readonly=True,
        copy=False,
        index=True,
        track_visibility='onchange',
        track_sequence=3,
        default='draft'
    )

    def action_installation(self):
        for data in self:
            data.write({'state': 'installation'})

    def action_hand_over(self):
        for data in self:
            data.write({'state': 'handover'})

    def action_done(self):
        for data in self:
            data.write({'state': 'done'})

    def action_cancel(self):
        for data in self:
            data.write({'state': 'cancel'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('ma.service') or 'New'
        result = super(MA, self).create(vals)
        return result


class MAService(models.Model):
    _name = 'sale.ma_service'

    partner = fields.Many2one('res.partner', string="Customer")
    contract_no = fields.Char(string="Contract No.",  readonly=True, select=True, copy=False, default='New')
    ma_source = fields.Many2one('ma.project_source', string="MA Source")
    product = fields.Char(string="Product List")
    sn = fields.Char(string="S/N")
    vendor_type = fields.Many2one('ma.vendor_type', string="Vendor Type")
    site = fields.Many2one('ma.site', string="Site")
    vendor_start_date = fields.Date(string="Vendor Period From")
    vendor_end_date = fields.Date(string="Vendor Period To")
    customer_start_date = fields.Date(string="Customer Period From")
    customer_end_date = fields.Date(string="Customer Period To")
    ma_end = fields.Char(string="MA Before End", compute="get_end")
    status = fields.Many2one('ma.status', string="Status")
    sale_ref = fields.Many2one('sale.order', string="Project Name")
    ma_ref = fields.Many2one('ma.service')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id)

    @api.constrains('vendor_start_date', 'vendor_end_date', 'customer_start_date', 'customer_end_date')
    def check_dates(self):
        for data in self:
            if data.vendor_start_date > data.vendor_end_date:
                raise ValidationError(_('Vendor start date cannot be greater than vendor end date'))
            if data.customer_start_date > data.customer_end_date:
                raise ValidationError(_('Customer start date cannot be greater than customer end date'))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['contract_no'] = self.env['ir.sequence'].next_by_code('sale.ma_service') or 'New'
        result = super(MAService, self).create(vals)
        return result

    def get_end(self):
        for data in self:
            today = datetime.today()
            # d1 = datetime.strptime(str(today), '%Y-%m-%d %H %M')
            if data.customer_end_date:
                d2 = datetime.strptime(str(data.customer_end_date), '%Y-%m-%d')
                data.ma_end = (d2 - today).days


class MASource(models.Model):
    _name = 'ma.project_source'
    name = fields.Char(string="Name")


class MAVendorType(models.Model):
    _name = 'ma.vendor_type'
    name = fields.Char(string="Name")


class MASite(models.Model):
    _name = 'ma.site'
    name = fields.Char(string="Name")


class MAStatus(models.Model):
    _name = 'ma.status'
    name = fields.Char(string="Name")