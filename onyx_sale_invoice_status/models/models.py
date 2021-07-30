# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID,_


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def set_invoiced(self):
        self.write({'invoice_status': 'invoiced'})
            
                