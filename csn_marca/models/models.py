from odoo import models, fields

class MrpMarca(models.Model):
    _inherit = 'mrp.marca'
    
    csn = fields.Char(string='CSN')
