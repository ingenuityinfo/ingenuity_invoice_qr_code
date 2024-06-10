# -*- coding: utf-8 -*-
#############################################################################
#
#    Ingenuity Info
#
#    Copyright (C) 2023-TODAY Ingenuity Info(<https://ingenuityinfo.in>)
#    Author: Ingenuity Info(<https://ingenuityinfo.in>)
#
#
#############################################################################
from odoo import models, fields, api
from odoo.http import request
import qrcode
import base64
from io import BytesIO

def generate_qr_code(value):
    qr = qrcode.QRCode(
             version=1,
             error_correction=qrcode.constants.ERROR_CORRECT_L,
             box_size=20,
             border=4)
    qr.add_data(value)
    qr.make(fit=True)
    img = qr.make_image()
    temp = BytesIO()
    img.save(temp, format="PNG")
    qr_img = base64.b64encode(temp.getvalue())
    return qr_img



class AccountMove(models.Model):
    _inherit = 'account.move'

    qr_image = fields.Binary("QR Code", compute='_generate_qr_code')
    qr_in_report = fields.Boolean('Display QRCode in Report?')

    def _generate_qr_code(self):
        self.qr_image = None
        for order in self:
            supplier_name = self.company_id.name
            vat = str(self.company_id.vat)
            vat_total = str(self.amount_tax)
            date = str(self.invoice_date)

            total = ''.join([self.currency_id.name, str(self.amount_total)])
            lf = '\t'
            invoice = lf.join(
                ['Seller name:', supplier_name, 'Vat Registration Number:', vat, 'Date:', date, 'Total with VAT:',
                 total, 'VAT total:', vat_total])
            order.qr_image = generate_qr_code(invoice)
