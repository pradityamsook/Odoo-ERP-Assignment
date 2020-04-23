# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
import datetime
import pytz
import io
from datetime import datetime, date, time, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT, date_utils
from odoo.exceptions import ValidationError, UserError, except_orm


def format_date_time(var_date):
    return str('{:{dfmt}}'.format(var_date, dfmt='%d/%m/%Y'))

def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def date_integer(date_time):
    return (10000 * date_time.year) + (100 * date_time.month) + (date_time.day)

class PartnerXlsx(models.AbstractModel):
    _name = 'report.sale_report.wizard_sale_report_total'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        # global variable
        now = datetime.now()
        _now = 'รายงาน ณ วันที่ ' + format_date_time(now)

        output = io.BytesIO()

        date_from = partners.date_from
        date_to = partners.date_to

        get_both_date = self.env['sale.order'].search([('create_date', '>=', date_from), ('create_date', '<=', date_to)])
        get_date_from = self.env['sale.order'].search([('create_date', '>=', date_from)])
        get_date_to = self.env['sale.order'].search([('create_date', '<=', date_to)])
        get_sale_order = self.env['sale.order'].search([])
        #get_company = self.env['sale.order'].search([])

        # format
        bold = workbook.add_format({'bold': True,
                                    'align':'center',
                                    'valign':'vcenter',
                                    'bg_color': 'red'})
        price_format = workbook.add_format({'num_format': '$#,##0.00'})

        # Report name
        sheet = workbook.add_worksheet('Sale report total')

        sheet.set_column('K:N', 12)
        sheet.set_row(0, 30)
        sheet.merge_range('K1:N1', _now, bold)

        sheet.set_column('A:N', 12)
        sheet.set_row(1, 30)
        sheet.set_row(2, 30)
        sheet.set_row(3, 30)

        date_format = workbook.add_format({'num_format': 'd mmm yyyy',
                                           'bold': True,
                                           'align': 'center',
                                           'valign': 'vcenter',
                                           'bg_color': 'red'})
        #sheet.merge_range('A1:N1', get_sale_order.partner_id, bold)
        sheet.merge_range('A2:N2', 'รายงานยอดขายของใบส่งขาย(Sale Order)', bold)
        # sheet.merge_range('A3:N3', 'จากวันที่ ' + str(date_from) + ' ถึง ' +
        #                   str(date_to), bold)
        if date_from == False and date_to == False:
            _date_from = self.env['sale.order'].search([], order = 'create_date asc', limit = 1)
            _date_to = self.env['sale.order'].search([], order = 'create_date desc', limit = 1)
            sheet.merge_range('A3:N3', 'จากวันที่ ' + format_date_time(_date_from.create_date.date()) + ' ถึง ' +
                              format_date_time(_date_to.create_date.date()), bold)
        elif date_from == False:
            _date_from_last = self.env['sale.order'].search([('create_date', '<=', date_to)], order='create_date asc',
                                                            limit=1)
            sheet.merge_range('A3:N3', 'จากวันที่ ' + format_date_time(_date_from_last.create_date.date()) + ' ถึง ' +
                              format_date_time(date_to), bold)
        elif date_to == False:
            _date_to_last = self.env['sale.order'].search([('create_date', '>=', date_from)], order='create_date desc',
                                                            limit=1)
            sheet.merge_range('A3:N3', 'จากวันที่ ' + format_date_time(date_from) + ' ถึง ' +
                              format_date_time(_date_to_last.create_date.date()), bold)
        else:
            sheet.merge_range('A3:N3', 'จากวันที่ ' + format_date_time(date_from) + ' ถึง ' +
                              format_date_time(date_to), bold)


        head_cell_format = workbook.add_format()
        head_cell_format.set_align('vcenter')
        sheet.set_row(5, 20)
        sheet.set_column('A:N', 20)
        sheet.write(5, 0, 'No.', bold)
        sheet.write(5, 1, 'สาขา', bold)
        sheet.write(5, 2, 'เลขที่ใบสั่งขาย', bold)
        sheet.write(5, 3, 'วันที่ใบสั่งขาย', bold)
        sheet.write(5, 4, 'ชื่อลูกค้า', bold)
        sheet.write(5, 5, 'ชื่อผู้ขาย', bold)
        sheet.write(5, 6, 'ชื่อสินค้า', bold)
        sheet.write(5, 7, 'รายละเอียด', bold)
        sheet.write(5, 8, 'จำนวน', bold)
        sheet.write(5, 9, 'มูลค่าก่อนภาษี', bold)
        sheet.write(5, 10, 'ภาษีมูลค่าเพิ่ม', bold)
        sheet.write(5, 11, 'มูลค่ารวม', bold)
        sheet.write(5, 12, 'สถานะ', bold)

        row = 6
        count = 1
        #
        # for get_in_sale_order in field:
        #     if date_from == True and date_to == True:
        #         for _date_range in date_range(date_from, date_to):
        #             print("_date_range----------->", _date_range)
        #             format_date_range = _date_range.strfmt('%Y-%m-%d')
        #             _format_date_range = datetime.strptime(str(format_date_range), '%Y-%m-%d')
        #             _create_date = datetime.strptime(str(get_in_sale_order.create_date.date()), '%Y-%m-%d')
        #             print(date_integer(format_date_range), date_integer(get_in_sale_order.create_date.date()))
        #             if date_integer(_format_date_range) == date_integer(_create_date):
        #                 print(get_in_sale_order.order_line)
        #                 for get_in_order_line in get_in_sale_order.order_line:
        #                     print(get_in_order_line.product_id.name, get_in_sale_order.name)
        #                     sheet.write(row, 0, count)
        #                     sheet.write(row, 1, get_in_sale_order.team_id.name)
        #                     sheet.write(row, 2, get_in_sale_order.name)
        #                     sheet.write(row, 3, format_date_time(get_in_sale_order.create_date.date()))
        #                     sheet.write(row, 4, get_in_sale_order.partner_id.name)
        #                     sheet.write(row, 5, get_in_sale_order.user_id.name)
        #                     sheet.write(row, 6, get_in_order_line.product_id.name)
        #                     sheet.write(row, 7, get_in_order_line.name)
        #                     sheet.write(row, 8, get_in_order_line.product_uom_qty)
        #                     sheet.write(row, 9, get_in_sale_order.amount_untaxed, price_format)
        #                     sheet.write(row, 10, get_in_sale_order.amount_tax, price_format)
        #                     sheet.write(row, 11, get_in_sale_order.amount_total, price_format)
        #                     sheet.write(row, 12, get_in_sale_order.state)
        #                     row += 1
        #                     count += 1
        #     elif date_from == True and date_to == False:
        #         if date_integer(get_in_sale_order.create_date.date()) >= date_integer(date_from):
        #             print(get_in_sale_order.order_line,)
        #             for get_in_order_line in get_in_sale_order.order_line:
        #                 print(get_in_order_line.product_id.name, get_in_sale_order.name)
        #                 sheet.write(row, 0, count)
        #                 sheet.write(row, 1, get_in_sale_order.team_id.name)
        #                 sheet.write(row, 2, get_in_sale_order.name)
        #                 sheet.write(row, 3, format_date_time(get_in_sale_order.create_date.date()))
        #                 sheet.write(row, 4, get_in_sale_order.partner_id.name)
        #                 sheet.write(row, 5, get_in_sale_order.user_id.name)
        #                 sheet.write(row, 6, get_in_order_line.product_id.name)
        #                 sheet.write(row, 7, get_in_order_line.name)
        #                 sheet.write(row, 8, get_in_order_line.product_uom_qty)
        #                 sheet.write(row, 9, get_in_sale_order.amount_untaxed, price_format)
        #                 sheet.write(row, 10, get_in_sale_order.amount_tax, price_format)
        #                 sheet.write(row, 11, get_in_sale_order.amount_total, price_format)
        #                 sheet.write(row, 12, get_in_sale_order.state)
        #                 row += 1
        #                 count += 1
        #     elif date_from == False and date_to == False:
        #         for get_in_order_line_all in get_in_sale_order.order_line:
        #             print(get_in_order_line_all.product_id.name, get_in_sale_order.name)
        #             print(date_integer(get_in_sale_order.create_date.date()))
        #             sheet.write(row, 0, count)
        #             sheet.write(row, 1, get_in_sale_order.team_id.name)
        #             sheet.write(row, 2, get_in_sale_order.name)
        #             sheet.write(row, 3, format_date_time(get_in_sale_order.create_date.date()))
        #             sheet.write(row, 4, get_in_sale_order.partner_id.name)
        #             sheet.write(row, 5, get_in_sale_order.user_id.name)
        #             sheet.write(row, 6, get_in_order_line_all.product_id.name)
        #             sheet.write(row, 7, get_in_order_line_all.name)
        #             sheet.write(row, 8, get_in_order_line_all.product_uom_qty)
        #             sheet.write(row, 9, get_in_sale_order.amount_untaxed, price_format)
        #             sheet.write(row, 10, get_in_sale_order.amount_tax, price_format)
        #             sheet.write(row, 11, get_in_sale_order.amount_total, price_format)
        #             sheet.write(row, 12, get_in_sale_order.state)
        #             row += 1
        #             count += 1

        if date_to == False:
            for get_in_sale_order in get_date_from:
                for get_in_order_line_all in get_in_sale_order.order_line:
                    sheet.write(row, 0, count)
                    sheet.write(row, 1, get_in_sale_order.team_id.name)
                    sheet.write(row, 2, get_in_sale_order.name)
                    sheet.write(row, 3, format_date_time(get_in_sale_order.create_date.date()))
                    sheet.write(row, 4, get_in_sale_order.partner_id.name)
                    sheet.write(row, 5, get_in_sale_order.user_id.name)
                    sheet.write(row, 6, get_in_order_line_all.product_id.name)
                    sheet.write(row, 7, get_in_order_line_all.name)
                    sheet.write(row, 8, get_in_order_line_all.product_uom_qty)
                    sheet.write(row, 9, get_in_sale_order.amount_untaxed, price_format)
                    sheet.write(row, 10, get_in_sale_order.amount_tax, price_format)
                    sheet.write(row, 11, get_in_sale_order.amount_total, price_format)
                    sheet.write(row, 12, get_in_sale_order.state)
                    row += 1
                    count += 1

        elif date_from == False:
            for get_in_sale_order in get_date_to:
                for get_in_order_line_all in get_in_sale_order.order_line:
                    sheet.write(row, 0, count)
                    sheet.write(row, 1, get_in_sale_order.team_id.name)
                    sheet.write(row, 2, get_in_sale_order.name)
                    sheet.write(row, 3, format_date_time(get_in_sale_order.create_date.date()))
                    sheet.write(row, 4, get_in_sale_order.partner_id.name)
                    sheet.write(row, 5, get_in_sale_order.user_id.name)
                    sheet.write(row, 6, get_in_order_line_all.product_id.name)
                    sheet.write(row, 7, get_in_order_line_all.name)
                    sheet.write(row, 8, get_in_order_line_all.product_uom_qty)
                    sheet.write(row, 9, get_in_sale_order.amount_untaxed, price_format)
                    sheet.write(row, 10, get_in_sale_order.amount_tax, price_format)
                    sheet.write(row, 11, get_in_sale_order.amount_total, price_format)
                    sheet.write(row, 12, get_in_sale_order.state)
                    row += 1
                    count += 1
        elif date_from and date_to:
            for get_in_sale_order in get_both_date:
                for get_in_order_line_all in get_in_sale_order.order_line:
                    sheet.write(row, 0, count)
                    sheet.write(row, 1, get_in_sale_order.team_id.name)
                    sheet.write(row, 2, get_in_sale_order.name)
                    sheet.write(row, 3, format_date_time(get_in_sale_order.create_date.date()))
                    sheet.write(row, 4, get_in_sale_order.partner_id.name)
                    sheet.write(row, 5, get_in_sale_order.user_id.name)
                    sheet.write(row, 6, get_in_order_line_all.product_id.name)
                    sheet.write(row, 7, get_in_order_line_all.name)
                    sheet.write(row, 8, get_in_order_line_all.product_uom_qty)
                    sheet.write(row, 9, get_in_sale_order.amount_untaxed, price_format)
                    sheet.write(row, 10, get_in_sale_order.amount_tax, price_format)
                    sheet.write(row, 11, get_in_sale_order.amount_total, price_format)
                    sheet.write(row, 12, get_in_sale_order.state)
                    row += 1
                    count += 1
        if date_to == False and date_from == False:
            for get_in_sale_order in get_sale_order:
                for get_in_order_line_all in get_in_sale_order.order_line:
                    sheet.write(row, 0, count)
                    sheet.write(row, 1, get_in_sale_order.team_id.name)
                    sheet.write(row, 2, get_in_sale_order.name)
                    sheet.write(row, 3, format_date_time(get_in_sale_order.create_date.date()))
                    sheet.write(row, 4, get_in_sale_order.partner_id.name)
                    sheet.write(row, 5, get_in_sale_order.user_id.name)
                    sheet.write(row, 6, get_in_order_line_all.product_id.name)
                    sheet.write(row, 7, get_in_order_line_all.name)
                    sheet.write(row, 8, get_in_order_line_all.product_uom_qty)
                    sheet.write(row, 9, get_in_sale_order.amount_untaxed, price_format)
                    sheet.write(row, 10, get_in_sale_order.amount_tax, price_format)
                    sheet.write(row, 11, get_in_sale_order.amount_total, price_format)
                    sheet.write(row, 12, get_in_sale_order.state)
                    row += 1
                    count += 1
