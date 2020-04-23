from odoo import fields, models, api

class CarCode(models.Model):
    _name = 'car.code'
    _rec_name = 'style_of_vehicle'
    # name = fields.Char(string='ชื่อ', required=True)
    code = fields.Char(string='รหัสลักษณะ', required=True)
    style_of_vehicle = fields.Char(string='ลักษณะรถ', required=True)
    vehicle_type_id = fields.Many2one('car.type', string='ประเภทรถ', required=True)