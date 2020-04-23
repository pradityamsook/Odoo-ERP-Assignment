from odoo import fields, models, api

class CarType(models.Model):
    _name = 'car.type'
    _rec_name = 'vehicle_type_name'

    code = fields.Char(string='รหัสประเภท', required=True)
    vehicle_type_name = fields.Char(string='ประเภทรถ', required=True, index=True)