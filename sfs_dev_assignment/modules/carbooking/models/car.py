from odoo import fields, models, api

class Car(models.Model):
    _name = 'car.car'

    # Function for create name of car license.
    @api.one
    @api.depends('car_brand', 'register_no')
    def _get_name(self):
        if self.register_no and self.car_brand:
            self.name = self.car_brand + ' ' + self.register_no

    # Notebook group view
    name = fields.Char(compute=_get_name, store=True)
    register_no = fields.Char(string='หมายเลขทะเบียน', required=True)
    vehicle_type_id = fields.Many2one('car.type', 'Car type', required=True)
    car_brand = fields.Char(string='car brand', required=True)
    color = fields.Char(string='color', required=True)
    model_year = fields.Char(string='Model year', required=False)
    car_code = fields.Many2one('car.code', 'code', required=True)
    model = fields.Char(string='Model', required=True)
    body_no = fields.Char(string='เลขตัวรถ', required=True)
    date_of_register = fields.Datetime(string='วันที่จดทะเบียน', default=fields.Datetime.now(), required=True)

    # Engine page for views
    engine_brands = fields.Char(string='Engine brands', required=False)
    engine_no = fields.Char(string='เลขเครื่องยนต์', required=False)
    gas_no = fields.Char(string='เลขถังก๊าซ', required=False)
    fuel = fields.Char(string='Fuel', required=False)

    # From class BookingCar and read only.
    user_id = fields.Many2one('res.users', string='พนักงาน', default=lambda self: self.env.user,
                              store=False, readonly=True, index=True
    )

    # relationship fields
    booking_car_ids = fields.One2many('booking.car', 'car_id', string='Booking car', readonly=True)
    # booking_car_user_id = fields.Many2one('res.users', 'user_id', readonly=True, related='booking_car_ids.user_id')

