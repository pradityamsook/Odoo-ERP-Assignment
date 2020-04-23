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
    _name = 'report.report_purchase.wizard_report_purchase'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        # global variable
        now = datetime.now()
        _now = 'รายงาน ณ วันที่ ' + format_date_time(now)

        date_from = partners.date_from
        date_to = partners.date_to
        selection = partners.selection

        purchase_both_date = self.env['purchase.order'].search(
            [
                ('create_date', '>=', date_from),
                ('create_date', '<=', date_to),
                ('state', 'in', ['purchase', 'done'])
            ],
            order='create_date asc'
        )
        purchase_date_from = self.env['purchase.order'].search(
            [
                ('create_date', '>=', date_from),
                ('state', 'in', ['purchase', 'done'])
            ],
            order='create_date asc'
        )
        purchase_date_to = self.env['purchase.order'].search(
            [
                ('create_date', '<=', date_to),
                ('state', 'in', ['purchase', 'done'])
            ],
            order='create_date asc'
        )
        purchase_sale_order = self.env['purchase.order'].search(
            [
                ('state', 'in', ['purchase', 'done'])
            ],
            order='create_date asc'
        )

        RFQ_both_date = self.env['purchase.order'].search(
            [
                ('create_date', '>=', date_from),
                ('create_date', '<=', date_to),
                ('state', 'in', ['draft', 'to approve'])
            ],
            order='create_date asc'
        )
        RFQ_date_from = self.env['purchase.order'].search(
            [
                ('create_date', '>=', date_from),
                ('state', 'in', ['draft', 'to approve'])
            ],
            order='create_date asc'
        )
        RFQ_date_to = self.env['purchase.order'].search(
            [
                ('create_date', '<=', date_to),
                ('state', 'in', ['draft', 'to approve'])
            ],
            order='create_date asc'
        )
        RFQ_sale_order = self.env['purchase.order'].search(
            [
                ('state', 'in', ['draft', 'to approve'])
            ],
            order='create_date asc'
        )

        all_purchase_order = self.env['purchase.order'].search(
            [

            ],
            order='create_date asc'
        )

        all_purchase_order_date_from = self.env['purchase.order'].search(
            [
                ('create_date', '>=', date_from)
            ],
            order='create_date asc'
        )

        all_purchase_order_date_to = self.env['purchase.order'].search(
            [
                ('create_date', '<=', date_to)
            ],
            order='create_date asc'
        )

        all_purchase_order_both_date = self.env['purchase.order'].search(
            [
                ('create_date', '>=', date_from),
                ('create_date', '<=', date_to)
            ],
            order='create_date asc'
        )

        company = self.env['purchase.order'].search(
            [
            ]
        )
        company_name = ''
        for company_ in company:
            print(company_.company_id.name)
            company_name = company_.company_id.name
        # format
        bold = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': True,
            'border_color': '#000000'
        })
        border = workbook.add_format({
            'border': True,
            'border_color': '#000000'
        })
        date_format = workbook.add_format({
            'num_format': 'd mmm yyyy',
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': 'red'
        })
        price_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': True,
            'border_color': '#000000'
        })

        # compute


        # Report name
        sheet = workbook.add_worksheet('Report purchase period')
        sheet.set_column('K:M', 20)
        sheet.set_row(0, 12)
        sheet.merge_range('K1:M1', _now, bold)
        sheet.set_column('A:M', 20)
        sheet.set_row(1, 12)
        sheet.set_row(2, 12)
        sheet.set_row(3, 12)
        sheet.merge_range('A2:M2', company_name, bold)
        sheet.merge_range('A3:M3', 'รายงานการจัดซื้อวัตถุดิบ (Purchases Order)', bold)

        if date_from == False and date_to == False:
            _date_from = self.env['purchase.order'].search(
                [],
                order='create_date asc', limit=1
            )
            _date_to = self.env['purchase.order'].search(
                [],
                order='create_date desc', limit=1
            )
            sheet.merge_range(
                'A4:M4',
                'จากวันที่ ' + format_date_time(_date_from.create_date.date()) + ' ถึง ' + format_date_time(_date_to.create_date.date()),
                bold
            )
        elif date_from == False:
            _date_from_last = self.env['purchase.order'].search(
                [
                    ('create_date', '<=', date_to)
                ],
                order='create_date asc',
                limit=1
            )
            sheet.merge_range(
                'A4:M4',
                'จากวันที่ ' + format_date_time(_date_from_last.create_date.date()) + ' ถึง ' + format_date_time(date_to),
                bold
            )
        elif date_to == False:
            _date_to_last = self.env['purchase.order'].search(
                [
                    ('create_date', '>=', date_from)
                ],
                order='create_date desc',
                limit=1
            )
            sheet.merge_range(
                'A4:M4',
                'จากวันที่ ' + format_date_time(date_from) + ' ถึง ' + format_date_time(_date_to_last.create_date.date()),
                bold
            )
        else:
            sheet.merge_range(
                'A4:M4',
                'จากวันที่ ' + format_date_time(date_from) + ' ถึง ' + format_date_time(date_to),
                bold
            )


        head_cell_format = workbook.add_format()
        head_cell_format.set_align('vcenter')
        sheet.set_row(5, 20)
        sheet.set_column('A:M', 20)
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
        sum_amount_untaxed = 0
        sum_amount_tax = 0
        sum_amount_total = 0
        sum_product_oum_qty = 0
        if selection == 'purchase order':
            if date_to == False and date_from == False:
                for get_in_purchase_order in purchase_sale_order:
                    for get_in_order_line_all in get_in_purchase_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_purchase_order.company_id.name, border)
                        sheet.write(row, 2, get_in_purchase_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_purchase_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_purchase_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_purchase_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_purchase_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_purchase_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_purchase_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_purchase_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_purchase_order.amount_tax
                        sum_amount_total += get_in_purchase_order.amount_total
                        sum_amount_untaxed += get_in_purchase_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty

                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)

            elif date_to == False:
                for get_in_purchase_order in purchase_date_from:
                    for get_in_order_line_all in get_in_purchase_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_purchase_order.company_id.name, border)
                        sheet.write(row, 2, get_in_purchase_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_purchase_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_purchase_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_purchase_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_purchase_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_purchase_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_purchase_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_purchase_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_purchase_order.amount_tax
                        sum_amount_total += get_in_purchase_order.amount_total
                        sum_amount_untaxed += get_in_purchase_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)

            elif date_from == False:
                for get_in_purchase_order in purchase_date_to:
                    for get_in_order_line_all in get_in_purchase_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_purchase_order.company_id.name, border)
                        sheet.write(row, 2, get_in_purchase_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_purchase_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_purchase_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_purchase_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_purchase_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_purchase_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_purchase_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_purchase_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_purchase_order.amount_tax
                        sum_amount_total += get_in_purchase_order.amount_total
                        sum_amount_untaxed += get_in_purchase_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)

            elif date_from and date_to:
                for get_in_purchase_order in purchase_both_date:
                    for get_in_order_line_all in get_in_purchase_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_purchase_order.company_id.name, border)
                        sheet.write(row, 2, get_in_purchase_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_purchase_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_purchase_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_purchase_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_purchase_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_purchase_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_purchase_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_purchase_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_purchase_order.amount_tax
                        sum_amount_total += get_in_purchase_order.amount_total
                        sum_amount_untaxed += get_in_purchase_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)




        elif selection == 'rfq':
            if date_to == False and date_from == False:
                for get_in_RFQ_order in RFQ_sale_order:
                    for get_in_order_line_all in get_in_RFQ_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_RFQ_order.company_id.name, border)
                        sheet.write(row, 2, get_in_RFQ_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_RFQ_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_RFQ_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_RFQ_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_RFQ_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_RFQ_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_RFQ_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_RFQ_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_RFQ_order.amount_tax
                        sum_amount_total += get_in_RFQ_order.amount_total
                        sum_amount_untaxed += get_in_RFQ_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)

            elif date_to == False:
                for get_in_RFQ_order in RFQ_date_from:
                    for get_in_order_line_all in get_in_RFQ_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_RFQ_order.company_id.name, border)
                        sheet.write(row, 2, get_in_RFQ_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_RFQ_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_RFQ_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_RFQ_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_RFQ_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_RFQ_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_RFQ_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_RFQ_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_RFQ_order.amount_tax
                        sum_amount_total += get_in_RFQ_order.amount_total
                        sum_amount_untaxed += get_in_RFQ_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)

            elif date_from == False:
                for get_in_RFQ_order in RFQ_date_to:
                    for get_in_order_line_all in get_in_RFQ_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_RFQ_order.company_id.name, border)
                        sheet.write(row, 2, get_in_RFQ_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_RFQ_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_RFQ_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_RFQ_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_RFQ_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_RFQ_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_RFQ_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_RFQ_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_RFQ_order.amount_tax
                        sum_amount_total += get_in_RFQ_order.amount_total
                        sum_amount_untaxed += get_in_RFQ_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row + 1, 1, 'Total', border)
                sheet.merge_range(row, 3, row + 1, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)

            elif date_from and date_to:
                for get_in_RFQ_order in RFQ_both_date:
                    for get_in_order_line_all in get_in_RFQ_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_RFQ_order.company_id.name, border)
                        sheet.write(row, 2, get_in_RFQ_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_RFQ_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_RFQ_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_RFQ_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_RFQ_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_RFQ_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_RFQ_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_RFQ_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_RFQ_order.amount_tax
                        sum_amount_total += get_in_RFQ_order.amount_total
                        sum_amount_untaxed += get_in_RFQ_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)



        elif selection == False:
            if date_to == False and date_from == False:
                for get_in_RFQ_order in all_purchase_order:
                    for get_in_order_line_all in get_in_RFQ_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_RFQ_order.company_id.name, border)
                        sheet.write(row, 2, get_in_RFQ_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_RFQ_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_RFQ_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_RFQ_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_RFQ_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_RFQ_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_RFQ_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_RFQ_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_RFQ_order.amount_tax
                        sum_amount_total += get_in_RFQ_order.amount_total
                        sum_amount_untaxed += get_in_RFQ_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)

            elif date_to == False:
                for get_in_RFQ_order in all_purchase_order_date_from:
                    for get_in_order_line_all in get_in_RFQ_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_RFQ_order.company_id.name, border)
                        sheet.write(row, 2, get_in_RFQ_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_RFQ_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_RFQ_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_RFQ_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_RFQ_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_RFQ_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_RFQ_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_RFQ_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_RFQ_order.amount_tax
                        sum_amount_total += get_in_RFQ_order.amount_total
                        sum_amount_untaxed += get_in_RFQ_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)

            elif date_from == False:
                for get_in_RFQ_order in all_purchase_order_date_to:
                    for get_in_order_line_all in get_in_RFQ_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_RFQ_order.company_id.name, border)
                        sheet.write(row, 2, get_in_RFQ_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_RFQ_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_RFQ_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_RFQ_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_RFQ_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_RFQ_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_RFQ_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_RFQ_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_RFQ_order.amount_tax
                        sum_amount_total += get_in_RFQ_order.amount_total
                        sum_amount_untaxed += get_in_RFQ_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)

            elif date_from and date_to:
                for get_in_RFQ_order in all_purchase_order_both_date:
                    for get_in_order_line_all in get_in_RFQ_order.order_line:
                        sheet.write(row, 0, count, border)
                        sheet.write(row, 1, get_in_RFQ_order.company_id.name, border)
                        sheet.write(row, 2, get_in_RFQ_order.name, border)
                        sheet.write(row, 3, format_date_time(get_in_RFQ_order.create_date.date()), border)
                        sheet.write(row, 4, get_in_RFQ_order.partner_id.name, border)
                        sheet.write(row, 5, get_in_RFQ_order.user_id.name, border)
                        sheet.write(row, 6, get_in_order_line_all.product_id.name, border)
                        sheet.write(row, 7, get_in_order_line_all.name, border)
                        sheet.write(row, 8, get_in_order_line_all.product_uom_qty, border)
                        sheet.write(row, 9, get_in_RFQ_order.amount_untaxed, price_format)
                        sheet.write(row, 10, get_in_RFQ_order.amount_tax, price_format)
                        sheet.write(row, 11, get_in_RFQ_order.amount_total, price_format)
                        sheet.write(row, 12, get_in_RFQ_order.state, border)
                        row += 1
                        count += 1
                        sum_amount_tax += get_in_RFQ_order.amount_tax
                        sum_amount_total += get_in_RFQ_order.amount_total
                        sum_amount_untaxed += get_in_RFQ_order.amount_untaxed
                        sum_product_oum_qty += get_in_order_line_all.product_uom_qty
                sheet.merge_range(row, 0, row, 1, 'Total', border)
                sheet.merge_range(row, 3, row, 7, '', border)
                sheet.write(row, 2, str(count - 1) + ' รายการ', border)
                sheet.write(row, 10, sum_amount_tax, price_format)
                sheet.write(row, 11, sum_amount_total, price_format)
                sheet.write(row, 9, sum_amount_untaxed, price_format)
                sheet.write(row, 8, sum_product_oum_qty, price_format)
                sheet.write(row, 12, '', border)
