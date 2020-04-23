from odoo import fields, models, api
from odoo.exceptions import UserError, AccessError, ValidationError
from datetime import datetime
import random

class BookingCar(models.Model):
    _name = 'booking.car'
    # _rec_name = 'name'

    # @api.multi
    def draft_state(self):
        return self.write({'state': 'draft'})

    # @api.multi
    def to_approve_state(self):
        # for to_approve in self:
        #     to_approve.state = 'to_approve'
        return self.write({'state': 'to_approve'})

    # @api.multi
    def approve_state(self):
        # for approve in self:
        #     approve.state = 'approve'
        return self.write({'state': 'approve'})

    # @api.multi
    def finish_state(self):
        # for finish in self:
        #     finish.state = 'finish'
        return self.write({'state': 'finish'})

    # @api.multi
    def cancel_state(self):
        # for cancel in self:
        #     cancel.state = 'cancel
        return self.write({'state': 'cancel'})


    name = fields.Char(string='ชื่อหนังสือรถ', required=True, readonly=False,
                       states={'to_approve': [('readonly', True)],
                               'approve': [('readonly', True)],
                               'finish': [('readonly', True)]}
                       )
    user_id = fields.Many2one('res.users', string='พนักงาน', default=lambda self:self.env.user, store=True,
                              readonly=False, index=True,
                              states={'to_approve': [('readonly', True)],
                                      'approve': [('readonly', True)],
                                      'finish': [('readonly', True)]}
                              )
    phone = fields.Char(string='โทรศัพท์', required=True, readonly=False,
                        states={'to_approve': [('readonly', True)],
                                'approve': [('readonly', True)],
                                'finish': [('readonly', True)]}
                        )
    start_date = fields.Date(string='วันที่ออก', required=True, readonly=False,
                             states={'to_approve': [('readonly', True)],
                                     'approve': [('readonly', True)],
                                     'finish': [('readonly', True)]}
                             )
    end_date = fields.Date(string='วันที่สิ้นสุด', required=True, readonly=False,
                           states={'to_approve': [('readonly', True)],
                                   'approve': [('readonly', True)],
                                   'finish': [('readonly', True)]}
                           )
    total_days = fields.Integer(string='เป็นจำนวนวัน', readonly=False,
                                states={'to_approve': [('readonly', True)],
                                        'approve': [('readonly', True)],
                                        'finish': [('readonly', True)]}
                                )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To approve'),
        ('approve', 'Approve'),
        ('finish', 'Finish'),
        ('cancel', 'Cancel')
    ], string='state', copy=False, index=True, default='draft')

    #relation fields
    car_id = fields.Many2one('car.car', string='Car', required=True, readonly=False,
                             states={'to_approve': [('readonly', True)],
                                     'approve': [('readonly', True)],
                                     'finish': [('readonly', True)]}
                             )

    @api.multi
    @api.onchange('start_date', 'end_date', 'total_days')
    def _calculate_days(self):
        if self.start_date and self.end_date:
            print(self.start_date)
            _first = datetime.strptime(str(self.start_date), "%Y-%m-%d")
            print('--------------------------------------->', _first)
            _last = datetime.strptime(str(self.end_date), "%Y-%m-%d")
            print('--------------------------------------->', _last)
            _total = _last - _first
            self.total_days = abs(_total.days)
            print('--------------------------------------->', self.total_days)

    @api.model
    def create(self, values):
        _boolean_state = self.search([('state', 'in', ['to_approve', 'approve'])])
        print('1-------------------------------------->ค่าของหนังสือรถที่สร้างใหม่', values)
        print('2---------------------------------------> ค่าของเลขทะเบียนที่มีการของสำเร็จแล้ว', _boolean_state)

        _current_date = [] # store date form create new booking.
        if values:
            for i in values.get('start_date'):
                _current_date.append(i)

        _merge_date = (_current_date[0] + _current_date[1] + _current_date[2] + _current_date[3] + _current_date[5] +
                      _current_date[6] + _current_date[8] + _current_date[9]) # store string is not "-".
        # print(int(_merge_date))

        for i in _boolean_state:
            print('3-------------------------------------->', i.start_date)
            print('4--------------------------------------> ค่าของเลขทะเบียนที่มีการของสำเร็จแล้ว(จำนวนวัน)',
                  int(i.total_days))
            print('5-------------------------------------->', i.car_id)
            _int_date = int('{:{dfmt}}'.format(i.start_date, dfmt='%Y%m%d'))
            _int_total_days = int(i.total_days)
            for _date_travel_integer in range(_int_total_days):
                _int_date += _date_travel_integer
                print('id----------------------------->', values['car_id'])
                if _int_date == int(_merge_date):
                    raise ValidationError(('รถคันนี้ได้ทำการถูกจองแล้ว กรุณาเลือกวันที่จะจองใหม่'))
                else:
                    _int_date -= _date_travel_integer
                print(_int_date)

        return super(BookingCar, self).create(values)

    @api.onchange('phone')
    def auto_input_phone(self):
        if self.phone == False:
            self.phone = '0' + str(random.randrange(600000000, 999999999, 107))
