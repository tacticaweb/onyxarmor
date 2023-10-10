# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID,_


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    sale_origin = fields.Char("Sale Order Origin", compute='_compute_origin')
    
    def _compute_origin(self):
        for reg in self:
            mo = self.env['mrp.production'].search([('name','=',reg.origin)])
            if mo:
                reg.sale_origin = mo.origin 
            else:
                reg.sale_origin = reg.origin
                