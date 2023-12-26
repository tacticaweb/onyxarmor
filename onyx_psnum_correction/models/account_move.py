# Copyright 2015-2021 Soluciones Opensource - Luis Miguel Var�n E
# Copyright 20121 Soluciones Opensource - Luis Miguel Var�n E
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    psnumber = fields.Integer(string='PSNUM')

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    psnumber = fields.Integer(string='PSNUM')

    
                    