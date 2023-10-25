from odoo import fields,models,api,_
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_round
from collections import Counter
from datetime import datetime


class mrp_product_produce(models.TransientModel):
    _inherit='mrp.product.produce'
    
    @api.model
    def default_get(self, fields):
        res = super(mrp_product_produce, self).default_get(fields)
        mo_id=self.env['mrp.production'].browse(self._context['active_id'])
        res.update({'lot_id':mo_id.mrp_lot_id.id})
        return res
