# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class MrpGo(models.Model):
    _name = 'mrp.go'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    
    name = fields.Char(string='Nombre', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('mrp.go.seq'))
    line_ids = fields.One2many('mrp.go.line', 'go_id', readonly=False, string='Go Lines')
    mo_ids = fields.One2many('mrp.production', 'go_id', domain=[('state','in',('confirmed','progress','to_close'))], string='MO')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('closed', 'Closed'),
            ('processed', 'Processed'),
            ('finish', 'Finished'),
        ],
        string='State', required=True,
        default='draft')
    
    def action_go_close(self):
        return self.write({'state': 'closed'})
    
    def action_go_read_consuption(self):
        for mo in self.mo_ids:
            for mp in mo.move_raw_ids:
                domain = [('product_id', '=', mp.product_id.id),('go_id', '=', self.id)]
                line = self.line_ids.search(domain)
                if line:
                    line.planned_consume += mp.product_uom_qty
                    line.manufacture_qty += mo.product_qty
                else:
                    dict = {
                        'product_id': mp.product_id.id,
                        'manufacture_qty': mo.product_qty,
                        'planned_consume': mp.product_uom_qty,
                        'go_id': self.id,
                    }
                    self.line_ids.create(dict)
        return self.write({'state': 'processed'})
    
    def action_go_real_consuption(self):
        for line in self.line_ids:
            product = line.product_id
            real_consume = line.real_consume / line.manufacture_qty
            if real_consume > 0:
                for mo in self.mo_ids:
                    domain = [('raw_material_production_id', '=', mo.id),('product_id', '=', product.id)]
                    move = self.env['stock.move'].search(domain)
                    print ("move: ", move)
                    consume = real_consume * mo.product_qty
                    print ("consume: ", consume)
                    move.write({'product_uom_qty': consume})
        return self.write({'state': 'finish'})

class MrpGoLine(models.Model):
    _name = 'mrp.go.line'
            
    go_id = fields.Many2one('mrp.go', string='Go')
    product_id = fields.Many2one(
        'product.product', 'Product',
        readonly=True, required=True,)
    manufacture_qty = fields.Float('Number of Finished Product to be Produced with this Raw Item')
    planned_consume = fields.Float('Consume Planned')
    real_consume = fields.Float('Real Consume')
    
class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    go_id = fields.Many2one('mrp.go', string='Go')
