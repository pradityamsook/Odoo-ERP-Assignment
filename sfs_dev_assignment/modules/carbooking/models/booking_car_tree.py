from odoo import api, models, fields

class BookingCarTree(models.Model):
    _inherit = 'booking.car'

    booking_car_name = fields.Many2one('booking.car', 'name')