# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError, ValidationError

class PromotionsPromotionsType(models.Model):
    _name = 'promotions.promotions.type'
    _description = 'Promotion Type'

    @api.one
    def draft_promotion_status_bar(self):
        return self.write({'state': 'draft'})

    def active_promotion_status_bar(self):
        for rec in self:
            rec.state = 'active'
        # return self.write({'state' : 'active'})

    def close_promotion_status_bar(self):
        for close in self:
            close.state = 'close'
        # return self.write({'state' : 'close'})

    # def _default_employee(self):
    #     # self.env['hr.employee'].search([('user_id', '=', self.env.user)])
    #     print('---------------',self.env.user)
    #     user_employee = self.env['hr.employee'].search([('user_id', '=', self.env.user)])
    #     print(user_employee)

    name = fields.Char(string = 'โปรโมชั่น', required = True)
    datetime_promotions_start = fields.Datetime(string = 'วันที่เริ่มต้นโปรโมชั่น', default = fields.Datetime.now(), required = True)
    datetime_promotions_end = fields.Datetime(string = 'วันที่สิ้นสุดโปรโมชั่น', required = True)


    user_id = fields.Many2one('res.users', string='พนักงาน', default=lambda self:self.env.user,#related=employee_id.user_id,
        store=False, readonly=True, index=True
    )
    # employee_id = fields.Many2one(
    #     'hr.employee', 'พนักงาน', help='Enter here the private of Employee.',
    #     required=True, default='_default_employee'
    # )
    promotions_type_line = fields.One2many(
        'promotions.type.line', 'promotions_type_id',
        string = 'รายละเอียด'
    )
    promotions_giveaway_lines = fields.One2many(
        'give.away.line', 'giveaway_lines', string = 'โปรโมชั่น'
    )
    detail = fields.Char(string = 'รายละเอียด')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('close', 'Closed')
    ], string='state', readonly=True, copy=False, index=True, default='draft')

    print()

    @api.model
    def create(self, values):
        print(values)
        _active = self.search([('state', '=', 'active')])

        print("1---------------------------->", _active)
        print("2---------------------------->", values)
        print("3---------------------------->", values.get('promotions_type_line'))
        print(values.get('promotions_giveaway_lines'))
        _product_list = []  # list store product ids only
        res = {}
        if values.get('promotions_type_line'):
            for i in values.get('promotions_type_line'):
                print("4---------------------------->", i[2]['product_id'])
                _product_list.append(i[2]['product_id'])
            print("5---------------------------->", _product_list)
            for promotions_type_id in _active:
                print("6---------------------------->", promotions_type_id.promotions_type_line)
                for promotions_type_line_id in promotions_type_id.promotions_type_line:
                    print("7---------------------------->", promotions_type_line_id.product_id)
                    print("9---------------------------->", promotions_type_line_id.product_id.id in _product_list)
                    if promotions_type_line_id.product_id.id in _product_list:
                        print("8---------------------------->", promotions_type_line_id.product_id.id)
                        raise ValidationError(_('มีสินค้าอยู่ในโปรโมชั่นอื่นแล้ว โปรดกดปุ่ม Discard'))
        if values.get('promotions_giveaway_lines'):
            for promotions_giveaway_lines_values in values.get('promotions_giveaway_lines'):
                print("8---------------------------->", promotions_giveaway_lines_values[2]['product_id'])
        r

    @api.multi
    def write(self, values):
        _product_list = []
        _res = {}
        _active = self.search([('state', '=', 'active')])

        print("1---------------------------->", _active)
        print("2---------------------------->", values)
        print("3---------------------------->", values.get('promotions_type_line'))
        print("4---------------------------->", values.get('promotions_giveaway_lines'))

        if values.get('promotions_type_line'):
            for i in values.get('promotions_type_line'):
                _product_list.append(i[2]['product_id'])

            print("5---------------------------->", _product_list)
            for promotions_type_id in _active:
                print(promotions_type_id.name)
                print("6---------------------------->", promotions_type_id.promotions_type_line)
                for promotions_type_line_id in promotions_type_id.promotions_type_line:
                    print("7---------------------------->", promotions_type_line_id.product_id)
                    print("8---------------------------->", promotions_type_line_id.product_id.name in _product_list)
                    if promotions_type_line_id.product_id.id in _product_list:
                        print("9---------------------------->", promotions_type_line_id.product_id.name)

                        raise ValidationError(_('มี %s อยู่ในโปรโมชั่นอื่นแล้ว'%promotions_type_line_id.product_id.name))

                        raise ValidationError(_('มีสินค้า '))


        return super(PromotionsPromotionsType, self).write(values)

    print()

class PromotionsTypeLine(models.Model):
    _name = 'promotions.type.line'

    product_id = fields.Many2one(
        'product.product', 'สินค้าที่ร่วมโปรโมชั่น', required=True
    )
    note = fields.Text('หมายเหตุ')
    promotions_type_id = fields.Many2one(
        'promotions.promotions.type', 'Parent type',
        index = True, ondelete = 'cascade', required = True
    )

class GiveAwayLine(models.Model):
    _name = 'give.away.line'

    def _get_default_product_id_uom_id(self):
        return self.env['uom.uom'].search([], limit = 1, order = 'id').id

    giveaway_lines = fields.Many2one(
        'promotions.promotions.type', 'ของแถม',
        required = True
    )
    product_id = fields.Many2one(
        'product.product', 'สินค้าที่ร่วมโปรโมชั่น', required=True
    )
    product_uom_id = fields.Many2one(
        'uom.uom', 'Product unit of measure',
        default = _get_default_product_id_uom_id,
        oldname = 'product_uom', required = True,
    )
    product_uom_qty = fields.Float(
        'จำนวน', default = 1.0,
        digits = dp.get_precision('Unit of measure'), required = True
    )
    notes = fields.Text('หมายเหตุ')
    name = fields.Char(string='Name', required=True)


# (0, 0, { values }) link to a new record that needs to be created with the given values dictionary
# (1, ID, { values }) update the linked record with id = ID (write *values* on it)
# (2, ID) remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
# (3, ID) cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
# (4, ID) link to existing record with id = ID (adds a relationship)
# (5) unlink all (like using (3,ID) for all linked records)
# (6, 0, [IDs]) replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)