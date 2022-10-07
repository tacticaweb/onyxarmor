# Copyright 2015-2021 Soluciones Opensource - Luis Miguel Var�n E
# Copyright 20121 Soluciones Opensource - Luis Miguel Var�n E
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models

class ReturnReason(models.Model):
    
    _name = "return.reason"

    name = fields.Char("Reason of return")


class AccountMove(models.Model):
    
    """Add some fields related to commissions"""

    _inherit = "account.move"
    
    return_reason = fields.Many2one('return.reason', 'Reason of Return')
    
class SaleOrder(models.Model):
    """Add some fields related to commissions"""

    _inherit = "sale.order"
    
    with_return = fields.Boolean("Sale with Return")
    
    def order_with_return(self):
        pedidos = self.env['sale.order'].search([('state','=','sale')])
        for order in pedidos:
            for invoice in order.invoice_ids:
                if invoice.move_type =='out_refund':
                     order.with_return = True




                    